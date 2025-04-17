from typing import List
from pydantic import BaseModel, Field

class Reflection(BaseModel):
    missing: str = Field(description="Critique of what is missing.")
    superfluous: str = Field(description="Critique of what is superfluous")

class AnswerQuestion(BaseModel):
    """Answer the question."""
    #LLM에게 어떤 값을 채워야 하는지를 필드의 설명(description)을 통해 지시
    answer: str = Field(description="~250 word detailed answer to the question.")
    reflection: Reflection = Field(description="Your reflection on the initial answer.")
    search_queries: List[str] = Field(
        description="1-3 search queries for researching improvements to address the critique of your current answer."
    )

class ReviseAnswer(AnswerQuestion): 
    """Revise your original answer to your question."""
    references: List[str] = Field(
        description="Citations motivating your updated answer."
    )