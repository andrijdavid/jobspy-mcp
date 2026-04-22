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
