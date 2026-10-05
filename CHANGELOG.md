# Changelog

## [0.2.0] - 2026-10-05

### Added
- `fetch_description` on `search_jobs` (all sites, python-jobspy 1.2.0)
- `linkedin_company_ids`, `enforce_annual_salary`, `user_agent` on `search_jobs`
- `"plain"` for `description_format`

### Changed
- Require `python-jobspy>=1.2.0,<1.3.0`
- `linkedin_fetch_description` is now a deprecated alias for `fetch_description`

### Fixed
- Re-pin `mcp<2` (dependabot had widened it to `<3`, which breaks `uvx jobspy-mcp` again)

## [0.1.1] - 2026-08-17

### Fixed
- Pin `mcp<2`: mcp 2.0 moved `mcp.server.fastmcp`, which broke `uvx jobspy-mcp`

## [0.1.0] - 2026-04-21

### Added
- Initial release
- `search_jobs` tool exposing all JobSpy search parameters
- `list_job_sites` tool listing all supported job boards
- Published to PyPI as `jobspy-mcp`
- GitHub Actions CI (test matrix Python 3.10–3.13) and PyPI publish via OIDC
- Dependabot for automatic python-jobspy version tracking
