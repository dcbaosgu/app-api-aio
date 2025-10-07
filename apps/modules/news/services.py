import requests
import xmltodict
from math import ceil
from bs4 import BeautifulSoup
from apps.utils.helper import Helper


class RSSService:
    def __init__(self):
        self.base_url = "https://vnexpress.net/rss/"

    async def fetch_rss(self, category: str):
        rss_url = f"{self.base_url}{category}"
        response = requests.get(rss_url, timeout=10)
        response.raise_for_status()
        data = xmltodict.parse(response.text)
        return data

    async def parse_items(self, data):
        items = data["rss"]["channel"]["item"]
        result = []

        for item in items:
            title = item.get("title", "")
            link = item.get("link", "")
            date = item.get("pubDate", "")
            image = item.get("enclosure", {}).get("@url", "")

            # Clean data description
            desc_raw = item.get("description", "")
            soup = BeautifulSoup(desc_raw, "html.parser")
            desc = next(soup.stripped_strings, "") # Get only text in string

            result.append({
                "title": title,
                "link": link,
                "image": image,
                "description": desc,
                "created_at": Helper.date_to_timestamp(dt=date, fmt="%a, %d %b %Y %H:%M:%S %z"),
            })

        return result

    async def get_paginated(self, page: int, limit: int, category: str, search: str = None):
        data = await self.fetch_rss(category)
        all_items = await self.parse_items(data)

        if search:
            search_lower = search.lower()
            all_items = [item for item in all_items if search_lower in item["title"].lower()]

        total = len(all_items)
        total_pages = ceil(total / limit)
        start, end = (page - 1) * limit, page * limit

        result = {
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages,
            "results": all_items[start:end],
        }
        return result
