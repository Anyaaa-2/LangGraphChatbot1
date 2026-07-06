import google.generativeai as genai
from typing import Optional
from typing_extensions import TypedDict

import networkx as nx 
import matplotlib.pyplot as plt
from langgraph.graph import StateGraph 

import os
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def ask_gemini(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini API error: {e}"
    
class GraphState(TypedDict):
    question: Optional[str]
    classification: Optional[str]
    response: Optional[str]
    

def classify(state: GraphState) -> GraphState:
    question = state.get("question","").lower()
    if any(word in question for word in ["hello","hi","hey","good morning","good evening"]):
        classification = "greeting"
    else:
        classification = "search"

    return{
        **state,
        "classification": classification 
    }

def respond(state: GraphState) -> GraphState:
    classification = state.get("classification")
    question = state.get("question")

    if classification == "greeting":
        response = "Hello! how can i help u today?"
    elif classification =="search":
        response = ask_gemini(question)
    else:
        response = "idk how to respond to that"

    return{
        **state,
        "response":response 
    }

builder = StateGraph(GraphState)
builder.add_node("classify",classify)
builder.add_node("respond",respond)
builder.set_entry_point("classify")
builder.add_edge("classify","respond")
builder.set_finish_point("respond")
app = builder.compile()

def visualize_workflow(builder):
    G = nx.DiGraph()
    for node in builder.nodes:
        G.add_node(node)
    for edge in builder.edges:
        G.add_edge(edge[0],edge[1])

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=3000,
            node_color="skyblue", font_size=12, font_weight="bold", arrows=True)

    plt.title("Langchain Workflow Visualization")
    plt.show()

visualize_workflow(builder)

print("=== Gemini-Powered Chatbot ===")
print("Type your question below. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.strip().lower() in ['exit', 'quit']:
        print("Bot: Goodbye!")
        break

    state = {"question": user_input}
    result = app.invoke(state)
    print("Bot:", result["response"])