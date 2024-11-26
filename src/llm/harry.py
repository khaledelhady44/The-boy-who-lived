import os
from langchain.schema import AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import START, MessagesState, StateGraph, END
from helpers import get_settings
from llm.mongo_db_saver import MongoDBSaver
from llm.prompts import harry_prompt

os.environ["GOOGLE_API_KEY"] =  get_settings().GOOGLE_API_KEY
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
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



workflow = StateGraph(state_schema=MessagesState)

workflow.add_node("harry", call_llm)
workflow.add_edge(START, "harry")
workflow.add_edge("harry", END)


memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

def get_harry_answer(query: str, thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    output = app.invoke({"messages": query}, config)
    return output["messages"][-1].content


# async with AsyncMongoDBSaver.from_conn_info(
#     host="localhost", port=27017, db_name="checkpoints"
# ) as checkpointer:
#     graph = create_react_agent(model, tools=tools, checkpointer=checkpointer)
#     config = {"configurable": {"thread_id": "2"}}
#     res = await graph.ainvoke(
#         {"messages": [("human", "what's the weather in nyc")]}, config
#     )

#     latest_checkpoint = await checkpointer.aget(config)
#     latest_checkpoint_tuple = await checkpointer.aget_tuple(config)
#     checkpoint_tuples = [c async for c in checkpointer.alist(config)]


