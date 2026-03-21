from dotenv import load_dotenv
import os
load_dotenv()


# ── DAY 1: Tavily Web Search ──────────────────────────────────────────────
from tavily import TavilyClient


def search_web(query, max_results=5):
    """
    Search the web using Tavily and return structured results.

    Args:
        query: search query string
        max_results: how many results to return (default 5)

    Returns:
        dict with keys:
          - answer: Tavily's quick AI-generated answer
          - results: list of result dicts, each with:
              - title: page title
              - url: page URL
              - content: extracted page content
              - score: relevance score (0 to 1, higher is better)
    """
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    results = client.search(
        query=query,
        search_depth="advanced",   # visits actual pages, not just snippets
        max_results=max_results,
        include_answer=True,       # Tavily generates a quick summary answer
    )

    return results


def format_search_results(results):
    """
    Format raw Tavily results into clean text for LLM consumption.

    Args:
        results: raw dict from search_web()

    Returns:
        formatted string with all results
    """
    output = []

    # Add Tavily's quick answer if available
    if results.get("answer"):
        output.append(f"Quick Summary: {results['answer']}")
        output.append("")

    # Add each result
    for i, result in enumerate(results["results"], 1):
        output.append(f"[Source {i}]")
        output.append(f"Title: {result['title']}")
        output.append(f"URL: {result['url']}")
        output.append(f"Relevance Score: {result['score']:.4f}")
        output.append(f"Content: {result['content'][:600]}")
        output.append("-" * 40)

    return "\n".join(output)


# ── TEST BLOCK ────────────────────────────────────────────────────────────
if __name__ == "__main__":

    print("=" * 60)
    print("TAVILY SEARCH TEST")
    print("=" * 60)

    # Test 1: Basic search
    query1 = "latest developments in AI agents 2026"
    print(f"\nTest 1: {query1}")
    print("-" * 40)

    raw_results = search_web(query1, max_results=3)

    print(f"Total results returned: {len(raw_results['results'])}")
    print(f"Quick Answer available: {bool(raw_results.get('answer'))}")
    print()

    # Show raw structure of first result
    print("Raw structure of first result:")
    first = raw_results["results"][0]
    print(f"  Keys available: {list(first.keys())}")
    print(f"  Title:   {first['title']}")
    print(f"  URL:     {first['url']}")
    print(f"  Score:   {first['score']}")
    print(f"  Content length: {len(first['content'])} characters")
    print()

    # Show formatted output
    print("Formatted output (what LLM will see):")
    print("-" * 40)
    formatted = format_search_results(raw_results)
    print(formatted[:800])
    print("...")

    # Test 2: Different query
    print("\n" + "=" * 60)
    query2 = "how do LangChain agents work"
    print(f"Test 2: {query2}")
    print("-" * 40)

    raw2 = search_web(query2, max_results=3)
    formatted2 = format_search_results(raw2)
    print(formatted2[:600])
    print("...")

    print("\n" + "=" * 60)
    print("SEARCH TEST COMPLETE")
    print("Both queries returned structured results.")
    print("Tavily is ready for the agent.")