import os
import re
import urllib.request

from bs4 import BeautifulSoup

from translate import translate


def get_chapter(book, chapter=1, version="GAE"):
    url ="https://www.bskorea.or.kr/bible/korbibReadpage.php?version={}&book={}&chap={}&sec=1&range=all&keyword1=".format(version, book, chapter)

    with urllib.request.urlopen(url) as response:
        html = response.read()
        soup = BeautifulSoup(html, "lxml")
        entries = [x.get_text() for x in soup.select("div#tdBible1>.smallTitle,div#tdBible1>span")]
        return "\n".join(entries)

if __name__ == "__main__":
    hwp_input = "_posts/20190602.hwp"
    tmp_output = "_tmp/20190602.txt"
    cmd = "hwp5txt {} --output={}".format(hwp_input, tmp_output)
    os.system(cmd)
    with open(tmp_output) as f:
        jt = f.read()

    headings = [h.start() for h in re.finditer(r"\[[0-9]+\]", jt)]
    headings.append(len(jt))
    days = []

    for i, h in enumerate(headings):
        if i == len(headings) -1:
            break

        day = jt[h:headings[i+1]]
        days.append(day)
        firstline = re.findall(r"\[[0-9]+\].*", day)

    # print(days)
    # book = 'gen'
    # chapter = 2
    # print(get_chapter(book, chapter))
