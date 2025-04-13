from dotenv import load_dotenv
from typing import List, Sequence
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph

from chains import generation_chain, reflection_chain

load_dotenv()


REFLECT = "reflect"
GENERATE = "generate"

def generation_node(state: Sequence[BaseMessage]):
    filtered_state = [msg for msg in state if msg.content.strip() != ""]
    return generation_chain.invoke({"messages": filtered_state})

def reflection_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
        # LLM에서 돌아오는 응답메세지의 역할을 AI인데 우리는 HumanMessage로 바꿔줌
        # LLM이 이 메세지를 사람이 보낸 것처럼 인식하게 만들기 위함 
        filtered_messages = [msg for msg in messages if msg.content.strip() != ""]
        res = reflection_chain.invoke({"messages": filtered_messages})
        return [HumanMessage(content=res.content)]

builder = MessageGraph()
builder.add_node(GENERATE, generation_node)
builder.add_node(REFLECT, reflection_node)
builder.set_entry_point(GENERATE)   # 시작 노드를 알려줌 

# 그래프에서 분기를 결정할 함수 구현 
def should_continue(state: List[BaseMessage]):
        if len(state) > 6:  # 6번 이상 실행했으면 END
                return END
        return REFLECT

builder.add_conditional_edges(GENERATE, should_continue)
builder.add_edge(REFLECT, GENERATE)

graph = builder.compile()
print(graph.get_graph().draw_mermaid()) # 그래프 시각화 
graph.get_graph().print_ascii()

if __name__ == "__main__":
        print("Hello LangGraph")
        inputs = HumanMessage(content="""Make this tweet better: @LangChainAI — newly Tool Calling feature is seriously underrated. After a long wait, it's  here- making the implementation of agents across different models with function calling - super easy. Made a video covering their newest blog post""")
        
        response = graph.invoke(inputs)     