# =========================
# MAIN ENTRY POINT 
# Run this file with all other helpers in the same folder. 
# Enter the regulation document (PDF) location when prompted. 
# =========================

from extractor import extract_pdf_pages
from processing import clean_lines, build_paragraphs, split_sentences
from rules import is_requirement, classify_requirement
from analytics import print_dashboard
from exporter import export_excel
import re


def run_pipeline(pdf_path):

    pdf_pages = extract_pdf_pages(pdf_path)

    results = []

    current_section = "MAIN"
    current_annex = None
    current_main_clause = "UNKNOWN"
    current_annex_clause = "UNKNOWN"

    ANNEX_PATTERN = re.compile(r'^\s*annex\s+(\d+)', re.IGNORECASE)
    CLAUSE_PATTERN = re.compile(r'^(\d+(?:\.\d+)*)')

    def detect_annex(line):
        m = ANNEX_PATTERN.match(line)
        return f"A{m.group(1)}" if m else None

    def detect_clause(line):
        m = CLAUSE_PATTERN.match(line)
        return m.group(1) if m else None

    def resolve_clause():
        if current_section == "ANNEX":
            return f"{current_annex}.{current_annex_clause}"
        return current_main_clause

    for page in pdf_pages:

        lines = clean_lines(page["text"])
        paragraphs = build_paragraphs(lines)

        for para in paragraphs:

            annex_id = detect_annex(para)
            if annex_id:
                current_section = "ANNEX"
                current_annex = annex_id
                current_annex_clause = "1"
                continue

            clause = detect_clause(para)
            if clause and current_section == "MAIN":
                current_main_clause = clause

            if clause and current_section == "ANNEX":
                current_annex_clause = clause

            sentences = split_sentences(para)

            for sent in sentences:

                if not is_requirement(sent):
                    continue

                cleaned = re.sub(r'\s+', ' ', sent).strip()

                if len(cleaned) < 25:
                    continue

                results.append({
                    "Clause": resolve_clause(),
                    "Section": current_section,
                    "Page": page["page"],
                    "Requirement Type": classify_requirement(cleaned),
                    "Requirement Text": cleaned
                })

    return results


# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":

    pdf_path = input("Enter PDF path: ")

    results = run_pipeline(pdf_path)

    print_dashboard(results)

    export_excel(results, "requirements_output.xlsx")

    print("\n✅ PIPELINE COMPLETE")