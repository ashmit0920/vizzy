import pandas as pd
from rich.console import Console
from rich.table import Table

console = Console()
data = pd.read_csv("data.csv")

# Display the data as a table
table = Table(title="Data Summary")
for col in data.columns:
    table.add_column(col)

for _, row in data.head().iterrows():
    table.add_row(*map(str, row))

console.print(table)
