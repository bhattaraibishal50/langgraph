from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
# In memorySave, SqliteSave, postGresqlsave
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sqlite3

load_dotenv()

llm = ChatOpenAI()

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}

# sql work on single thread, so we set check_same_thread to False to allow multiple threads to access the database　
conn = sqlite3.connect(database='chatbot.db', check_same_thread=False) 
# Checkpointer
checkpointer = SqliteSaver(conn=conn)

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    # in set it will only keep unique values, we want unique thread ids, so we can use set comprehension to get all unique thread ids from the checkpoints
    all_threads = set()
    for checkpoint in checkpointer.list(None): # fetch all chdckpoints
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)


