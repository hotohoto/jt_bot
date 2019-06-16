import datetime
import functools
import os
import re

import scriptures

from books import replace_korean_book_name_with_english
from download import get_lines_over_chapters

if __name__ == "__main__":
    # Find last JT
    posts_folder = "_posts"
    files = [
        x for x in os.listdir(posts_folder) if os.path.isfile(os.path.join(posts_folder, x)) and x.endswith(".hwp")
    ]
    files.sort(reverse=True)
    if not files:
        exit()
    input_path = os.path.join(posts_folder, files[0])
    print("input file: {}".format(input_path))

    _, file_name = os.path.split(input_path)
    input_name, input_ext = os.path.splitext(file_name)
    parsed_input_date = datetime.datetime.strptime(input_name, "%Y%m%d")
    assert parsed_input_date.weekday() is 6, "Sunday check: {}" .format(parsed_input_date.weekday())

    # Retrieve JT
    tmp_output = "_posts/tmp.txt"
    cmd = "hwp5txt {} --output={}".format(input_path, tmp_output)
    os.system(cmd)
    with open(tmp_output) as f:
        jt = f.read()
    os.remove(tmp_output)

    headings = [h.start() for h in re.finditer(r"\[[0-9]+\]", jt)]
    headings.append(len(jt))
    days = []

    # Add bible text
    for i, h in enumerate(headings):

        if i == len(headings) - 1:
            break

        jt_lines = jt[h : headings[i + 1]].split("\n")

        first_line = jt_lines[0]
        translated_first_line = replace_korean_book_name_with_english(first_line)
        extrancted_ranges = scriptures.extract(translated_first_line)
        parsed_text_lines = get_lines_over_chapters(extrancted_ranges[0])
        text_lines = functools.reduce(
            lambda v, e: v + ([e[1]] if e[0] else ["", e[1]]), parsed_text_lines, []
        )

        day_lines = [jt_lines[0]] + text_lines + jt_lines[1:]

        note_link = "(이번주 JT: http://bit.ly/2IiNLfe)"
        day_lines.append(note_link)

        days.append("\n".join([x.strip() for x in day_lines]))

    assert len(days) == 6, len(days)

    # Write files
    with open(os.path.join(posts_folder, "note.md"), "w") as note_file:
        datetime_format = "%m/%d"
        note_file.write("{} ~ {}\n\n".format(
            (parsed_input_date + datetime.timedelta(days=1)).strftime(datetime_format),
            (parsed_input_date + datetime.timedelta(days=6)).strftime(datetime_format)
        ))
        for i, d in enumerate(days):
            target_datetime = parsed_input_date + datetime.timedelta(days=i+1)
            target_filename = "{}.txt".format(i)
            with open(os.path.join(posts_folder, target_filename), "w") as day_file:
                day_file.write(d)
            note_file.write("- [{}](https://raw.githubusercontent.com/hotohoto/jt_bot/master/_posts/{})\n".format(
                target_datetime.strftime(datetime_format),
                target_filename
            ))
