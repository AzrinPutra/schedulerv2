import typer
from rich.console import Console
from rich.prompt import Prompt

console = Console()

app = typer.Typer(
    name="scheduler",
    help="FireSchedule - Personal Assistant & Weekly Scheduler",
    add_completion=False,
)

@app.command()
def version():
    """Show the version of FireSchedule."""
    from . import __version__
    console.print(f"[green]FireSchedule v{__version__}[/green]")

@app.command()
def add():
    """Add a new task or event."""
    console.print("[bold]Add New Task[/bold]")
    title = Prompt.ask("Task title")
    console.print(f"Adding: {title}")

@app.command()
def list():
    """List all scheduled tasks."""
    console.print("[bold]Your Schedule[/bold]")
    console.print("No tasks scheduled yet.")

@app.command()
def backup():
    """Backup schedule to GitHub."""
    console.print("[bold]Git Backup[/bold]")
    console.print("Starting backup...")

@app.command()
def settings():
    """Configure FireSchedule."""
    console.print("[bold]Settings[/bold]")
    console.print("No settings configured yet.")
