import streamlit as st
import warnings
import util

from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from chains import unit_test_chain, code_explanation_chain

warnings.filterwarnings('ignore')

load_dotenv()

vectorstore = Chroma(persist_directory="./vectorstore",
                     embedding_function=OpenAIEmbeddings())

retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 8})

llm = ChatOpenAI(model_name="gpt-4-1106-preview")

memory = ConversationSummaryMemory(
    llm=llm,
    memory_key="chat_history",
    return_messages=True
)

qa = ConversationalRetrievalChain.from_llm(llm,
                                           retriever=retriever,
                                           memory=memory)

files = util.get_py_files()

st.title("Chat with your codebase!")
request = st.text_area('How can I help you today! ', height=50)
submit = st.button("submit", type="primary")

st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 800px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    add_radio = st.radio(
        "Choose a file!",
        files
    )
    st.markdown(""" :red[explain code in English--> generate unit test] """, unsafe_allow_html=True)
    analyst = st.button("analyse", type="primary")
    if analyst:
        selected_file = util.load_file_by_name(add_radio)
        st.write("I'm thinking...")
        st.markdown(""" :blue[Code Explanation : ] """, unsafe_allow_html=True)
        code_explanation = code_explanation_chain(selected_file)
        st.write(code_explanation["text"])
        st.markdown(""" :blue[Unit Test : ] """, unsafe_allow_html=True)
        test_chain = unit_test_chain(selected_file)
        st.write(test_chain["text"])


if submit and request:
    result = qa(request)
    st.write(result["answer"])
