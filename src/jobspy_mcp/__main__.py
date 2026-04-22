import argparse

from jobspy_mcp.server import mcp


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="jobspy-mcp",
        description="JobSpy MCP server",
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
        help="Transport to use (default: stdio)",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind for SSE/HTTP transports (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind for SSE/HTTP transports (default: 8000)",
    )

    args = parser.parse_args()

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.settings.host = args.host
        mcp.settings.port = args.port
        mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
