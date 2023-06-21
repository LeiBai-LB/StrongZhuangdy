# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 13:36:31 2023

"""

import csv
import requests
from bs4 import BeautifulSoup

def get_google_scholar_data(keyword, num_pages=5):
    base_url = "https://scholar.google.com/scholar"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    rows = []
    for page in range(num_pages):
        params = {
            "q": keyword,
            "start": page * 10,
            "hl": "en"
        }

        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("div", class_="gs_ri")

        for result in results:
            title_element = result.find("h3", class_="gs_rt")
            title = title_element.text.strip()
            title_link = title_element.a["href"] if title_element.a else None

            author_element = result.find("div", class_="gs_a")
            author = author_element.text.strip() if author_element else None

            citation_element = result.find("div", class_="gs_fl")
            citation = citation_element.text.strip() if citation_element else None

            snippet_element = result.find("div", class_="gs_rs")
            snippet = snippet_element.text.strip() if snippet_element else None

            abstract_element = result.find("div", class_="gs_rs")
            abstract = abstract_element.text.strip() if abstract_element else None

            # Extract journal and year information
            info_element = result.find("div", class_="gs_a")
            info_text = info_element.text.strip() if info_element else None
            if info_text:
                info_parts = info_text.split(" - ")
                journal = info_parts[0] if len(info_parts) > 1 else None
                year = info_parts[-1] if len(info_parts) > 1 else None
            else:
                journal = None
                year = None

            rows.append([title, title_link, author, journal, year, citation, snippet, abstract])

    # Save the data into a CSV file
    filename = "google_scholar_data.csv"
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Title Link", "Author", "Journal", "Year", "Citation Count", "Snippet", "Abstract"])  # Write header row
        writer.writerows(rows)

    print(f"Data saved to '{filename}' successfully.")

# Call the function with your desired keyword and number of pages
keyword = "oxidative coupling methane"
num_pages = 10  # Total number of pages (10 results per page)

get_google_scholar_data(keyword, num_pages)
