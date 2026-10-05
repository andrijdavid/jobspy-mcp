import pytest
from mcp.server.fastmcp import FastMCP

from jobspy_mcp.server import mcp, list_job_sites


def test_mcp_instance():
    assert isinstance(mcp, FastMCP)


def test_tools_registered():
    tools = mcp._tool_manager.list_tools()
    tool_names = {t.name for t in tools}
    assert "search_jobs" in tool_names
    assert "list_job_sites" in tool_names


def test_list_job_sites_returns_sites():
    result = list_job_sites()
    assert "sites" in result
    assert "linkedin" in result["sites"]
    assert "indeed" in result["sites"]
    assert "zip_recruiter" in result["sites"]
    assert "glassdoor" in result["sites"]
    assert len(result["sites"]) >= 6


def test_list_job_sites_includes_notes():
    result = list_job_sites()
    assert "notes" in result
    assert "linkedin" in result["notes"]


def test_list_job_sites_known_sites_count():
    result = list_job_sites()
    assert len(result["sites"]) == 8


async def test_search_jobs_maps_deprecated_fetch_flag(monkeypatch):
    import jobspy_mcp.server as server

    seen = {}
    monkeypatch.setattr(server, "_run_scrape", lambda kw: seen.update(kw))
    await server.search_jobs(
        linkedin_fetch_description=True,
        linkedin_company_ids=[1, 2],
        enforce_annual_salary=True,
        user_agent="ua",
    )
    assert seen["fetch_description"] is True
    assert "linkedin_fetch_description" not in seen
    assert seen["linkedin_company_ids"] == [1, 2]
    assert seen["enforce_annual_salary"] is True
    assert seen["user_agent"] == "ua"
