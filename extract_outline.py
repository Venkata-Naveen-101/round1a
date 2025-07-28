import os
import json
import re
from collections import Counter
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTTextLine, LTChar

INPUT_DIR = "input/"
OUTPUT_DIR = "output/"

def extract_font_size(text_line):
    sizes = []
    for char in text_line:
        if isinstance(char, LTChar):
            sizes.append(round(char.size))
    return sizes

def detect_heading_level(text):
    text = text.strip()
    if re.match(r"^chapter\s+\d+", text.lower()):
        return "H1"
    elif re.match(r"^\d+\.\d+\s", text):
        return "H2"
    elif re.match(r"^\d+\.\d+\.\d+\s", text):
        return "H3"
    return None

def extract_headings(pdf_path):
    lines_with_fonts = []
    font_sizes = []

    for page_num, layout in enumerate(extract_pages(pdf_path), start=1):
        for element in layout:
            if isinstance(element, LTTextContainer):
                for line in element:
                    if isinstance(line, LTTextLine):
                        text = line.get_text().strip()
                        sizes = extract_font_size(line)
                        if text and sizes:
                            avg_size = round(sum(sizes) / len(sizes))
                            lines_with_fonts.append({
                                "text": text,
                                "font_size": avg_size,
                                "page": page_num
                            })
                            font_sizes.append(avg_size)

    # Title detection: largest font on page 1
    title = ""
    title_size = 0
    for line in lines_with_fonts:
        if line["page"] == 1 and line["font_size"] > title_size:
            title = line["text"]
            title_size = line["font_size"]

    # Body font size: most common
    body_font = Counter(font_sizes).most_common(1)[0][0]

    outline = []
    for line in lines_with_fonts:
        text = line["text"]
        page = line["page"]
        size = line["font_size"]

        if text.strip() == title.strip():
            continue

        level = detect_heading_level(text)

        if not level:
            if size > body_font and len(text) < 100:
                level = "H2"  # fallback heuristic

        if level:
            outline.append({
                "level": level,
                "text": text,
                "page": page
            })

    return {
        "title": title,
        "outline": outline
    }

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, filename)
            result = extract_headings(pdf_path)
            output_path = os.path.join(OUTPUT_DIR, filename.replace(".pdf", ".json"))
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()