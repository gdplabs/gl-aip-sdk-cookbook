"""Interactive BOSA MCP setup and demonstration script.

This script provides an interactive way to set up BOSA (Business Operations &
Service Automation) credentials, configure GitHub integration, and demonstrate
MCP (Model Control Protocol) tool execution using GLLM Tools as the MCP client.

The script handles:
- Interactive BOSA Client Key setup
- User token configuration
- GitHub integration verification and setup
- MCP session initialization and tool execution

If you already have all credentials configured, you can use `uv run example_all_setup.py` instead.

Authors:
    Samuel Lusandi (samuel.lusandi@gdplabs.id)
"""

import asyncio
import os
from typing import cast
import time

from bosa_connectors import BosaConnector
from dotenv import load_dotenv

from mcp import ClientSession
from gllm_tools.mcp.client.session import create_session

from utilities import launch_console_browser, update_env_file

load_dotenv()


def setup_bosa_client_key(bosa_api_url: str) -> str:
    console_url = f"{bosa_api_url}/console"
    
    print("🔑 BOSA_CLIENT_KEY is not set!")
    print(f"📖 Opening browser to: {console_url}")
    print("Please retrieve your Client Key from the console.")
    
    if not launch_console_browser(console_url):
        print("⚠️ Could not open a browser automatically. Please open the URL manually.")
        print(console_url)

    while True:
        client_key = input("\n🔑 Please enter your BOSA_CLIENT_KEY: ").strip()
        if client_key:
            update_env_file("BOSA_CLIENT_KEY", client_key)
            # Reload environment variables
            load_dotenv(override=True)
            return client_key
        else:
            print("❌ Client key cannot be empty. Please try again.")


def setup_bosa_token(bosa_api_url: str) -> str:
    print("\n🎫 Now we need to set up your BOSA_TOKEN (User Token)!")
    print(f"Retrieve your User Token from the same place where you retrieved your Client Key ({bosa_api_url}/console).")

    while True:
        token = input("\n🎫 Please enter your BOSA_TOKEN: ").strip()
        if token:
            update_env_file("BOSA_TOKEN", token)
            load_dotenv(override=True)
            return token
        else:
            print("❌ Token cannot be empty. Please try again.")


async def main():
    bosa_api_url = os.getenv("BOSA_API_URL") or "https://api.bosa.id"
    bosa_client_key = os.getenv("BOSA_CLIENT_KEY")
    bosa_token = os.getenv("BOSA_TOKEN")

    if not bosa_client_key:
        bosa_client_key = setup_bosa_client_key(bosa_api_url)

    if not bosa_token:
        bosa_token = setup_bosa_token(bosa_api_url)

    print(f"\n✅ All credentials are set up!")
    print(f"🔗 API URL: {bosa_api_url}")
    print(f"🔑 Client Key: {bosa_client_key[:10]}...")
    print(f"🎫 Token: {bosa_token[:10]}...")
    print("🚀 BOSA connector initialized successfully!")

    bosa_connector = BosaConnector(
        api_base_url=bosa_api_url,
        api_key=bosa_client_key,
    )

    print("🔍 Getting user information...")
    try:
        user_info = bosa_connector.get_user_info(bosa_token)
        print(f"✅ User ID: {user_info.id}")
        print(f"✅ Identifier: {user_info.identifier}")
        print(f"✅ Integrations: {user_info.integrations}")
    except Exception as e:
        print(f"❌ Error getting user info: {e}")
        print("Please check your BOSA_TOKEN and try again.")
        return

    print("🔍 Checking GitHub integration...")
    try:
        user_has_github_integration = bosa_connector.user_has_integration("github", bosa_token)
        if user_has_github_integration:
            print("✅ GitHub integration is active")
        else:
            print("⚠️ GitHub integration not found")
    except Exception as e:
        print(f"❌ Error checking GitHub integration: {e}")
        return

    if not user_has_github_integration:
        print("🔗 Setting up GitHub integration...")
        try:
            create_github_integration = bosa_connector.initiate_connector_auth("github", bosa_token, "http://localhost:8000")
            print("📖 Opening GitHub authorization page in your browser...")
            
            if not launch_console_browser(create_github_integration):
                print("⚠️ Could not open browser automatically. Please open this URL manually:")
                print(create_github_integration)
            
            print("⏳ Waiting for GitHub integration to complete...")
            print("   (Please complete the authorization in your browser)")
            
            max_retries = 60  # Wait up to 60 seconds
            retry_count = 0
            
            while retry_count < max_retries:
                try:
                    user_has_github_integration = bosa_connector.user_has_integration("github", bosa_token)
                    if user_has_github_integration:
                        print("✅ GitHub integration completed successfully!")
                        break
                    else:
                        retry_count += 1
                        if retry_count % 10 == 0:  # Show progress every 10 seconds
                            print(f"   Still waiting... ({retry_count}/{max_retries}s)")
                        time.sleep(1)
                except Exception as e:
                    print(f"❌ Error checking integration status: {e}")
                    return
            
            if retry_count >= max_retries:
                print("❌ GitHub integration setup timed out. Please try again.")
                return
                
        except Exception as e:
            print(f"❌ Error setting up GitHub integration: {e}")
            return
    
    print("🔍 Connecting to BOSA Github MCP...")
    bosa_configuration = {
        "transport": "streamable_http",
        "url": f"{bosa_api_url}/github/mcp",
        "headers": {
            "Authorization": f"Bearer {bosa_token}",
            "X-Api-Key": bosa_client_key,
        }
    }
    print("🔍 Executing GitHub 'Get Issue' tool...")
    try:
        async with create_session(bosa_configuration) as session:
            await session.initialize()
            
            print("\n📝 Please provide GitHub repository details:")
            try:
                owner = input("  Repository owner (e.g., 'octocat'): ").strip()
                repo = input("  Repository name (e.g., 'Hello-World'): ").strip()
                issue_number_str = input("  Issue number (e.g., '1'): ").strip()
                
                if not owner or not repo or not issue_number_str:
                    print("❌ All fields are required. Please try again.")
                    return
                
                issue_number = int(issue_number_str)
                if issue_number <= 0:
                    print("❌ Issue number must be a positive integer.")
                    return
                    
            except ValueError:
                print("❌ Invalid issue number. Please enter a valid integer.")
                return
            except KeyboardInterrupt:
                print("\n❌ Operation cancelled by user.")
                return
            
            tool_name = "github_get_issue_handler"
            params = {
                "owner": owner,
                "repo": repo,
                "issue_number": issue_number,
            }
            request = {"request": params}

            print(f"\n🚀 Calling tool '{tool_name}' with params: {params}")
            call_tool_result = await cast(ClientSession, session).call_tool(tool_name, request)

            print("\n✅ Tool execution completed successfully!")
            print("📋 Result:")
            print(call_tool_result)
            
    except Exception as e:
        print(f"❌ Error executing MCP tool: {e}")
        print("Please check your network connection and try again.")


if __name__ == "__main__":
    asyncio.run(main())
