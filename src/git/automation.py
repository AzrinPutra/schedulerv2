"""Git automation for schedule backup."""

import os
import subprocess
from pathlib import Path
from typing import Optional, List
from datetime import datetime


class GitAutomation:
    """Git automation for automatic commits and backups."""
    
    def __init__(self, repo_path: Path = Path.cwd()):
        self.repo_path = repo_path
        self.git_executable = self._find_git()
    
    def _find_git(self) -> str:
        """Find git executable."""
        return "git"
    
    def is_git_repo(self) -> bool:
        """Check if directory is a git repository."""
        try:
            result = subprocess.run(
                [self.git_executable, "rev-parse", "--is-inside-work-tree"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def init(self) -> bool:
        """Initialize a git repository."""
        if self.is_git_repo():
            return True
        try:
            result = subprocess.run(
                [self.git_executable, "init"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def get_status(self) -> List[str]:
        """Get list of modified files."""
        try:
            result = subprocess.run(
                [self.git_executable, "status", "--porcelain"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                return [line for line in result.stdout.strip().split('\n') if line]
            return []
        except Exception:
            return []
    
    def add(self, patterns: List[str] = None) -> bool:
        """Stage files for commit."""
        try:
            if patterns is None:
                patterns = ["."]
            result = subprocess.run(
                [self.git_executable, "add"] + patterns,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def commit(self, message: str) -> bool:
        """Commit staged changes."""
        try:
            result = subprocess.run(
                [self.git_executable, "commit", "-m", message],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def get_remote(self) -> Optional[str]:
        """Get remote repository URL."""
        try:
            result = subprocess.run(
                [self.git_executable, "remote", "get-url", "origin"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except Exception:
            return None
    
    def push(self, remote: str = "origin", branch: str = "main") -> bool:
        """Push to remote repository."""
        try:
            result = subprocess.run(
                [self.git_executable, "push", remote, branch],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def pull(self, remote: str = "origin", branch: str = "main") -> bool:
        """Pull from remote repository."""
        try:
            result = subprocess.run(
                [self.git_executable, "pull", remote, branch],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def has_remote(self) -> bool:
        """Check if repository has a remote."""
        return self.get_remote() is not None
    
    def auto_commit(self, message: str = None) -> bool:
        """Auto-commit all changes."""
        if not self.is_git_repo():
            return False
        
        modified = self.get_status()
        if not modified:
            return True
        
        if not self.add():
            return False
        
        if message is None:
            message = f"Update: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        return self.commit(message)
    
    def backup(self, message: str = None, push: bool = False) -> bool:
        """Full backup: commit and optionally push."""
        if not self.auto_commit(message):
            return False
        
        if push and self.has_remote():
            return self.push()
        
        return True
