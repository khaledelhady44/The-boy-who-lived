import os
from langchain.schema import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import START, MessagesState, StateGraph, END
from helpers import get_settings
from llm.mongo_db_saver import MongoDBSaver
from llm.prompts import harry_prompt

settings = get_settings()
os.environ["GOOGLE_API_KEY"] =  settings.GOOGLE_API_KEY
llm = ChatGoogleGenerativeAI(
    model=settings.MODEL_NAME,
    temperature=0.7,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


harry = llm


def call_llm(state: MessagesState):
    chain = harry_prompt | harry
    result = chain.invoke(state["messages"])
    return {"messages": [AIMessage(content=result.content, name="harry potter")]}



def create_graph(checkpointer):

    workflow = StateGraph(state_schema=MessagesState)
    workflow.add_node("harry", call_llm)
    workflow.add_edge(START, "harry")
    workflow.add_edge("harry", END)

    app = workflow.compile(checkpointer=checkpointer)
    return app

def get_harry_answer(query: str, thread_id: str):

    with MongoDBSaver.from_conn_info(
         url = settings.MONGODB_URL, db_name="checkpoints"
    ) as checkpointer:
        graph = create_graph(checkpointer=checkpointer)
        config = {"configurable": {"thread_id": thread_id}}
        res = graph.invoke({"messages": [("human", query)]}, config)

    return res["messages"][-1].content





