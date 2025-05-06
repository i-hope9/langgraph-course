from dotenv import load_dotenv

from pprint import pprint

load_dotenv()

from graph.chains.retrieval_grader import GradeDocuments, retrieval_grader
from ingestion import retriever
from graph.chains.generation import generation_chain

from graph.chains.hallucination_grader import (GradeHallucinations, hallucination_grader)

from graph.chains.router import question_router, RouteQuery

# 우리는 검색한 문서가 질문과 관련이 있는지 판단을 LLM에게 맡기고 있음
# 1. LLM이 믿을 만한 판단을 내리는지 확인이 필요
# 2. 실제 서비스를 돌려 보며 테스트 하기에는 비용 문제가 있을 수 있음 
def test_retrival_grader_answer_yes() -> None:
    question = "agent memory"
    docs = retriever.invoke(question)
    doc_txt = docs[1].page_content

    res: GradeDocuments = retrieval_grader.invoke(
        {"question": question, "document": doc_txt}
    )

    assert res.binary_score == "yes"


def test_retrival_grader_answer_no() -> None:
    question = "How to make pizza"
    docs = retriever.invoke(question)
    doc_txt = docs[1].page_content

    res: GradeDocuments = retrieval_grader.invoke(
        {"question": question, "document": doc_txt}
    )

    assert res.binary_score == "no"


def test_generation_chain() -> None:
    question = "agent memory"
    docs = retriever.invoke(question)
    generation = generation_chain.invoke({"context": docs, "question": question})
    pprint(generation)

def test_hallucination_grader_answer_yes() -> None:
    question = "agent memory"
    docs = retriever.invoke(question)

    generation = generation_chain.invoke({"context": docs, "question": question})
    res: GradeHallucinations = hallucination_grader.invoke(
        {"documents": docs, "generation": generation}
    )
    assert res.binary_score

def test_hallucination_grader_answer_no() -> None:
    question = "agent memory"
    docs = retriever.invoke(question)

    res: GradeHallucinations = hallucination_grader.invoke(
        {
            "documents": docs,
            "generation": "In order to make pizza we need to first start with the dough",
        }
    )
    assert not res.binary_score

def test_router_to_vectorstore() -> None:
    question = "agent memory"

    res: RouteQuery = question_router.invoke({"question": question})
    assert res.datasource == "vectorstore"