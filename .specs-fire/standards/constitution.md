# FIRE Constitution
# Universal policies for FIRE (Fast Intent-Run Engineering)

## Git Workflow
- Always commit before starting a new intent
- Use conventional commits: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`
- Create feature branches for intents
- Squash merge for clean history
- Push to GitHub after each intent completion

## PR Process
- PR required for all non-trivial changes
- PR description must link to intent ID
- CI checks must pass before merge
- Code review required (except autopilot mode small changes)

## Security
- Never commit secrets or API keys
- Use `.env` files for credentials
- Scan dependencies regularly

## Standards
- All standards are in `.specs-fire/standards/`
- `constitution.md` is root-only, cannot be overridden
- Other standards follow inheritance rules (see `memory-bank.yaml`)

## Data Persistence
- Schedule output as Markdown files
- Markdown files backed up to git
- SQLite for fast local access (optional, can use Markdown-only)
