from dotenv import load_dotenv
import asyncio
import os

from glaip_sdk import Agent
from gllm_tools.mcp.client.langchain import LangchainMCPClient

load_dotenv()

DESIRED_TOOLS = {"google_mail_send_email"} # Send an email with the specified content, recipient, and subject

client = LangchainMCPClient({
    "google_mail": {
        "url": f"{os.getenv('GL_CONNECTORS_URL')}/google_mail/mcp",
        "headers": {"Authorization": f"Bearer {os.getenv('GL_CONNECTORS_USER_TOKEN')}"},
    }
})

EMAIL_SUBJECT = "Updated Team Schedule: [Week/Month] [Date Range]"
EMAIL_RECIPIENTS = ["example@gmail.com", "example2@gmail.com"]
EMAIL_MESSAGE = """
THIS IS A TEST EMAIL. PLEASE IGNORE.
Hi Team,\n\n

I hope you’re all having a great week.\n\n

To keep everyone on the same page and ensure our projects stay on track, I’ve outlined the schedule for the upcoming period below. Please take a moment to review your specific shifts, meeting times, and deadlines.\n\n

**Weekly Highlights**
- [Date]: [Key Event, e.g., All-Hands Meeting at 10:00 AM]
- [Date]: [Project Milestone/Deadline]
- [Date]: [Team Lunch / Social Hour]\n\n

**Action Items**
1. **Confirm Availability**: Please let me know by [Time/Day] if there are any conflicts with the times listed above.
2. **Sync Calendars**: Ensure your shared calendars are updated with any planned PTO or out-of-office blocks.
3. **Preparation**: [Optional: Note any documents or tasks that need to be completed before a specific meeting].\n\n

You can find the full, live version of the schedule here: **[Link to Spreadsheet/Calendar]**\n\n

If you have any questions or need to request a shift swap, please reach out to me directly. Thanks for all your hard work!\n\n

Best regards,\n\n

[Your Name]
[Your Title]\n
"""

def extract_content(chunk) -> str | None:
    if isinstance(chunk, str):
        return chunk
    if isinstance(chunk, dict):
        return chunk.get("content")
    return getattr(chunk, "content", None)


async def main():
    all_tools = await client.get_tools("google_mail")
    tools = [t for t in all_tools if t.name in DESIRED_TOOLS]

    agent = Agent(
        name="gmail_agent",
        instruction="You are a helpful assistant.",
        tools=tools,
        model="gpt-4.1",
    )

    prompt = (
        "Create a new draft. "
        f"The recipient email address is/are {EMAIL_RECIPIENTS}. "
        f"The subject should be {EMAIL_SUBJECT}. "
        f"The body of email should contains this message: {EMAIL_MESSAGE}. "
        "The \n character in the body message should be preserved as entered above. "
        "The **text surrounded by double asterisks** should be bolded in the email body. "
        "After that, you need to send it immediately. "
    )

    async for chunk in agent.arun(prompt):
        if content := extract_content(chunk):
            print(content)


if __name__ == "__main__":
    asyncio.run(main())
    