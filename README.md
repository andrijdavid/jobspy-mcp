# jobspy-mcp

MCP server wrapping [JobSpy](https://github.com/speedyapply/JobSpy) to search LinkedIn, Indeed, Glassdoor, ZipRecruiter, Google Jobs, Bayt, Naukri, and BDJobs from any MCP-compatible AI client.

## Quick Start

Run directly with `uvx` (stdio, default):

```bash
uvx jobspy-mcp
```

Or with SSE / HTTP transports:

```bash
uvx jobspy-mcp --transport sse                        # SSE on 127.0.0.1:8000
uvx jobspy-mcp --transport streamable-http            # HTTP on 127.0.0.1:8000
uvx jobspy-mcp --transport sse --host 0.0.0.0 --port 9000
```

Or install globally:

```bash
pip install jobspy-mcp
jobspy-mcp
```

### CLI Options

| Flag | Default | Description |
|------|---------|-------------|
| `--transport` | `stdio` | `stdio`, `sse`, or `streamable-http` |
| `--host` | `127.0.0.1` | Bind host (SSE/HTTP only) |
| `--port` | `8000` | Bind port (SSE/HTTP only) |

## Claude Desktop Configuration

Add to `~/.config/claude/claude_desktop_config.json` (Linux/macOS):

```json
{
  "mcpServers": {
    "jobspy": {
      "command": "uvx",
      "args": ["jobspy-mcp"]
    }
  }
}
```

On Windows: `%APPDATA%\Claude\claude_desktop_config.json`

## Available Tools

| Tool | Description |
|------|-------------|
| `list_job_sites` | Returns all supported site names with notes |
| `search_jobs` | Search jobs with full parameter control |

### `search_jobs` Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `site_name` | list[str] | `["linkedin","indeed"]` | Job boards to search |
| `search_term` | str | None | Job title or keywords |
| `google_search_term` | str | None | Search term for Google Jobs specifically |
| `location` | str | None | City, state, or country |
| `results_wanted` | int | 15 | Results per site |
| `hours_old` | int | None | Filter by recency (hours) |
| `job_type` | str | None | fulltime, parttime, internship, contract |
| `is_remote` | bool | False | Remote jobs only |
| `distance` | int | 50 | Search radius in miles |
| `country_indeed` | str | "usa" | Country for Indeed/Glassdoor |
| `easy_apply` | bool | None | Easy Apply filter |
| `linkedin_fetch_description` | bool | False | Fetch full LinkedIn descriptions |
| `offset` | int | 0 | Pagination offset |
| `description_format` | str | "markdown" | "markdown" or "html" |
| `proxies` | list[str] | None | Proxy URLs for rate limit avoidance |

### Supported Sites

| Site | Notes |
|------|-------|
| `linkedin` | Global; proxies recommended for large searches |
| `indeed` | Best scraper; use `country_indeed` for non-US |
| `glassdoor` | Use `country_indeed` for non-US |
| `zip_recruiter` | US and Canada only |
| `google` | Use `google_search_term` for best results |
| `bayt` | Middle East focused |
| `naukri` | India focused |
| `bdjobs` | Bangladesh focused |

## Development

```bash
git clone https://github.com/andrijdavid/jobspy-mcp
cd jobspy-mcp
uv sync --dev
uv run pytest
uv run jobspy-mcp   # starts MCP server on stdio
```