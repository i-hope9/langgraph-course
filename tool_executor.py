import json
from dotenv import load_dotenv
from collections import defaultdict
from typing import List
from langchain_core.messages import BaseMessage, ToolMessage, HumanMessage, AIMessage
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolExecutor, ToolInvocation

from schemas import AnswerQuestion, Reflection
from chains import parser

load_dotenv()

search = TavilySearchAPIWrapper()
tavily_tool = TavilySearchResults(api_wrapper=search, max_results=5)
# batch()라는 메서드를 이용해 모든 tool invocation을 스레드 풀로 병렬 실행
tool_executor = ToolExecutor([tavily_tool])

# ToolMessage는 도구 실행 결과를 표현하는 표준 형식
def execute_tools(state: List[BaseMessage]) -> List[ToolMessage]:
    tool_invocation: AIMessage = state[-1]
    parsed_tool_calls = parser.invoke(tool_invocation)

    ids = []
    tool_invocation = []

    for parsed_call in parsed_tool_calls:
        for query in parsed_call["args"]["search_queries"]:
            tool_invocation.append(ToolInvocation(
                tool="tavily_search_results_json",  # tool name
                tool_input=query
            ))

            ids.append(parsed_call["id"])
    outputs = tool_executor.batch(tool_invocation)
    outputs_map = defaultdict(dict)
    for id_, output, invocation in zip(ids, outputs, tool_invocation):
        outputs_map[id_][invocation.tool_input] = output
    tool_messages = []
    for id_, mapped_output in outputs_map.items():
        tool_messages.append(
            ToolMessage(content=json.dumps(mapped_output), tool_call_id=id_)
        )

    return tool_messages


if __name__ == "__main__":
    print("Tool Executor 시작")

    human_message = HumanMessage(content = "Write about AI-Powered SOC / autonomous soc  problem domain,"
        " list startups that do that and raised capital.")
    
    answer = AnswerQuestion(
        answer="",
        reflection=Reflection(missing="", superfluous=""),
        search_queries=['AI cybersecurity machine learning techniques', 
                        'Autonomous SOC technical implementation challenges', 
                        'AI security operations market size and trends'],
        id = "call_KpYHichFFEmLitHFvFhKy1Ra"
    )

    raw_res = execute_tools(
        state=[
            human_message,
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": AnswerQuestion.__name__,
                        "args": answer.dict(),
                        "id": "call_KpYHichFFEmLitHFvFhKy1Ra"}
                ]
            )
        ]
    )