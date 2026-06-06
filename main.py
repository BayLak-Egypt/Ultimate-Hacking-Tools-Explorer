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
def search_baylak_files(base_url, search_query):
    results_table = Table(box=box.MINIMAL, expand=True)
    results_table.add_column("File Name", style="green", ratio=2)
    results_table.add_column("Size", style="magenta", justify="center", ratio=1)
    results_table.add_column("Link", style="blue", ratio=3)
    seen_links = set()
    layout = Layout()
    layout.split_column(Layout(name="results", ratio=8), Layout(name="status", size=3))
    layout["results"].update(results_table)
    def process_and_add(url):
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            for card in soup.find_all('div', class_='col-lg-3'):
                link_tag = card.find('a', href=True)
                if not link_tag or link_tag['href'] in seen_links: continue
                text = card.get_text(" ", strip=True)
                if search_query.lower() in text.lower():
                    name_match = re.search(r'([\w\s\-\.\(\)]+\.rar)', text, re.IGNORECASE)
                    if name_match:
                        name = re.sub(r'^(rar|0|1)\s+', '', name_match.group(1).strip(), flags=re.IGNORECASE)
                        name = name.replace("_ed", "_CRACK")
                        size = re.search(r'(\d+\.?\d*\s*(?:KB|MB))', text, re.IGNORECASE)
                        size = size.group(1) if size else "N/A"
                        results_table.add_row(name, size, link_tag['href'])
                        seen_links.add(link_tag['href'])
            return soup
        except: return None
    with Live(layout, refresh_per_second=4, console=console):
        for page in range(1, 10):
            layout["status"].update(f"[bold yellow]Scanning Main Page {page}...[/bold yellow]")
            soup = process_and_add(f"{base_url}?page={page}")
            if not soup: break
            for folder in soup.select('a[href*="/users/baylak/"]'):
                folder_url = folder['href']
                if folder_url.count('/') > 4:
                    layout["status"].update(f"[bold cyan]Scanning Folder: {folder_url.split('/')[-1]}...[/bold cyan]")
                    for f_page in range(1, 6):
                        f_soup = process_and_add(f"{folder_url}?page={f_page}")
                        if not f_soup or not f_soup.find_all('div', class_='col-lg-3'): break
if __name__ == "__main__":
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()
    print_ascii_banner()
    try:
        query = console.input("[bold cyan]Enter search query: [/bold cyan]").strip()
        search_baylak_files("https://www.up-4ever.net/users/baylak", query)
    except KeyboardInterrupt:
        console.print(f"\n[bold red]Scan aborted.")
