from dotenv import load_dotenv
load_dotenv()

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

# MemorySaver: 노드 실행 결과를 메모리에 저장함 (그래프 실행 후 휘발됨)

class State(TypedDict):
    input: str
    user_feedback: str

def step_1(state: State) -> None:
    print("--Step 1--")

def human_feedback(state: State) -> None:
    print("--Human Feedback--")

def step_3(state: State) -> None:
    print("--Step 3--")

builder = StateGraph(State)
builder.add_node("step_1", step_1)
builder.add_node("human_feedback", human_feedback)
builder.add_node("step_3", step_3)
builder.add_edge(START, "step_1")
builder.add_edge("step_1", "human_feedback")
builder.add_edge("human_feedback", "step_3")
builder.add_edge("step_3", END)

# memory = MemorySaver()
conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
memory = SqliteSaver(conn)
# memory = SqliteSaver.from_conn_string("checkpoints.sqlite")

# Graph 실행을 "human_feedback" 전에 잠깐 멈춘다 
graph = builder.compile(checkpointer=memory, interrupt_before=["human_feedback"])

#graph.get_graph().draw_mermaid_png(output_file_path="graph.png")

if __name__ == "__main__":
    thread = {"configurable": {"thread_id": "999"}}

    # initial_input = {"input": "hello world"}

    # # LangGraph에서 정의한 노드 그래프를 노드 단위로 순차 실행하면서, 각 노드의 출력 결과나 상태 변경을 스트림(stream) 형식으로 반환
    # for event in graph.stream(initial_input, thread, stream_mode="values"):
    #     print(event)
    
    # print(graph.get_state(thread).next)

    user_input = input("Tell me how you want to update the state: ")
    graph.update_state(thread, {"user_feedback": user_input}, as_node="human_feedback")
    
    print("--State after update--")
    print(graph.get_state(thread))

    for event in graph.stream(None, thread, stream_mode="values"):
        print(event)