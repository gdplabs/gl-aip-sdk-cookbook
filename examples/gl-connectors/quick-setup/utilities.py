"""Utility functions for the BOSA MCP GLLM Tools Cookbook.

This module provides helper functions for environment variable management
and cross-platform browser launching capabilities.

Authors:
    Samuel Lusandi (samuel.lusandi@gdplabs.id)
"""

import os
import subprocess
import sys
import webbrowser
from pathlib import Path

def update_env_file(key: str, value: str) -> None:
    """Update or create .env file with the given key-value pair.
    
    This function safely updates environment variables in a .env file,
    preserving existing content and adding new variables as needed.
    
    Args:
        key (str): Environment variable name to set.
        value (str): Environment variable value to assign.
        
    Raises:
        IOError: If the .env file cannot be read or written.
    """
    env_file = Path(".env")
    
    # Read existing content if file exists
    existing_lines = []
    if env_file.exists():
        with open(env_file, "r") as f:
            existing_lines = f.readlines()
    
    # Check if key already exists and update it
    key_found = False
    for i, line in enumerate(existing_lines):
        if line.strip().startswith(f"{key}="):
            existing_lines[i] = f"{key}={value}\n"
            key_found = True
            break
    
    # If key doesn't exist, add it
    if not key_found:
        existing_lines.append(f"{key}={value}\n")
    
    # Write back to file
    with open(env_file, "w") as f:
        f.writelines(existing_lines)
    
    print(f"✅ Updated .env file with {key}")


def launch_console_browser(url: str) -> bool:
    """Attempt to open a URL in the default browser across different platforms.
    
    This function tries multiple methods to open a URL in the user's default
    browser, with fallbacks for different operating systems and execution contexts.
    It's particularly useful in sandboxed environments where standard browser
    launching might fail.
    
    Args:
        url (str): The URL to open in the browser.
        
    Returns:
        bool: True if the URL was successfully opened, False otherwise.
        
    Note:
        The function attempts webbrowser.open() first, then falls back to
        platform-specific command-line tools (open on macOS, xdg-open on Linux,
        start on Windows).
    """
    # webbrowser prefers Apple Events; that can fail inside sandboxed shells.
    if webbrowser.open(url, new=1, autoraise=True):
        return True
    
    # Fallback: call platform-specific openers directly.
    commands = []
    if sys.platform == "darwin":
        commands.append(["open", url])
    elif sys.platform.startswith("linux"):
        commands.extend([["xdg-open", url], ["gio", "open", url]])
    elif os.name == "nt":
        commands.append(["cmd", "/c", "start", "", url])
    
    for cmd in commands:
        try:
            subprocess.run(cmd, check=True)
            return True
        except FileNotFoundError:
            continue
        except subprocess.CalledProcessError:
            continue
    
    return False