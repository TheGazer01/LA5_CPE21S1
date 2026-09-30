"""Console output built on the pip module: rich."""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def show_banner():
    console.print(Panel.fit(
        "[bold cyan]PAYMENT SYSTEM[/bold cyan]\n"
        "[white]Polymorphism: one interface, many forms[/white]",
        border_style="cyan"))


def show_summary(history):
    table = Table(title="Transaction Summary", header_style="bold magenta")
    table.add_column("#", justify="right")
    table.add_column("Txn ID")
    table.add_column("Payer")
    table.add_column("Method")
    table.add_column("Amount (PHP)", justify="right")
    table.add_column("Status")
    for i, t in enumerate(history, start=1):
        color = "green" if t.success else "red"
        table.add_row(str(i), t.txn_id, t.payer, t.method,
                      f"{t.amount:,.2f}", f"[{color}]{t.status}[/{color}]")
    console.print(table)
