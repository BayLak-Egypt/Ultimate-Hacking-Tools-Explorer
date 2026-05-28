import requests
from bs4 import BeautifulSoup
import re
import time
import sys
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.live import Live
from rich.layout import Layout
from rich import box
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
def search_baylak_files(base_url, search_query, total_pages=32):
    layout = Layout()
    layout.split_column(
        Layout(name="results", ratio=8),
        Layout(name="progress", size=3)
    )
    results_table = Table(box=box.MINIMAL, expand=True)
    results_table.add_column("File Name", style="green", ratio=2, no_wrap=True)
    results_table.add_column("Size", style="magenta", justify="center", ratio=1)
    results_table.add_column("Link", style="blue", ratio=3)
    progress = Progress(
        SpinnerColumn(spinner_name="dots"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40, complete_style="green", finished_style="bold yellow"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    )
    task_id = progress.add_task(f"[bold yellow]Scanning...[/bold yellow]", total=total_pages)
    layout["results"].update(results_table)
    layout["progress"].update(progress)
    with Live(layout, refresh_per_second=5, console=console):
        for page in range(1, total_pages + 1):
            url = f"{base_url}?page={page}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            try:
                response = requests.get(url, headers=headers, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                file_cards = soup.find_all('div', class_='col-lg-3')
                for card in file_cards:
                    text = card.get_text(" ", strip=True)
                    name_match = re.search(r'([\w\s\-\.\(\)]+\.rar)', text, re.IGNORECASE)
                    if name_match:
                        name = name_match.group(1).strip()
                        name = re.sub(r'^(rar|0|1)\s+', '', name, flags=re.IGNORECASE)
                        if "_ed" in name.lower():
                            name = name.replace("_ed", "_CRACK")
                        if search_query.lower() in name.lower():
                            size_match = re.search(r'(\d+\.?\d*\s*(?:KB|MB))', text, re.IGNORECASE)
                            size = size_match.group(1) if size_match else "N/A"
                            link_tag = card.find('a', href=True)
                            link = link_tag['href'] if link_tag else "N/A"
                            results_table.add_row(name, size, link)
            except:
                pass
            progress.advance(task_id, advance=1)
            time.sleep(0.1)
if __name__ == "__main__":
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()
    print_ascii_banner()
    try:
        query = console.input("[bold cyan]Enter search query: [/bold cyan]").strip()
        search_baylak_files("https://www.up-4ever.net/users/baylak", query)
    except KeyboardInterrupt:
        console.print(f"\n[bold red]Scan aborted.")