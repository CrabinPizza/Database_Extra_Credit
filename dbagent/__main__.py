"""Allow running the package with `python -m dbagent`."""

from .cli import main
# Delegate argument parsing and file generation to the CLI module.
main()
