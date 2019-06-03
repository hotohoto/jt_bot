import functools
import os
import re
import scriptures

from books import replace_korean_book_name_with_english
from download import get_lines_over_chapters

if __name__ == "__main__":
    # Retrieve JT
    hwp_input = "_posts/20190602.hwp" #FIXME
    tmp_output = "_tmp/20190602.txt" #FIXME

    cmd = "hwp5txt {} --output={}".format(hwp_input, tmp_output)
    os.system(cmd)
    with open(tmp_output) as f:
        jt = f.read()

    headings = [h.start() for h in re.finditer(r"\[[0-9]+\]", jt)]
    headings.append(len(jt))
    days = []

    # Add bible text
    for i, h in enumerate(headings):
        #FIXME
        if i != 1:
            continue

        if i == len(headings) -1:
            break

        jt_lines = jt[h:headings[i+1]].split("\n")

        first_line = jt_lines[0]
        translated_first_line = replace_korean_book_name_with_english(first_line)
        extrancted_ranges = scriptures.extract(translated_first_line)
        parsed_text_lines = get_lines_over_chapters(extrancted_ranges[0])
        text_lines = functools.reduce(lambda v,e: v + ([e[1]] if e[0] else ["", e[1]]), parsed_text_lines, [])

        day_lines = [jt_lines[0]] + text_lines + jt_lines[1:]

        days.append("\n".join([x.strip() for x in day_lines]))

        print(days[-1]) # FIXME
