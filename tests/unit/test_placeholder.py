"""Placeholder test — verifies the project skeleton is functional.

This test exists to satisfy M0 acceptance: `make test` passes, and the test can fail.
Real tests will be added alongside each milestone's implementation.
"""

from typer.testing import CliRunner

from evalgate import __version__
from evalgate.cli import app

runner = CliRunner()


def test_version_exists() -> None:
    """Test that the package version is set."""
    assert __version__ is not None
    assert isinstance(__version__, str)
    assert __version__ == "0.1.0"


def test_cli_help() -> None:
    """Test that the CLI can be invoked and returns help text."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Statistically honest regression gate" in result.stdout


def test_cli_version() -> None:
    """Test that the CLI returns the correct version."""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.stdout
