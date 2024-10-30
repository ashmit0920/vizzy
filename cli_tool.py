import argparse
import pandas as pd
from rich.console import Console
from rich.table import Table
import sys

console = Console()

def welcome_screen():
    console.print("\n[bold cyan]Welcome to Vizzy![/bold cyan]")
    console.print("\nA command-line tool for quick and easy data visualization!\n")

def display_table(data):
    table = Table(title="Data Summary")

    for col in data.columns:
        table.add_column(col)

    for _, row in data.iterrows():
        table.add_row(*map(str, row))

    console.print(table)

def main():
    # Show the welcome screen
    welcome_screen()
    
    # Setup argument parser
    parser = argparse.ArgumentParser(
        description="Vizzy - A command-line tool for data visualization."
    )
    
    # Path to CSV file
    parser.add_argument(
        "-p", "--path",
        type=str,
        help="Path to the CSV file",
        required=True
    )
    
    # Display table flag
    parser.add_argument(
        "-t", "--table",
        action="store_true",
        help="Display data as a table"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Load CSV file
    try:
        data = pd.read_csv(args.path)
    except FileNotFoundError:
        console.print("[bold red]Error:[/bold red] File not found. Please check the path and try again.")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)
    
    # Display data as a table if -t flag is set
    if args.table:
        display_table(data)
    else:
        console.print("[bold yellow]Tip:[/bold yellow] Use -t flag to display data as a table.")

if __name__ == "__main__":
    main()