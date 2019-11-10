#%%
import re

#%%
def replace_korean_book_name_with_english(text: str, default_book_name: str):
    rules = [
        (r"(창세기)", "Genesis"),
        (r"(출애굽기)", "Exodus"),
        (r"(레위기)", "Leviticus"),
        (r"(민수기)", "Numbers"),
        (r"(신명기)", "Deuteronomy"),
        (r"(여호수아)", "Joshua"),
        (r"(사사기)", "Judges"),
        (r"(룻기)", "Ruth"),
        (r"(사무엘상)", "I Samuel"),
        (r"(사무엘하)", "II Samuel"),
        (r"(열왕기상)", "I Kings"),
        (r"(열왕기하)", "II Kings"),
        (r"(역대상)", "I Chronicles"),
        (r"(역대하)", "II Chronicles"),
        (r"(에스라)", "Ezra"),
        (r"(느헤미야)", "Nehemiah"),
        (r"(에스더)", "Esther"),
        (r"(욥기)", "Job"),
        (r"(시편)", "Psalms"),
        (r"(잠언)", "Proverbs"),
        (r"(전도서)", "Ecclesiastes"),
        (r"(아가)", "Song of Songs"),
        (r"(이사야)", "Isaiah"),
        (r"(예레미야)", "Jeremiah"),
        (r"(예레미야\S?애가)", "Lamentations"),
        (r"(에스겔)", "Ezekiel"),
        (r"(다니엘)", "Daniel"),
        (r"(호세아)", "Hosea"),
        (r"(요엘)", "Joel"),
        (r"(아모스)", "Amos"),
        (r"(오바댜)", "Obadiah"),
        (r"(요나)", "Jonah"),
        (r"(미가)", "Micah"),
        (r"(나훔)", "Nahum"),
        (r"(하박국)", "Habakkuk"),
        (r"(스바냐)", "Zephaniah"),
        (r"(학개)", "Haggai"),
        (r"(스가랴)", "Zechariah"),
        (r"(말라기)", "Malachi"),
        (r"(마태복음)", "Matthew"),
        (r"(마가복음)", "Mark"),
        (r"(누가복음)", "Luke"),
        (r"(요한복음)", "John"),
        (r"(사도행전)", "Acts"),
        (r"(로마서)", "Romans"),
        (r"(고린도\S?전서)", "1 Corinthians"),
        (r"(고린도\S?후서)", "2 Corinthians"),
        (r"(갈라디아서)", "Galatians"),
        (r"(에베소서)", "Ephesians"),
        (r"(빌립보서)", "Philippians"),
        (r"(골로새서)", "Colossians"),
        (r"(데살로니가\S?전서)", "1 Thessalonians"),
        (r"(데살로니가\S?후서)", "2 Thessalonians"),
        (r"(디모데\S?전서)", "1 Timothy"),
        (r"(디모데\S?후서)", "2 Timothy"),
        (r"(디도서)", "Titus"),
        (r"(빌레몬서)", "Philemon"),
        (r"(히브리서)", "Hebrews"),
        (r"(야고보서)", "James"),
        (r"(베드로\S?전서)", "1 Peter"),
        (r"(베드로\S?후서)", "2 Peter"),
        (r"(요한\S?1서)", "1 John"),
        (r"(요한\S?2서)", "2 John"),
        (r"(요한\S?3서)", "3 John"),
        (r"(유다서)", "Jude"),
        (r"(요한계시록)", "Revelation"),
    ]
    book_name_used = None
    for r in rules:
        pattern, book_name = r
        before = text
        text = re.sub(pattern, book_name, text)
        if before != text:
            book_name_used = book_name
            break
    else:
        if default_book_name is not None:
            pattern = r"(\[[0-9]+\])"
            repl = r"\1 " + re.escape(default_book_name)
            text = re.sub(pattern, repl, text)
            book_name_used = default_book_name
    text = text.replace("장", ":")
    text = text.replace("절", " ")
    return text, book_name_used


#%%
def book_name_to_code(name: str):
    rule_map = {
        "Genesis": "gen",
        "Exodus": "exo",
        "Leviticus": "lev",
        "Numbers": "num",
        "Deuteronomy": "deu",
        "Joshua": "jos",
        "Judges": "jdg",
        "Ruth": "rut",
        "I Samuel": "1sa",
        "II Samuel": "2sa",
        "I Kings": "1ki",
        "II Kings": "2ki",
        "I Chronicles": "1ch",
        "II Chronicles": "2ch",
        "Ezra": "ezr",
        "Nehemiah": "neh",
        "Esther": "est",
        "Job": "job",
        "Psalms": "psa",
        "Proverbs": "pro",
        "Ecclesiastes": "ecc",
        "Song of Songs": "sng",
        "Isaiah": "isa",
        "Jeremiah": "jer",
        "Lamentations": "lam",
        "Ezekiel": "ezk",
        "Daniel": "dan",
        "Hosea": "hos",
        "Joel": "jol",
        "Amos": "amo",
        "Obadiah": "oba",
        "Jonah": "jnh",
        "Micah": "mic",
        "Nahum": "nam",
        "Habakkuk": "hab",
        "Zephaniah": "zep",
        "Haggai": "hag",
        "Zechariah": "zec",
        "Malachi": "mal",
        "Matthew": "mat",
        "Mark": "mrk",
        "Luke": "luk",
        "John": "jhn",
        "Acts": "act",
        "Romans": "rom",
        "I Corinthians": "1co",
        "II Corinthians": "2co",
        "Galatians": "gal",
        "Ephesians": "eph",
        "Philippians": "php",
        "Colossians": "col",
        "I Thessalonians": "1th",
        "II Thessalonians": "2th",
        "I Timothy": "1ti",
        "II Timothy": "2ti",
        "Titus": "tit",
        "Philemon": "phm",
        "Hebrews": "heb",
        "James": "jas",
        "I Peter": "1pe",
        "II Peter": "2pe",
        "I John": "1jn",
        "II John": "2jn",
        "III John": "3jn",
        "Jude": "jud",
        "Revelation": "rev",
    }
    return rule_map[name]
