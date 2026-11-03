"""Optional standalone GitHub Copilot SDK example.

This file is not part of the Database Design Agent execution pipeline.
Requires Python 3.11+, github-copilot-sdk, and authorized GitHub Copilot access.
"""

import asyncio


async def main():
    """Ask Copilot for an explanation of 3NF; do not execute model-generated code."""
    try:
        from copilot import CopilotClient
    except ImportError as exc:
        raise SystemExit(
            "Install github-copilot-sdk in a Python 3.11+ virtual environment first."
        ) from exc

    # Do not grant automatic file/system tool permissions for this teaching example.
    async with CopilotClient() as client:
        session = await client.create_session(available_tools=[])
        response = await session.send_and_wait(
            "Explain Third Normal Form in database design. "
            "Give one small example with functional dependencies and candidate keys. "
            "Do not claim that an unverified decomposition is correct."
        )
        if response is None:
            print("Copilot returned no assistant message.")
        else:
            print(response.data.content or "(Empty response)")


if __name__ == "__main__":
    asyncio.run(main())
