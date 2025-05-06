from typing import Any, Dict
from graph.state import GraphState
from ingestion import retriever

def retrieve(state: GraphState) -> Dict[str, Any]:
    print("--RETRIEVE--")
    question = state["question"]
    documents = retriever.invoke(question)  # 벡터 임베딩 기반 의미 검색 수행

    # question은 추가 정보. 필수는 아님.
    return {"documents": documents, "question": question}