import pdfplumber 
import re
import unicodedata
import os
import uuid

def clean_text(text):

    _HORIZONTAL_SPACES = re.compile(r'[ \t\f\v]+')
    _EXCESS_NEWLINES = re.compile(r'\n{3,}')
    _CID_ERRORS = re.compile(r'\(cid:\d+\)')
    _HYPHENATED_WORDS = re.compile(r'(\w+)-\s*\n\s*(\w+)')

    text = _CID_ERRORS.sub('', text)
    text = _HYPHENATED_WORDS.sub(r'\1\2', text)
    text = unicodedata.normalize("NFKC", text)
    text = _HORIZONTAL_SPACES.sub(' ', text)
    text = '\n'.join(line.strip() for line in text.splitlines())
    text = _EXCESS_NEWLINES.sub('\n\n', text)

    return text.strip()


def load_pdf(pdf_path):

    document = []

    
    document_id = str(uuid.uuid4())
    document_name = os.path.basename(pdf_path)

    with pdfplumber.open(pdf_path) as pdf:

        for pg_no, page in enumerate(pdf.pages, start=1):

            text = page.extract_text(layout=True)

            if text:

                cleaned_text = clean_text(text)

                document.append(
                    {
                        "document_id": document_id,
                        "document_name": document_name,
                        "page_number": pg_no,
                        "content": cleaned_text
                    }
                )

    return document

