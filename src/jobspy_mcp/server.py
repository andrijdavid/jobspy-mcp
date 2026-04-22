from __future__ import annotations

import asyncio
from typing import Annotated, Optional

from mcp.server.fastmcp import FastMCP

from jobspy_mcp.serializer import dataframe_to_json_records

mcp = FastMCP(
    name="jobspy-mcp",
    instructions=(
        "Search for jobs across LinkedIn, Indeed, Glassdoor, ZipRecruiter, "
        "Google, Bayt, Naukri, and BDJobs. Use search_jobs to query job boards "
        "and list_job_sites to see available sources."
    ),
)


@mcp.tool(
    name="list_job_sites",
    description=(
        "Returns the list of job board site names that can be passed to search_jobs. "
        "Call this first if you are unsure which sites to target."
    ),
)
def list_job_sites() -> dict:
    """List all supported job board sites."""
    return {
        "sites": [
            "linkedin",
            "indeed",
            "zip_recruiter",
            "glassdoor",
            "google",
            "bayt",
            "naukri",
            "bdjobs",
        ],
        "notes": {
            "zip_recruiter": "US and Canada only",
            "glassdoor": "Requires country_indeed parameter for non-US searches",
            "indeed": "Requires country_indeed parameter for non-US searches",
            "bayt": "Middle East focused",
            "naukri": "India focused",
            "bdjobs": "Bangladesh focused",
            "linkedin": "Rate limiting applies; proxies recommended for large searches",
        },
    }


@mcp.tool(
    name="search_jobs",
    description=(
        "Search for jobs across one or more job boards using JobSpy. "
        "Returns a list of job postings with title, company, location, salary, "
        "description, and direct URL. "
        "At least search_term or location should be provided for useful results."
    ),
)
async def search_jobs(
    site_name: Annotated[
        list[str],
        "Job board(s) to search. Use list_job_sites for valid values. "
        "Default searches LinkedIn and Indeed.",
    ] = ["linkedin", "indeed"],
    search_term: Annotated[
        Optional[str],
        "Job title or keywords to search for, e.g. 'software engineer'.",
    ] = None,
    google_search_term: Annotated[
        Optional[str],
        "Search term specifically for Google Jobs (overrides search_term for Google).",
    ] = None,
    location: Annotated[
        Optional[str],
        "City, state, or country to search in, e.g. 'San Francisco, CA'.",
    ] = None,
    results_wanted: Annotated[
        int,
        "Number of results to return per site (default 15).",
    ] = 15,
    hours_old: Annotated[
        Optional[int],
        "Filter to jobs posted within this many hours. None means no filter. "
        "Note: cannot combine with job_type or easy_apply on Indeed.",
    ] = None,
    job_type: Annotated[
        Optional[str],
        "One of: fulltime, parttime, internship, contract. None means all types.",
    ] = None,
    is_remote: Annotated[
        bool,
        "If True, filter for remote jobs only.",
    ] = False,
    distance: Annotated[
        int,
        "Search radius in miles from the specified location (default 50).",
    ] = 50,
    country_indeed: Annotated[
        str,
        "Country for Indeed and Glassdoor searches (default 'usa'). "
        "Examples: 'uk', 'canada', 'australia', 'india'.",
    ] = "usa",
    easy_apply: Annotated[
        Optional[bool],
        "If True, filter for Easy Apply / Quick Apply jobs only (LinkedIn/Indeed). "
        "Note: cannot combine with hours_old on LinkedIn.",
    ] = None,
    linkedin_fetch_description: Annotated[
        bool,
        "If True, fetch full job descriptions from LinkedIn (slower, more requests).",
    ] = False,
    offset: Annotated[
        int,
        "Pagination offset — skip this many results before returning.",
    ] = 0,
    description_format: Annotated[
        str,
        "Format for job descriptions: 'markdown' or 'html'.",
    ] = "markdown",
    proxies: Annotated[
        Optional[list[str]],
        "List of proxy URLs to rotate through, e.g. ['http://user:pass@host:port']. "
        "Recommended for LinkedIn to avoid rate limiting.",
    ] = None,
) -> dict:
    """Search jobs across multiple job boards."""
    kwargs: dict = {
        "site_name": site_name,
        "search_term": search_term,
        "google_search_term": google_search_term,
        "location": location,
        "results_wanted": results_wanted,
        "hours_old": hours_old,
        "job_type": job_type,
        "is_remote": is_remote,
        "distance": distance,
        "country_indeed": country_indeed,
        "easy_apply": easy_apply,
        "linkedin_fetch_description": linkedin_fetch_description,
        "offset": offset,
        "description_format": description_format,
        "proxies": proxies,
        "verbose": 0,
    }

    try:
        loop = asyncio.get_event_loop()
        df = await loop.run_in_executor(None, _run_scrape, kwargs)
        records = dataframe_to_json_records(df)
        return {"total": len(records), "jobs": records}
    except Exception as exc:
        return {
            "error": type(exc).__name__,
            "message": str(exc),
            "total": 0,
            "jobs": [],
        }


def _run_scrape(kwargs: dict):
    from jobspy import scrape_jobs

    # Strip None values so JobSpy applies its own defaults
    clean_kwargs = {k: v for k, v in kwargs.items() if v is not None}
    return scrape_jobs(**clean_kwargs)
