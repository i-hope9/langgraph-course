from typing import Any, Dict

from graph.chains.generation import generation_chain
from graph.state import GraphState

# LangGraph에서 최종적으로 질문에 대한 답변을 생성하는 노드(node)

def generate(state: GraphState) -> Dict[str, Any]:
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]

    generation = generation_chain.invoke({"context": documents, "question": question})
    return {"documents": documents, "question": question, "generation": generation}