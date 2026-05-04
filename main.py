from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from state import AgentState
from agents.coder import coder_node, tester_node
from tools.file_tools import tools
from langchain_core.messages import HumanMessage

# 1. Initialize Graph
workflow = StateGraph(AgentState)

# 2. Add Nodes
workflow.add_node("coder", coder_node)
workflow.add_node("tester", tester_node)
workflow.add_node("coder_tools", ToolNode(tools)) # Tool node for coder
workflow.add_node("tester_tools", ToolNode(tools)) # Tool node for tester

# 3. Define the Logic (Edges)
workflow.add_edge(START, "coder")

# CODER FLOW
workflow.add_conditional_edges(
    "coder", 
    tools_condition, 
    {
        "tools": "coder_tools", 
        "__end__": "tester" 
    }
)
workflow.add_edge("coder_tools", "coder") # Always go back to coder

# TESTER FLOW
workflow.add_conditional_edges(
    "tester",
    tools_condition,
    {
        "tools": "tester_tools",
        "__end__": END
    }
)
workflow.add_edge("tester_tools", "tester") # Always go back to tester

# 4. Compile
app = workflow.compile()

if __name__ == "__main__":
    initial_state : AgentState = {
        "messages": [HumanMessage(content="Fix the bug in workspace/src/app.py and verify it works by running it.")]
    }
    
    # We use a config to set recursion limit
    
    
    for event in app.stream(initial_state, config = {"recursion_limit": 50}):
        for key, value in event.items():
            print(f"\n--- Node: {key} ---")
            if "messages" in value:
                print(value["messages"][-1].content)