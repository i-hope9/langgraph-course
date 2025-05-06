from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode
from react import react_agent_runnable, tools
from state import AgentState

load_dotenv()

def run_agent_reasoning_engine(state: AgentState):
    agent_outcome = react_agent_runnable.invoke(state)
    return {"agent_outcome": agent_outcome} # agent_outcome은 계속 덮어 씌워짐

tool_executor = ToolNode(tools)

def execute_tools(state: AgentState):
    agent_action = state["agent_outcome"]
    tool_name = agent_action.tool
    tool_input = agent_action.tool_input
    
    # added code 
    if tool_name == "tavily_search" and isinstance(tool_input, str):
        formatted_input = {"query": tool_input.strip()}
        print(f"Formatted input: {formatted_input}")
        
        # call the Tavily directly 
        from react import tools
        for tool in tools:
            if tool.name == tool_name:
                output = tool.invoke(formatted_input)
                return {"intermediate_steps": [(agent_action, str(output))]}
    
    # original code 
    output = tool_executor.invoke(agent_action)
    return {"intermediate_steps": [(agent_action, str(output))]}