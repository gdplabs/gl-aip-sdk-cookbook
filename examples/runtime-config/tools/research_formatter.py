"""Configurable research formatter tool - demonstrates tool_configs."""

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class FormatterConfig(BaseModel):
    """Tool configuration for research formatting."""

    style: str = Field(default="brief", description="Output style: brief, detailed, or academic")
    max_results: int = Field(default=5, ge=1, le=20, description="Maximum results to format")
    include_links: bool = Field(default=True, description="Include paper links")


class FormatterInput(BaseModel):
    """Input schema for research formatter."""

    query: str = Field(..., description="Research topic or query")
    papers: list[dict] = Field(default_factory=list, description="Papers to format")


class ResearchFormatterTool(BaseTool):
    """Format research results with configurable style."""

    name: str = "research_formatter"
    description: str = "Format research papers with configurable output style"
    args_schema: type[BaseModel] = FormatterInput
    tool_config_schema: type[BaseModel] = FormatterConfig

    def _run(
        self,
        query: str,
        papers: list[dict] | None = None,
        config: RunnableConfig | None = None,
    ) -> str:
        """Format research results based on configuration."""
        papers = papers or []
        tool_config = self.get_tool_config(config)

        style = tool_config.style
        max_results = tool_config.max_results
        include_links = tool_config.include_links

        # Limit results
        papers = papers[:max_results]

        if not papers:
            return f"No papers found for: {query}"

        # Format based on style
        if style == "brief":
            return self._format_brief(query, papers, include_links)
        elif style == "academic":
            return self._format_academic(query, papers, include_links)
        return self._format_detailed(query, papers, include_links)

    def _format_brief(self, query: str, papers: list[dict], include_links: bool) -> str:
        lines = [f"Results for '{query}':"]
        for i, p in enumerate(papers, 1):
            line = f"{i}. {p.get('title', 'Untitled')}"
            if include_links and p.get("url"):
                line += f" [{p['url']}]"
            lines.append(line)
        return "\n".join(lines)

    def _format_detailed(self, query: str, papers: list[dict], include_links: bool) -> str:
        lines = [f"# Research Results: {query}\n"]
        for p in papers:
            lines.append(f"## {p.get('title', 'Untitled')}")
            lines.append(f"Authors: {p.get('authors', 'Unknown')}")
            if p.get("abstract"):
                lines.append(f"Abstract: {p['abstract'][:200]}...")
            if include_links and p.get("url"):
                lines.append(f"Link: {p['url']}")
            lines.append("")
        return "\n".join(lines)

    def _format_academic(self, query: str, papers: list[dict], include_links: bool) -> str:
        lines = [f"Literature Review: {query}\n"]
        for i, p in enumerate(papers, 1):
            authors = p.get("authors", "Unknown")
            title = p.get("title", "Untitled")
            year = p.get("year", "n.d.")
            line = f"[{i}] {authors} ({year}). {title}."
            if include_links and p.get("url"):
                line += f" Available at: {p['url']}"
            lines.append(line)
        return "\n".join(lines)
