from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich import box
import os
from scraper import Scraper
console = Console()
def print_ascii_banner():
    banner = r"""
                            ,-.
       ___,---.__          /'|`\          __,---,___
    ,-'    \\`    `-.____,-'  |  `-.____,-'    //    `-.
  ,'        |           ~'\\     /`~           |        `.
 /      ___//              `. ,'          ,  , \\___      \\
|    ,-'   `-.__   _         |        ,    __,-'   `-.    |
|   /          /\\_  `   .    |    ,      _/\\          \\   |
\\  |           \\ \\`-.___ \\   |   / ___,-'/ /           |  /
 \\  \\           | `._   `\\\\  |  //'   _,' |           /  /
  `-.\\         /'  _ `---'' , . ``---' _  `\\         /,-'
     ``       /     \\    ,='/ \\`=.    /     \\       ''
             |__   /|\\_,--.,-.--,--._/|\\   __|    Ultimate hacking tools
             /  `./  \\\\`\\ |  |  | /,//' \,'  \\   Not Safe files
            /   /     ||--+--|--+-/-|     \\   \\ Script By BayLak
           |   |     /'\\_\\_\\ | /_/_/`\\     |   |
            \\   \\__, \\_     `~'     _/ .__/   /
             `-._,-'   `-._______,-'   `-._,-'
    """
    console.print(f"[bold red]{banner}[/bold red]")
    console.print("[bold yellow]========================================================")
    console.print("[bold yellow]NOTICE: This tool is for EDUCATIONAL AND RESEARCH PURPOSES ONLY.")
    console.print("[bold yellow]Usage for unauthorized access or illegal activities is prohibited.")
    console.print("[bold yellow]The user assumes full responsibility for their actions.[/bold yellow]")
    console.print("[bold yellow]========================================================\n")
def run_app():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_ascii_banner()
    query = console.input("[bold cyan]Enter search query: [/bold cyan]").strip()
    scraper = Scraper()
    results_table = Table(box=box.SIMPLE, expand=True)
    results_table.add_column("File Name", style="green", ratio=4, no_wrap=True)
    results_table.add_column("Size", style="magenta", justify="center", ratio=1, no_wrap=True)
    results_table.add_column("Link", style="blue", ratio=3, no_wrap=True)
    layout = Layout()
    layout.split_column(
        Layout(name="results", ratio=20),
        Layout(name="status", size=1)
    )
    layout["results"].update(results_table)
    with Live(layout, refresh_per_second=4, screen=True):
        scraper.run_scan(query, results_table, layout)
    console.print(results_table)
    console.input("\n[bold green]Scan complete. Press Enter to exit...[/bold green]")
if __name__ == "__main__":
    run_app()
