"""Local PoC for passing hidden metadata between custom tools."""

from textwrap import dedent

from dotenv import load_dotenv

from glaip_sdk.agents import Agent

from tools import LoadCaseFileTool, RevealVerificationCodeTool

load_dotenv(override=True)

agent = Agent(
    name="tool_state_handoff_local",
    instruction=dedent(
        """
        You are a case-review assistant.

        Always call `load_case_file` first.
        Read the public notes from that tool result, decide one short summary,
        then call `reveal_verification_code` with only your summary.
        Do not paste the public notes into the second tool call. That tool reads the
        shared state from metadata by itself.
        There is also a hidden verification code stored in metadata by the first tool.
        You cannot see that code until the second tool reveals it.
        In the final answer, include your summary and the revealed verification code.
        """
    ).strip(),
    tools=[LoadCaseFileTool, RevealVerificationCodeTool],
    model="openai/gpt-5-mini",
)

agent.run(
    "Load the checkout_delay case, summarize the issue, then reveal the verification code.", export=True
)
