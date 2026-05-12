import os

from dotenv import load_dotenv

from gl_connectors_sdk import GLConnectors

load_dotenv()

connector = GLConnectors(api_base_url="https://connectors.glair.ai")
data, status = connector.execute(
    "github",
    "list_issues",
    token=os.getenv("GL_CONNECTORS_USER_TOKEN"),
    input_={"owner": "github", "repo": "awesome-copilot", "per_page": 1},
)
print(status)
print(data)
