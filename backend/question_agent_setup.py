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
                    Generate 2 diverse, related questions. 3-5 words each. Broken English OK. Split questions by \n. Don't number questions.
                    Questions should be leading users down an analytical path.
                    some sample questions:
                    Select Oscar-winning movies
                    Select movies that belong to multiple genres
                    Select the top viewed movies from January to June
                    Select movies released before the year 2000
                    Select movies with a runtime greater than 2 hours
                    Select movies available globally
                    Select movies projected on film
                    Select movies projected digitally
                    Identify titles with high worldwide gross but low ratings
                    Calculate ROI for each title
                    Calculate cost per view for each title
                    Rank U.S. movies by their audience engagement relative to their profit
                    Rank U.S. movies by profit-weighted audience engagement efficiency
                    Calculate budget to rating efficiency
                    Find low-budget, critically acclaimed U.S. films with low viewership
                    Names of US origin directors who make profitable movies in action genre
                    Rank U.S. movies by budget as a predictor of performance
                    Select profitable movies
                    List individual movie genres with the highest box office ROI, grouped by budget range and release decade for US movies
                    List the top movie genres based on average streaming performance (total hours viewed) in the United States, grouped by budget range and release decade
    """
                            )
        
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def generate_questions(self, current_question, chat_history):
        result = self.chain.run(current_question=current_question, chat_history=chat_history)
        
        # Parse the result into a list of questions
        questions = [q.strip() for q in result.split('\n') if q.strip()]
        return questions[:2]  # Ensure we return at most 3 questions

def setup_question_generator():
    return QuestionGeneratorAgent()