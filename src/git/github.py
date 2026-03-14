"""GitHub integration using gh CLI."""

import subprocess
from pathlib import Path
from typing import Optional, List, Dict
import os


class GitHubIntegration:
    """GitHub integration using gh CLI."""
    
    def __init__(self, repo_path: Path = Path.cwd()):
        self.repo_path = repo_path
        self.gh_executable = self._find_gh()
    
    def _find_gh(self) -> str:
        """Find gh executable."""
        return "gh"
    
    def is_gh_installed(self) -> bool:
        """Check if gh CLI is installed."""
        try:
            result = subprocess.run(
                [self.gh_executable, "--version"],
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def is_authenticated(self) -> bool:
        """Check if authenticated with GitHub."""
        if not self.is_gh_installed():
            return False
        try:
            result = subprocess.run(
                [self.gh_executable, "auth", "status"],
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def get_current_user(self) -> Optional[str]:
        """Get current GitHub username."""
        if not self.is_authenticated():
            return None
        try:
            result = subprocess.run(
                [self.gh_executable, "api", "user", "--jq", ".login"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except Exception:
            return None
    
    def create_repo(self, name: str, private: bool = True, description: str = "") -> bool:
        """Create a new GitHub repository."""
        if not self.is_authenticated():
            return False
        
        cmd = [self.gh_executable, "repo", "create", name]
        if private:
            cmd.append("--private")
        else:
            cmd.append("--public")
        
        if description:
            cmd.extend(["--description", description])
        
        cmd.extend(["--source", str(self.repo_path), "--push", "--clone"])
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def get_repo_info(self) -> Optional[Dict[str, str]]:
        """Get current repository information."""
        if not self.is_gh_installed():
            return None
        
        try:
            result = subprocess.run(
                [self.gh_executable, "repo", "view", "--json", "name,owner,url"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                import json
                data = json.loads(result.stdout)
                return {
                    "name": data.get("name", ""),
                    "owner": data.get("owner", {}).get("login", ""),
                    "url": data.get("url", ""),
                }
            return None
        except Exception:
            return None
    
    def list_repos(self, limit: int = 10) -> List[Dict[str, str]]:
        """List user's repositories."""
        if not self.is_authenticated():
            return []
        
        try:
            result = subprocess.run(
                [self.gh_executable, "repo", "list", "--limit", str(limit), "--json", "name,private,url"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                import json
                repos = json.loads(result.stdout)
                return [
                    {
                        "name": r.get("name", ""),
                        "private": r.get("private", False),
                        "url": r.get("url", ""),
                    }
                    for r in repos
                ]
            return []
        except Exception:
            return []
    
    def add_remote(self, repo_name: str) -> bool:
        """Add a remote for an existing repository."""
        if not self.is_authenticated():
            return False
        
        username = self.get_current_user()
        if not username:
            return False
        
        remote_url = f"https://github.com/{username}/{repo_name}.git"
        
        try:
            result = subprocess.run(
                ["git", "remote", "add", "origin", remote_url],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def push_to_github(self, branch: str = "main") -> bool:
        """Push current branch to GitHub."""
        if not self.is_authenticated():
            return False
        
        try:
            result = subprocess.run(
                [self.gh_executable, "repo", "push", "--source", branch],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except Exception:
            return False
