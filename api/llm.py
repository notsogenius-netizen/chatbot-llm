from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage


outputParser = StrOutputParser()

llm = OllamaLLM(model= "phi3")

template = ChatPromptTemplate([
        ("system", "You are a helpful assistant that tells jokes."),
        ("human", "Tell me about {topic}")
    ])
chain = template | llm
response = chain.invoke({"topic": "programming"})
print(response)