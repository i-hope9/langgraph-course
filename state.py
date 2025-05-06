import operator
from typing import Annotated, TypedDict, Union

from langchain_core.agents import AgentAction, AgentFinish


class AgentState(TypedDict):
    input: str
    # AgentAction: 도구 실행이 필요함 (예: 검색, 계산 등)
	# AgentFinish: 이미 최종 답변이 만들어짐 (더 이상 추론 불필요)
	# None: 아직 아무 추론도 하지 않은 초기 상태
    agent_outcome: Union[AgentAction, AgentFinish, None]
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]