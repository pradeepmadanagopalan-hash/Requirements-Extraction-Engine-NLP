import re

def clean_lines(text):
    noise = ["e/ece", "united nations", "contents", "page", "revision"]

    lines = []
    for l in text.split("\n"):
        l = l.strip()
        if len(l) < 5:
            continue
        if any(n in l.lower() for n in noise):
            continue
        lines.append(l)

    return lines


ENUM_PATTERN = re.compile(r'^\(([a-z]|i{1,3}|iv|vi{0,3}|ix)\)', re.IGNORECASE)

def build_paragraphs(lines):
    paragraphs = []
    current = ""

    for line in lines:
        if re.match(r'^\d+(\.\d+)*', line):
            if current:
                paragraphs.append(current.strip())
            current = line

        elif ENUM_PATTERN.match(line):
            current += " " + line

        else:
            if current.endswith("-"):
                current = current[:-1] + line
            else:
                current += " " + line

    if current:
        paragraphs.append(current.strip())

    return paragraphs


def split_sentences(text):
    text = text.replace("i.e.", "IE")
    text = text.replace("e.g.", "EG")

    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if len(s) > 10]