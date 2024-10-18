from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

class QuestionGeneratorAgent:
    def __init__(self, model="gpt-3.5-turbo"):
        self.llm = ChatOpenAI(model=model, temperature=0.7)
        
        self.prompt = PromptTemplate(
            input_variables=["current_question", "chat_history"],
            template="""Q: {current_question}
                    Context: {chat_history}
                    Generate 2 diverse, related questions. 3-5 words each. Broken English OK. Split questions by \n. Don't number questions.:"""
                            )
        
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def generate_questions(self, current_question, chat_history):
        result = self.chain.run(current_question=current_question, chat_history=chat_history)
        
        # Parse the result into a list of questions
        questions = [q.strip() for q in result.split('\n') if q.strip()]
        return questions[:2]  # Ensure we return at most 3 questions

def setup_question_generator():
    return QuestionGeneratorAgent()