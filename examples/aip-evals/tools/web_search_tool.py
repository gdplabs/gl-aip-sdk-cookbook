"""Web Search Tool — Returns mocked search results for the research agent.

This is a custom LangChain ``BaseTool`` subclass that returns a fixed set of
mocked search results. It is intentionally self-contained so the cookbook can
be run without depending on any external search API.
"""

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


MOCKED_SEARCH_RESULTS = [
    {
        "title": "The Jakarta Post - Still bold, fiercely independent",
        "link": "https://www.thejakartapost.com/",
        "snippet": (
            "Indonesia · Politics. Prosecutors reject Nadiem's defense plea in "
            "Chromebook corruption case ; Business · Economy. Pertamina hikes "
            "Pertamax prices by 32% amid high ..."
        ),
        "position": 1,
    },
    {
        "title": "LIST OF REGIONS HIT BY HEAVY RAIN ON THURSDAY, JUNE 11 ...",
        "link": "https://www.youtube.com/watch?v=N0E5Z34r9KM",
        "snippet": (
            "... Indonesia on Thursday (June 11, 2026). According to Kompas.com ... "
            "news app on the Play Store or App Store for a new experience. LIST OF ..."
        ),
        "date": "19 hours ago",
        "position": 2,
    },
    {
        "title": "Indonesia National Holidays and Collective Leave Days 2026",
        "link": "https://www.bankofchina.co.id/m/en-id/service/information/latest-news/2025/public-holiday-2026.html",
        "snippet": (
            "Indonesia National Holidays and Collective Leave Days 2026 ; "
            "1 June. Monday. Pancasila Day ; 16 June. Tuesday. Islamic New Year 1448 H ; "
            "17 August. Monday."
        ),
        "position": 3,
    },
    {
        "title": "ANTARA News: Latest Indonesia News",
        "link": "https://en.antaranews.com/",
        "snippet": (
            "Trade Ministry to route all coal exports through PT DSI by 2027 · "
            "Prabowo says Indonesia remains open to foreign investors · "
            "Prabowo defends foreign trips, cites ..."
        ),
        "position": 4,
    },
    {
        "title": "5 stories you might have missed, June 11, 2026 | The Straits Times",
        "link": "https://www.straitstimes.com/world/while-you-were-sleeping-5-stories-you-might-have-missed-june-11-2026",
        "snippet": (
            "Indonesia floods wipe out 7% of rare orang utans. PHOTO: AFP. "
            "Deadly floods and landslides in Indonesia's Sumatra in 2025 wiped ..."
        ),
        "date": "7 hours ago",
        "position": 5,
    },
    {
        "title": "Laos, Indonesia deepen bilateral ties during official visit",
        "link": "https://asianews.network/laos-indonesia-deepen-bilateral-ties-during-official-visit/",
        "snippet": (
            "Laos, Indonesia deepen bilateral ties during official visit. "
            "The visit was aimed at further enhancing the longstanding friendship ..."
        ),
        "date": "May 7, 2026",
        "position": 6,
    },
    {
        "title": "Indonesia - AP News",
        "link": "https://apnews.com/hub/indonesia",
        "snippet": (
            "Indonesian court finds 4 military members guilty of acid attack on activist, "
            "sends them to prison · Indonesia arrests former nutrition agency head and officials ..."
        ),
        "position": 7,
    },
    {
        "title": "Indonesia Volcano Erupts, Forcing Airport to Close",
        "link": "https://english.aawsat.com/varieties/5280661-indonesia-volcano-erupts-forcing-airport-close",
        "snippet": (
            "Mount Lewotobi Laki-Laki on Flores Island erupted at 11:15 am (0315 GMT), "
            "sending volcanic material 2.5 kilometers (1.6 miles) into the air, the ..."
        ),
        "position": 8,
    },
    {
        "title": "June Mission To Gaza: Indonesia Confirms Humanitarian-only ...",
        "link": "https://www.i24news.tv/en/news/middle-east/palestinian-territories/artc-june-mission-to-gaza-indonesia-confirms-humanitarian-only-deployment",
        "snippet": (
            "Indonesia has confirmed that the forces it plans to deploy in the Gaza Strip "
            "will not engage in combat, emphasizing that their role will ..."
        ),
        "date": "Feb 16, 2026",
        "position": 9,
    },
    {
        "title": "The Latest on Southeast Asia: Indonesia joins BRICS - CSIS",
        "link": "https://www.csis.org/blogs/latest-southeast-asia/latest-southeast-asia-indonesia-joins-brics",
        "snippet": (
            "On January 7, Indonesia became the first Southeast Asian nation to formally join "
            "BRICS, an intergovernmental bloc consisting of countries from the Global South."
        ),
        "date": "Jan 16, 2025",
        "position": 10,
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
