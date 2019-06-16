
#%%

import os
import re
import urllib.request

from bs4 import BeautifulSoup

from books import book_name_to_code


def get_lines(book_name, chapter=1, verse_start=1, verse_end=None, version="GAE"):
    book_code = book_name_to_code(book_name)
    url ="https://www.bskorea.or.kr/bible/korbibReadpage.php?version={}&book={}&chap={}&sec=1&range=all&keyword1=".format(version, book_code, chapter)
    print(book_name, chapter, verse_start, verse_end, url)

    with urllib.request.urlopen(url) as response:
        html = response.read()
        soup = BeautifulSoup(html, "lxml")
        entries = soup.select("div#tdBible1>.smallTitle,div#tdBible1>span")

        begin = verse_start == 1
        filtered_entries = []
        for e in entries:
            try:
                verse = int(e.select("span.number:first-of-type")[0].get_text().strip())
            except:
                verse = None

            if not begin:
                if verse and verse >= verse_start - 1:
                    begin = True
                continue

            filtered_entries.append((verse, e.get_text()))

            if verse and verse_end and verse == verse_end:
                break

        return filtered_entries

def get_lines_over_chapters(text_range):
    print(text_range)
    book_name, chapter_start, verse_start, chapter_end, verse_end = text_range

    lines = []
    for chapter in range(chapter_start, chapter_end + 1):
        if chapter == chapter_start:
            current_verse_start = verse_start
        else:
            current_verse_start = 1

        if chapter == chapter_end:
            current_verse_end = verse_end
        else:
            current_verse_end = None

        lines += get_lines(book_name, chapter, current_verse_start, current_verse_end)
    return lines
