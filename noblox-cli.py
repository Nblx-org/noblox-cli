#!/usr/bin/env python3
import argparse
import json
import os
import requests
import sys
import time
from typing import Optional

try:
    from rich.console import Console
    from rich.progress import Progress
except ImportError:
    print("Please install rich: pip install rich")
    sys.exit(1)

def get_figlet_header(text: str) -> str:
    try:
        import subprocess
        result = subprocess.run(['figlet', '-f', 'slant', text], capture_output=True, text=True, check=True)
        return result.stdout
    except FileNotFoundError:
        return f"  {text}  "
    except subprocess.CalledProcessError as e:
        return f"Error generating figlet: {e}"

def getenv(api_url: str, output_file: str, console: Console, progress: Optional[Progress] = None):
    try:
        if progress:
            task_id = progress.add_task("[cyan]Fetching environment variables...", total=100)
        else:
            print("Fetching environment variables...")

        response = requests.get(api_url, stream=True)
        response.raise_for_status()

        if progress:
            for chunk in response.iter_content(chunk_size=8192):
                progress.update(task_id, advance=0.1)
                time.sleep(0.005)
            progress.update(task_id, completed=True)

        data = json.loads(response.text)

        with open(output_file, 'w') as f:
            for key, value in data.items():
                f.write(f'{key}={value}\n')

        console.print(f"[green]Successfully wrote environment variables to {output_file}[/]")

    except requests.exceptions.RequestException as e:
        console.print(f"[red]API request failed: {e}[/]")
    except json.JSONDecodeError:
        console.print("[red]Failed to decode JSON response.[/]")
    except Exception as e:
        console.print(f"[red]An unexpected error occurred: {e}[/]")


if __name__ == '__main__':
    console = Console()
    grid = """
┌──┬──┐                
│  │  │
├──┼──┤
│  │  │
└──┴──┘
"""
    grid_lines = grid.strip().split('\n')
    header = get_figlet_header("noblox")
    header_lines = header.strip().split('\n')
    combined_lines = []
    for i in range(max(len(grid_lines), len(header_lines))):
        grid_line = grid_lines[i % len(grid_lines)]
        header_line = header_lines[i] if i < len(header_lines) else ""
        combined_lines.append(f"{grid_line} {header_line}")
    combined_output = "\n".join(combined_lines)
    console.print(f"[yellow]{combined_output}[/]")

    parser = argparse.ArgumentParser(description='noblox CLI tool.')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # getenv command
    getenv_parser = subparsers.add_parser('getenv', help='Fetch environment variables and populate .env file')
    getenv_parser.add_argument('--output', default='.env', help='The output file name (default: .env).')

    # request command
    request_parser = subparsers.add_parser('request', help='Request API keys from fly.io or together.ai')
    request_parser.add_argument('provider', choices=['fly.io', 'together.ai'], help='API key provider (fly.io or together.ai)')

    # update command
    update_parser = subparsers.add_parser('update', help='Check for updated API keys')

    # share command
    share_parser = subparsers.add_parser('share', help='Share a restricted set of environment variables')
    
    # login command
    login_parser = subparsers.add_parser('login', help='Login with an API key')
    login_parser.add_argument('api_key', help='Your API key')

    args = parser.parse_args()

    if args.command == 'getenv':
        api_url = "localhost:5000/respond"
        with Progress(transient=True) as progress:
            getenv(api_url, args.output, console, progress)
    elif args.command == 'request':
        request_api_keys(args.provider, console)
    elif args.command == 'update':
        update_api_keys(console)
    elif args.command == 'share':
        share_environment_variables(console)
    elif args.command == 'login':
        login_api_key(args.api_key, console)
    else:
        parser.print_help()

def request_api_keys(provider: str, console: Console):
    """Requests API keys from a provider."""
    console.print(f"[yellow]Requesting API keys from {provider}...[/]")
    # TODO: Implement API key request logic
    console.print("[red]Not yet implemented.[/]")

def update_api_keys(console: Console):
    """Checks for updated API keys."""
    console.print("[yellow]Checking for updated API keys...[/]")
    # TODO: Implement update logic
    console.print("[red]Not yet implemented.[/]")

def share_environment_variables(console: Console):
    """Shares a restricted set of environment variables."""
    console.print("[yellow]Sharing environment variables...[/]")
    # TODO: Implement share logic
    console.print("[red]Not yet implemented.[/]")

def login_api_key(api_key: str, console: Console):
    """Logs in with the provided API key."""
    console.print(f"[yellow]Logging in with API key: {api_key}...[/]")
    try:
        response = requests.post("http://localhost:5000/requests", json={"api_key": api_key})
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        console.print(f"[green]Login successful: {data}[/]")
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Login failed: {e}[/]")
    except json.JSONDecodeError:
        console.print("[red]Failed to decode JSON response.[/]")