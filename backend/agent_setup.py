from langchain_community.utilities import SQLDatabase
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import TimescaleVector

from langchain.tools import tool
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from config import Config
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder, ChatPromptTemplate
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain.schema import HumanMessage, AIMessage
from langchain_community.vectorstores import FAISS
from agent_helper import examples, system_prefix


def get_conversation(db_conversation):
    chat_history = []
    for index, text in enumerate(db_conversation):
        if index % 2 == 0:
            chat_history.append(HumanMessage(content=text))
        else:
            chat_history.append(AIMessage(content=text))
    return chat_history


def setup_agent(db_conversation):
    # Initialize embeddings for vector-based search
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    
    # Initialize the language model (GPT-4)
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    
    # Set up the external database connection (for retrieving data, not storing it)
    db = SQLDatabase.from_uri(Config.EXTERNAL_DB_URL)
    chat_history = get_conversation(db_conversation=db_conversation)
    # Set up conversation memory for handling multi-turn interactions
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    memory.chat_memory.messages = chat_history


    # Initialize vector stores for different data collections (from external sources)
    vec_movie = TimescaleVector(embedding=embeddings, service_url=Config.EXTERNAL_DB_URL, collection_name="movie_embeddings")
    vec_technical = TimescaleVector(embedding=embeddings, service_url=Config.EXTERNAL_DB_URL, collection_name="technical_specifications")
    vec_name = TimescaleVector(embedding=embeddings, service_url=Config.EXTERNAL_DB_URL, collection_name="name_embeddings")
    
    # Define custom tools to fetch data from vector stores (external)
    @tool
    def get_movie_ids(query):
        '''Retrieve movie IDs based on a similar plot, detail, or descriptor.'''
        results = vec_movie.similarity_search(query, k=10)
        return [res.metadata['movie_id'] for res in results]
    
    @tool
    def get_technical_details(query):
        '''Retrieve technical details such as camera models, sound mixes, or processes.'''
        results = vec_technical.similarity_search(query)
        return [res.page_content for res in results]
    
    @tool
    def get_name_ids(query):
        '''Retrieve name IDs of actors, directors, or writers based on their bio or descriptor.'''
        results = vec_name.similarity_search(query, k=10)
        return [res.metadata['name_id'] for res in results]
    
    # Example selector for dynamic prompt completion
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples, embeddings, FAISS, k=5, input_keys=["input"]
    )


    # Few-shot prompt configuration
    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=PromptTemplate.from_template(
            "User input: {input}\nSQL query: {query}"
        ),
        input_variables=["input", "dialect", "top_k"],
        prefix=system_prefix,
        suffix="",
    )

    full_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate(prompt=few_shot_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    # Create the agent with SQL and vector search capabilities
    agent = create_sql_agent(
        llm=llm,
        db=db,
        prompt=full_prompt,
        verbose=True,
        agent_type="openai-tools",
        extra_tools=[get_movie_ids, get_technical_details, get_name_ids],
        top_k=10,
        memory=memory,
        agent_executor_kwargs={"memory": memory}
    )

    return agent
