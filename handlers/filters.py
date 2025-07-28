def filter_text(text):
    sozaks = ["yomonso'z1", "yomonso'z2"]
    return any(soz in text.lower() for soz in sozaks)
