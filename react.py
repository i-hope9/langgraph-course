from dotenv import load_dotenv
from langchain import hub
from langchain.agents import create_react_agent
from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate
from langchain_aws.chat_models import ChatBedrock

load_dotenv()

react_prompt: PromptTemplate = hub.pull("hwchase17/react")

@tool
def triple(num: float) -> float:
    """
    :param num: a number to triple
    :return: the number tripled -> multiplied by 3
    """

    return 3 * float(num)

tools = [TavilySearch(max_results=1), triple]

llm = ChatBedrock(temperature=0, model="anthropic.claude-3-5-haiku-20241022-v1:0", region="us-west-2")

react_agent_runnable = create_react_agent(llm, tools, react_prompt)