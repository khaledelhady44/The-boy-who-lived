from langchain.chat_models import ChatOllama
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

prompt = ChatPromptTemplate.from_messages(

    [
        SystemMessage(content="""You are Harry Potter, a young wizard who responds in a modest and sincere way. You speak clearly and to 
                      the point, often with a bit of hesitation when you’re unsure, but you open up more when talking about meaningful topics 
                      like friendship, courage, or magic. You keep your responses brief when it’s just small talk or answering simple questions,
                       but when the topic is deeper, you may share personal experiences, thoughts, and reflections. You often mention your life 
                      at Hogwarts, your friends Ron and Hermione, your adventures, and the wisdom of Dumbledore. Always speak as Harry Potter
                       would, keeping your responses natural, heartfelt, and casual. You are friendly, humble, and occasionally show your dry 
                      sense of humor"""),
        
        MessagesPlaceholder(variable_name="messages")
    ]
)

# Define the base_url for the Ollama instance
base_url = "https://2490-34-143-221-157.ngrok-free.app"  # Replace with your server's base URL if necessary

# Initialize the Ollama chat model
model = ChatOllama(model="gemma2:9b-instruct-q5_0", base_url=base_url)


# Define a new graph
workflow = StateGraph(state_schema=MessagesState)


# Define the function that calls the model
def call_model(state: MessagesState):
    chain = prompt | model
    response = chain.invoke(state)
    return {"messages": response}


# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Add memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# query = input("Enter your message: ")
# config = {"configurable": {"thread_id": "abc345"}}
# while query != "Q":
#     input_messages = [HumanMessage(query)]
#     output = app.invoke({"messages": input_messages}, config)
#     print(output["messages"][-1].content)

#     query = input("Enter your message: ")
