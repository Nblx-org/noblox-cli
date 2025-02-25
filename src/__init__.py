#!/usr/bin/env python3
import argparse
import json
import os
import requests
import sys
import time
import base64
import subprocess
from cryptography.fernet import Fernet
from typing import Optional

from git import Repo, InvalidGitRepositoryError
from git.exc import GitCommandError
from dotenv import set_key
from rich.console import Console
from rich.progress import Progress

NOBLOX_DIR = ".nblx"
SECRET_FILE = f"{NOBLOX_DIR}/secret.key"
ENCRYPTED_ENV = f"{NOBLOX_DIR}/env.enc"

_project = Repo('.')
_nblx = Repo('.nblx')

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

        for key, value in data.items():
            set_key(output_file, key, value)

        console.print(f"[green]Successfully wrote environment variables to {output_file}[/]")

    except requests.exceptions.RequestException as e:
        console.print(f"[red]API request failed: {e}[/]")
    except json.JSONDecodeError:
        console.print("[red]Failed to decode JSON response.[/]")
    except Exception as e:
        console.print(f"[red]An unexpected error occurred: {e}[/]")



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
        import os


def generate_key():
    key = Fernet.generate_key()
    with open(SECRET_FILE, "wb") as key_file:
        key_file.write(key)
    return key


def load_key():
    if os.path.exists(SECRET_FILE):
        with open(SECRET_FILE, "rb") as key_file:
            return key_file.read()
    return generate_key()

def install_git_hooks():
    """
    🚀 This repo uses **nblx** to securely manage secrets. 🚀  

    You just tried to commit `XXX`, but **You Don't Need To Do That!**  
    Nblx automatically encrypts and tracks secrets for you.  

    📖 Learn why:  `nblx hello`  
    🔕 Silence this warning:  `nblx bye`  
    (One-time override: `git commit --no-verify`)  
    (Permanent removal: `nblx bye --forever`)  
    """
    """Installs git hooks."""
    try:
        repo = Repo(search_parent_directories=True)
        hook_path = os.path.join(repo.git_dir, 'hooks', 'pre-commit')
        with open(hook_path, 'w') as f:
            f.write("#!/bin/sh\n")
            f.write("# Add your pre-commit hook logic here\n")
            f.write("echo 'Running pre-commit hook...'\n")
            f.write("if [[ $1 == *.env ]]; then\n")
            f.write("  echo 'Skipping .env file'\n")
            f.write("else\n")
            f.write("  # Example: Run linters or formatters\n")
            f.write("  # black . || exit 1\n")
            f.write("  # flake8 . || exit 1\n")
            f.write("fi\n")
        os.chmod(hook_path, 0o755)  # Make the hook executable
        print("Git pre-commit hook installed.")
    except InvalidGitRepositoryError:
        print("Not a git repository.")
    except Exception as e:
        print(f"Error installing git hook: {e}")
        print(f"Error installing git hook: {e}")


def change_branch(branch_name: str):
    """Changes to the specified branch."""
    try:
        repo = Repo(search_parent_directories=True)
        repo.git.checkout(branch_name)
        print(f"Switched to branch: {branch_name}")
    except InvalidGitRepositoryError:
        print("Not a git repository.")
    except GitCommandError as e:
        print(f"Error changing branch: {e}")
    except Exception as e:
        print(f"Error changing branch: {e}")


def checkout_and_commit(file_path: str, commit_message: str):
    """Checks out a file, adds it, and commits the changes."""
    try:
        repo = Repo(search_parent_directories=True)
        repo.git.checkout(file_path)  # Checkout the file
        repo.index.add([file_path])  # Add the file
        repo.index.commit(commit_message)  # Commit the changes
        print(f"Checked out, added, and committed changes to {file_path}")
    except InvalidGitRepositoryError:
        print("Not a git repository.")
    except GitCommandError as e:
        print(f"Error during checkout/commit: {e}")
    except Exception as e:
        print(f"Error during checkout/commit: {e}")


def encrypt_env():
    if not os.path.exists(".env"):
        print("No .env file found.")
        return
    
    key = load_key()
    cipher = Fernet(key)
    
    with open(".env", "rb") as env_file:
        encrypted_data = cipher.encrypt(env_file.read())
    
    with open(ENCRYPTED_ENV, "wb") as enc_file:
        enc_file.write(encrypted_data)
    
    print(".env encrypted and stored in .noblox/env.enc")


def decrypt_env():
    if not os.path.exists(ENCRYPTED_ENV):
        print("No encrypted .env found.")
        return
    
    key = load_key()
    cipher = Fernet(key)
    
    with open(ENCRYPTED_ENV, "rb") as enc_file:
        decrypted_data = cipher.decrypt(enc_file.read())
    
    with open(".env", "wb") as env_file:
        env_file.write(decrypted_data)
    
    print("Decrypted .env file restored.")


def init_noblox():
    global _nblx 
    if not os.path.exists(NOBLOX_DIR):
        os.mkdir(NOBLOX_DIR)
        _nblx = Repo(NOBLOX_DIR)
        if not _project.ignored(NOBLOX_DIR):
            with open('.gitignore', 'a') as gitignore:
                gitignore.write(NOBLOX_DIR)
        print("Noblox initialized. .noblox/ added to .gitignore.")
    else:
        print("Noblox already initialized.")

if __name__ == '__main__':
    console = Console()
    grid = """
                     _     _           
         _ __   ___ | |__ | | _____  __
┌──┬### | '_ \ / _ \| '_ \| |/ _ \ \/ /
├──┼### | | | | (_) | |_) | | (_) >  < 
└──┴──┘ |_| |_|\___/|_.__/|_|\___/_/\_\
"""
    console.print(f"[yellow]{grid}[/]")

    parser = argparse.ArgumentParser(description='noblox CLI tool.')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Todo: things like api keys should maybe be in a chroot or something to keep their permissions isolated to the project
    # I think maybe the direnv abstraction does this
    # Git commands
    log_parser = subparsers.add_parser('log', help='Log of previous changes and checkpoints')
    init_parser = subparsers.add_parser('init', help=f'Create the {NOBLOX_DIR} and try to get permissions for the .env directory')
    pull_parser = subparsers.add_parser('pull', help='Update permissions')
    push_parser = subparsers.add_parser('push', help='Push (revertable) updates to permissions')
    checkout_parser = subparsers.add_parser('checkout', help='Switch permissions between environments')
    fork = subparsers.add_parser('fork', help='Clone the current permissions and (potentially) remove or add users')

    # Custom commands
    reject_parser = subparsers.add_parser('reject', help='Reject an email')
    reject_parser.add_argument('email', help='The email to reject')

    invite_parser = subparsers.add_parser('invite', help='Invite a new team member')
    invite_parser.add_argument('email', help='The email to invite')

    # getenv command
    getenv_parser = subparsers.add_parser('init', help='Fetch environment variables and populate .env file')
    getenv_parser.add_argument('--output', default='.env', help='The output file name (default: .env).')

    request_parser = subparsers.add_parser('request', help='Request API keys for cli utils')
    update_parser = subparsers.add_parser('update', help='Check for updated secrets')

    # login command
    login_parser = subparsers.add_parser('login', help='Login with an API key')
    login_parser.add_argument('api_key', help='Your API key')

    args = parser.parse_args()

    if args.command == 'init:
        api_url = "localhost:5000/respond"
        with Progress(transient=True) as progress:
            getenv(api_url, args.output, console, progress)

    if args.command == 'log':
        print(_nblx.git.log())
    elif args.command == 'init':
        init_noblox()
    elif args.command == 'pull':
        _nblx.remotes.origin.pull()
    elif args.command == 'push':
        _nblx.remotes.origin.push()
    elif args.command == 'checkout':
        _nblx.git.checkout()
    elif args.command == 'reject':
        print(f"Rejecting email: {args.email}")
    elif args.command == 'invite':
        print(f"Inviting email: {args.email}")
    elif args.command == 'request':
        request_api_keys(args.provider, console)
    elif args.command == 'update':
        update_api_keys(console)
    elif args.command == 'login':
        login_api_key(args.api_key, console)
    else:
        parser.print_help()
