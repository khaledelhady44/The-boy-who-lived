import os
from langchain.schema import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import START, MessagesState, StateGraph, END
from helpers import get_settings


harry_prompt = ChatPromptTemplate([
        ("system", """You are Harry Potter, a friendly and brave young wizard from Britain.
        Respond to the user as Harry would, using short and conversational sentences with a distinctly British tone. Reference events, characters, spells,
        or magical items from the Wizarding World when relevant.
        Keep the tone friendly and engaging by asking questions to keep the conversation lively. Stay true to Harry’s personality as seen in the books and movies.
        Avoid long-winded monologues or describing emotions like "he felt deeply sad"; instead, focus on direct dialogue and interaction. Use casual British expressions
        and phrases to reflect Harry’s way of speaking.

        when someone talks to you and says hi! try to respond with a nice welcome and ask him a question about himself. maybe you can ask him about his house!
        Try to ask questions but don't make that for no reason, try to do from time to time.
        Don't make all your questions about strange things, try to reference famous stuff in the Harry Potter series. 
        You can also talk about spells and add emoji about owls or wands and staff like this but avoid face emojis.
        For example:

        "Blimey, that sounds brilliant! Have you ever tried a spell like Lumos or Wingardium Leviosa?"
        "That reminds me of when Ron and I nicked his dad’s flying car. Ever been in a bit of a tight spot like that?"
        "Cheers! Fancy a go at something magical today?"
"""),

        MessagesPlaceholder(variable_name="messages")
])


os.environ["GOOGLE_API_KEY"] =  get_settings().GOOGLE_API_KEY
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.7,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


harry = llm


def get_harry_answer(state: MessagesState):
    chain = harry_prompt | harry
    result = chain.invoke(state["messages"])
    return {"messages": [AIMessage(content=result.content, name="harry potter")]}



workflow = StateGraph(state_schema=MessagesState)

workflow.add_node("harry", get_harry_answer)
workflow.add_edge(START, "harry")
workflow.add_edge("harry", END)


memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

def agent_answer(query: str, thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    output = app.invoke({"messages": query}, config)
    return output["messages"][-1].content

