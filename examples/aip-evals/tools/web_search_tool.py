"""Web Search Tool — Returns mocked search results for the research agent.

This is a custom LangChain ``BaseTool`` subclass that returns a fixed set of
mocked search results. It is intentionally self-contained so the cookbook can
be run without depending on any external search API.
"""

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


MOCKED_SEARCH_RESULTS = [
    {
        "title": "LIST OF REGIONS HIT BY HEAVY RAIN ON THURSDAY, JUNE 11, 2026",
        "link": "https://www.youtube.com/watch?v=N0E5Z34r9KM",
        "snippet": (
            "Indonesia on Thursday (June 11, 2026). According to Kompas.com, "
            "the agency has warned residents in low-lying areas to remain on alert."
        ),
        "date": "June 11, 2026",
        "position": 1,
    },
    {
        "title": "5 stories you might have missed, June 11, 2026 | The Straits Times",
        "link": "https://www.straitstimes.com/world/while-you-were-sleeping-5-stories-you-might-have-missed-june-11-2026",
        "snippet": (
            "Indonesia floods wipe out 7% of rare orang utans. PHOTO: AFP. "
            "Deadly floods and landslides in Indonesia's Sumatra in 2026 wiped out a large share of the species' habitat."
        ),
        "date": "June 11, 2026",
        "position": 2,
    },
    {
        "title": "Laos, Indonesia deepen bilateral ties during official visit",
        "link": "https://asianews.network/laos-indonesia-deepen-bilateral-ties-during-official-visit/",
        "snippet": (
            "Laos, Indonesia deepen bilateral ties during official visit. "
            "The visit was aimed at further enhancing the longstanding friendship between the two Southeast Asian nations."
        ),
        "date": "May 7, 2026",
        "position": 3,
    },
    {
        "title": "Indonesia Volcano Erupts, Forcing Airport to Close",
        "link": "https://english.aawsat.com/varieties/5280661-indonesia-volcano-erupts-forcing-airport-close",
        "snippet": (
            "Mount Lewotobi Laki-Laki on Flores Island erupted at 11:15 am (0315 GMT) on May 25, 2026, "
            "sending volcanic material 2.5 kilometers (1.6 miles) into the air, the country's disaster agency said."
        ),
        "date": "May 25, 2026",
        "position": 4,
    },
    {
        "title": "Indonesia's Prabowo says economy grew 5.1% in Q1 2026",
        "link": "https://en.antaranews.com/news/indonesia-q1-2026-gdp",
        "snippet": (
            "President Prabowo Subianto announced on May 5, 2026 that Indonesia's economy grew 5.1% in the first quarter, "
            "driven by strong domestic consumption and a recovery in tourism."
        ),
        "date": "May 5, 2026",
        "position": 5,
    },
]


class SearchInput(BaseModel):
    query: str = Field(description="The search query string.")


class WebSearchTool(BaseTool):
    name: str = "web_search"
    description: str = (
        "Search the web for a given query and return a list of relevant results. "
        "Each result contains a title, link, snippet, and position."
    )
    args_schema: type[BaseModel] = SearchInput

    def _run(self, query: str) -> list[dict]:
        return MOCKED_SEARCH_RESULTS


__all__ = ["WebSearchTool"]
