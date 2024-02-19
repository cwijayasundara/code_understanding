from langchain.chains import LLMChain
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model_name='gpt-4-0125-preview',
                 streaming=True,
                 callbacks=[StreamingStdOutCallbackHandler()],
                 temperature=0
                 )


prompt = """System: You are an expert in Python programming. Explain the provided code in plain English.

Human: {input}

Explanation:

"""

code_explanation_chain = LLMChain.from_string(
    llm=llm,
    template=prompt
)

prompt = """System: You are an expert in Python programming. Generate a unit test for the following code snippet. DO 
NOT GENERATE ANY EXPLANATION AND JUST RETURN THE UNIT TEST!!

Human: {input}

Unit test:
"""

unit_test_chain = LLMChain.from_string(
    llm=llm,
    template=prompt
)
