import subprocess
from pathlib import Path
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("pytest_gen")


@mcp.tool()
def check_coverage(
        project_path: Annotated[str, Field(description="Location of the project to measure test coverage")]
) -> Annotated[bool, Field(description="Test Coverage Passed")]:
    """
    Measure the test coverage of a project in a given path and return True if it exceeds 90%, False if the coverage is insufficient
    """

    subprocess.run(["pytest", "--cov=.", "--cov-report=term-missing"], cwd=project_path, check=True)

    result = subprocess.run(["coverage", "report"], cwd=project_path, text=True, capture_output=True)
    for line in result.stdout.splitlines():
        if line.startswith('TOTAL'):
            coverage_percentage = float(line.split()[-1][:-1])
            return coverage_percentage > 90
    return False


@mcp.tool()
def write_file(
        file_path: Annotated[str, Field(description="file storage location (including file name")],
        file_text: Annotated[str, Field(description="file text content")],
) -> None:
    """
    write a file on a given path
    """
    Path(file_path).write_text(file_text, encoding="utf-8")


@mcp.tool()
def read_file(
        file_path: Annotated[str, Field(description="file location (including file name")],
) -> Annotated[str, Field(description="file text content")]:
    """
    Gets the file text content of the given path
    """
    return Path(file_path).read_text(encoding="utf-8")


if __name__ == "__main__":
    mcp.run(transport="stdio")
