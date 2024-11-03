import argparse
import pandas as pd
from rich.console import Console
from rich.table import Table
import sys
import matplotlib.pyplot as plt

console = Console()

def welcome_screen():
    console.print("\n[bold cyan]Welcome to Vizzy![/bold cyan]")
    console.print("\nA command-line tool for quick and easy data visualization!")
    console.print("\n[bold yellow]Tip:[/bold yellow] Use 'vizzy -h' to see the available options.\n")

def display_table(data):
    table = Table(title="Data Summary")

    for col in data.columns:
        table.add_column(col)

    for _, row in data.iterrows():
        table.add_row(*map(str, row))

    console.print(table)

def summary(data):
    # Select only numeric columns
    numeric_data = data.select_dtypes(include='number')
    
    if numeric_data.empty:
        console.print("[bold yellow]No numeric columns found in the dataset.[/bold yellow]")
        return

    stats = numeric_data.describe().T
    stats['median'] = numeric_data.median()
    
    # Display statistics in a table format
    stat_table = Table(title="Descriptive Statistics")
    stat_table.add_column("Column")
    stat_table.add_column("Mean", justify="center")
    stat_table.add_column("Median", justify="center")
    stat_table.add_column("Min", justify="center")
    stat_table.add_column("Max", justify="center")
    stat_table.add_column("Std Dev", justify="center")

    for col in stats.index:
        stat_table.add_row(
            col,
            f"{stats['mean'][col]:.2f}",
            f"{stats['median'][col]:.2f}",
            f"{stats['min'][col]:.2f}",
            f"{stats['max'][col]:.2f}",
            f"{stats['std'][col]:.2f}",
        )

    console.print(stat_table)

def display_boxplot(data, cols):
    fig = plt.figure(figsize =(10, 7))

    for col in cols:
        if col not in data.columns:
            console.print(f"[bold red]Error:[/bold red] Column '{col}' not found in the dataset.")
            return

    selected_data = data[cols]
    
    plt.figure(figsize=(10, 6))
    selected_data.boxplot(column=cols)
    plt.title("Boxplot of Selected Columns")
    plt.xticks(rotation=45)
    plt.show()

def display_histograms(data, columns):
    for col in columns:
        if col not in data.columns:
            console.print(f"[bold red]Error:[/bold red] Column '{col}' not found in the dataset.")
            return

    data[columns].hist(bins=20, figsize=(10, 6))
    plt.suptitle("Histograms of Selected Columns")
    plt.show()

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

    # Descriptive statistics (summary) flag
    parser.add_argument(
        "-s", "--summary",
        action="store_true",
        help="Display a summary of numeric columns (mean, median, min, max, std dev)"
    )

    # Boxplot flag
    parser.add_argument(
        "-bp", "--boxplot",
        type=str,
        help="Display boxplots for specified columns (comma-separated list)."
    )

    # Histogram flag
    parser.add_argument(
        "-hg", "--histogram",
        type=str,
        help="Display histograms for specified columns (comma-separated list)"
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
    
    if args.summary:
        summary(data)
    
    if args.boxplot:
        cols = args.boxplot.split(",")
        display_boxplot(data, cols)
    
    if args.histogram:
        columns = args.histogram.split(",")
        display_histograms(data, columns)
        
if __name__ == "__main__":
    main()