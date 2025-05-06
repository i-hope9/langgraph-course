from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_aws import ChatBedrock

# 검색된 문서 목록 중에서 질문과 관련 없는 문서를 제거하고,
# 관련 없는 문서가 있다면 웹 검색을 트리거하는 web_search: True 플래그를 설정하는 로직 구현
# 이를 위해 LangChain에서 LLM + Pydantic을 결합한 retrieval grader chain을 작성함

llm = ChatBedrock(temperature=0, model="anthropic.claude-3-5-haiku-20241022-v1:0", region="us-west-2")

class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score: str = Field(
        description="Documents are relevant to the question, 'yes' or 'no'"
    )

structured_llm_grader = llm.with_structured_output(GradeDocuments)

system = """You are a grader assessing relevance of a retrieved document to a user question. \n 
     If the document contains keyword(s) or semantic meaning related to the question, grade it as relevant. \n
     Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."""

grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
    ]
)

retrieval_grader = grade_prompt | structured_llm_grader