import pdfplumber

def extract_pdf_content(path):
    tables = []
    paragraphs = []
    content = []
    
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            # Extract text (paragraphs/headings)
            text = page.extract_text()
            if text:
                content.append({"type": "paragraph", "text": text.strip()})

            # Extract tables
            page_tables = page.extract_tables()
            for table in page_tables:
                cleaned_table = [
                    [cell.strip() if cell else "Empty Cell" for cell in row]
                    for row in table
                ]
                content.append({"type" : "table", "rows": cleaned_table})

    return content

