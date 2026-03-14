# Setup
- Install Typer, Rich dependencies
- Run `pip install -r requirements.txt`

# Files Created
- `src/__init__.py` - Package init with version
- `src/cli.py` - Typer CLI with commands (version, add, list, backup, settings)
- `src/main.py` - Entry point that runs CLI
- `requirements.txt` - Dependencies
- `scripts/setup.sh` - Setup script
- `scripts/backup.sh` - Git backup script

# Usage
```bash
# Install dependencies
pip install -r requirements.txt

# Run CLI
python -m src.main

# Or using typer directly
python -m src.cli
```
