from langchain_ollama import ChatOllama
from tools.file_tools import tools

llm = ChatOllama(model="qwen3.5:2b", temperature=0).bind_tools(tools)

def coder_node(state):
    messages = state["messages"]
    # Provide clear instruction so it doesn't try to "Test" yet
    system_msg = ("system", "You are a Coder. Fix the code and use 'lint_code' to verify syntax. When done, summarize your changes.")
    response = llm.invoke([system_msg] + list(messages))
    return {"messages": [response]}

def tester_node(state):
    messages = state["messages"]
    # Instruction to use the execution tool
    system_msg = ("system", "You are a Tester. Use 'execute_code' to run the file. If it passes, say 'STAMP OF APPROVAL'. If it fails, describe why.")
    response = llm.invoke([system_msg] + list(messages))
    return {"messages": [response]}