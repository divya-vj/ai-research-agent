# agent.py — AI Research Assistant Agent

from dotenv import load_dotenv
import os
load_dotenv()

from tavily import TavilyClient
from langchain_groq import ChatGroq
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain_core.prompts import PromptTemplate


# ── Web Search ────────────────────────────────────────────────────────────
def search_web(query, max_results=5):
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    results = client.search(
        query=query,
        search_depth="advanced",
        max_results=max_results,
        include_answer=True,
    )
    return results


def format_search_results(results):
    output = []
    if results.get("answer"):
        output.append(f"Quick Summary: {results['answer']}")
        output.append("")
    for i, result in enumerate(results["results"], 1):
        output.append(f"[Source {i}]")
        output.append(f"Title: {result['title']}")
        output.append(f"URL: {result['url']}")
        output.append(f"Relevance Score: {result['score']:.4f}")
        output.append(f"Content: {result['content'][:300]}")
        output.append("-" * 40)
    return "\n".join(output)


# ── Tool ──────────────────────────────────────────────────────────────────
def tavily_search_tool(query: str) -> str:
    results = search_web(query, max_results=3)
    return format_search_results(results)


tools = [
    Tool(
        name="WebSearch",
        func=tavily_search_tool,
        description=(
            "Search the web for current and accurate information. "
            "Use this tool when you need up-to-date facts, recent "
            "developments, statistics, expert opinions, or any "
            "information that requires current knowledge. "
            "Input should be a specific and focused search query. "
            "Use different queries each time to gather diverse information."
        )
    )
]


# ── ReAct Prompt ──────────────────────────────────────────────────────────
REACT_PROMPT_TEMPLATE = """You are an expert research assistant with access to web search.
Your job is to research any topic thoroughly and produce a comprehensive report.

You have access to these tools:
{tools}

Tool names: {tool_names}

To complete a research task, use this EXACT format every time:

Thought: [think about what aspect to research first]
Action: WebSearch
Action Input: [your specific search query]
Observation: [search results will appear here automatically]
Thought: [analyse results and decide what else to search]
Action: WebSearch
Action Input: [different search query to cover another angle]
Observation: [search results]
Thought: [continue until you have enough for a full report]
Thought: I now have comprehensive information to write the research report.
Final Answer: [your complete structured research report]

IMPORTANT RULES:
1. Always search at least 3 times with DIFFERENT queries
2. Each query should explore a DIFFERENT aspect of the topic
3. Never repeat the same search query twice
4. Cite sources URLs in your final answer
5. Structure your Final Answer with these exact sections:

## RESEARCH REPORT: [Topic Title]

### Executive Summary
[2-3 sentence overview]

### Key Findings
[5-7 bullet points of most important facts]

### Detailed Analysis
[3-4 paragraphs of analysis]

### Current Trends (2025-2026)
[What is happening right now]

### Sources
[List all URLs used]

Begin researching now.

Question: {input}
{agent_scratchpad}"""

prompt = PromptTemplate(
    template=REACT_PROMPT_TEMPLATE,
    input_variables=["tools", "tool_names", "input", "agent_scratchpad"]
)


# ── Build Agent ───────────────────────────────────────────────────────────
def build_agent():
    llm = ChatGroq(
        model_name="llama-3.1-8b-instant",
        temperature=0.1,
        max_tokens=4096,
        api_key=os.getenv("GROQ_API_KEY")
    )

    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=10,
        handle_parsing_errors=True,
        return_intermediate_steps=False
    )

    return executor


# ── Research Function ─────────────────────────────────────────────────────
def research_topic(topic: str) -> str:
    print(f"\nStarting research on: {topic}")
    print("Agent is working... watch the thinking process below")
    print("=" * 60)

    executor = build_agent()
    result = executor.invoke({"input": topic})

    return result["output"]


# ── Test Block ────────────────────────────────────────────────────────────
if __name__ == "__main__":

    print("=" * 60)
    print("REACT AGENT TEST")
    print("=" * 60)

    topic = "What are the key differences between RAG and fine-tuning for LLMs and when should you use each?"

    report = research_topic(topic)

    print("\n" + "=" * 60)
    print("FINAL REPORT:")
    print("=" * 60)
    print(report)
