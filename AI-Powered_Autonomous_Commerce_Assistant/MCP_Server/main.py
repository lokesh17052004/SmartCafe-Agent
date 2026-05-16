from fastmcp import FastMCP
from contextlib import asynccontextmanager
from src.router.mcp_router import router
from src.migrations .migration import run_migration_and_seed

@asynccontextmanager
async def lifespan(mcp: FastMCP):
    print("Starting Bean & Brew Agent API...")
    run_migration_and_seed()
    yield
    print("Shutting down Bean & Brew Agent API...")

mcp = FastMCP("Bean and Brew Sever",lifespan=lifespan)
mcp.mount(router)

if __name__ == "__main__":
        mcp.run(transport="streamable-http",host = "127.0.0.1",port = 8001)
