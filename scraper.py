import requests
from bs4 import BeautifulSoup
import time
class Scraper:
    def __init__(self):
        self.base_url = "https://www.up-4ever.net/users/baylak"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
        self.seen_links = set()
    def get_page_content(self, url):
        try:
            time.sleep(0.5)
            response = requests.get(url, headers=self.headers, timeout=15)
            if response.status_code == 200:
                return BeautifulSoup(response.text, 'html.parser')
        except:
            return None
        return None
    def fetch_items(self, url, search_query):
        found_items = []
        soup = self.get_page_content(url)
        if not soup: return [], False
        cards = soup.find_all('article', class_='u4X-card')
        if not cards: return [], False
        for card in cards:
            try:
                name_tag = card.find('a', class_='u4X-name', href=True)
                if not name_tag or name_tag['href'] in self.seen_links: continue
                name = name_tag.get('title', name_tag.get_text(strip=True))
                if "_ed" in name.lower():
                    name = name.lower().replace("_ed", "_crack")
                size_div = card.find('div', class_='u4X-size')
                size = size_div.get_text(strip=True) if size_div else "N/A"
                if search_query.lower() in name.lower():
                    found_items.append({'name': name, 'size': size, 'link': name_tag['href']})
                    self.seen_links.add(name_tag['href'])
            except: continue
        return found_items, True
    def run_scan(self, query, results_table, layout):
        main_soup = self.get_page_content(self.base_url)
        if not main_soup: return
        folders = main_soup.select('.u4pf-grid a.u4pf-card')
        chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        start_time = time.time()
        for folder in folders:
            folder_url = folder['href']
            folder_name = folder.find('span', class_='u4pf-name').get_text(strip=True)
            page = 1
            while True:
                elapsed = int((time.time() - start_time) * 20)
                spinner = chars[elapsed % len(chars)]
                layout["status"].update(f"[bold cyan]{spinner} Scanning: {folder_name}[/bold cyan]")
                page_url = f"{folder_url}?page={page}" if page > 1 else folder_url
                items, has_files = self.fetch_items(page_url, query)
                for item in items:
                    results_table.add_row(item['name'], item['size'], item['link'])
                if not has_files: break
                page += 1