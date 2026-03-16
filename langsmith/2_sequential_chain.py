from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

# If we want to change the project
os.environ["LANGCHAIN_PROJECT"] = "Langsmith-demo2"

load_dotenv()

prompt1 = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(


     
    template='Generate a 5 pointer summary from the following text \n {text}',
    input_variables=['text']
)

model1 = ChatOpenAI()
model2 = ChatOpenAI(model='gpt-4o', temperature=0.7)

parser = StrOutputParser()

chain = prompt1 | model1 | parser | prompt2 | model2 | parser

# can sent the config with the run, or set it globally on the chain
config = {
    'tags': ['llm_chain', 'demo'],
    'metadata': {
        'description': 'A chain that generates a report and then summarizes it.',
        'version': '1.0'    
    }
}
result = chain.invoke({'topic': 'Unemployment in Nepal'}, config=config)

print(result)
