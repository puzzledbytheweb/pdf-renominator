import os
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from pathlib import Path
from openai import OpenAI

client = OpenAI()


def extract_text_from_pdf(pdf_path):
    """Extract text from the first 5 pages of a PDF, using OCR if needed."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num in range(min(5, len(pdf.pages))):
                page = pdf.pages[page_num]
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text + "\n"
                else:
                    # If no text found, use OCR
                    images = convert_from_path(
                        pdf_path, first_page=page_num + 1, last_page=page_num + 1
                    )
                    for image in images:
                        text += pytesseract.image_to_string(image) + "\n"
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
    return text.strip()


def generate_new_title(text):
    """Use OpenAI to generate a meaningful title from the extracted text."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Generate a concise, descriptive title for a document based on the following text. Without adding any keywords such as title. Make sure that the resulting title is meaningful and relevant to the content as well as not too long.",
                },
                {"role": "user", "content": text},
            ],
            max_tokens=20,
        )

        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating title: {e}")
        return None


def find_pdfs(directory):
    """Recursively find all PDFs in a directory."""
    return list(Path(directory).rglob("*.pdf"))


def rename_pdfs(directory, dry_run=True):
    """Process all PDFs in a directory and rename them based on AI-generated titles."""
    pdf_files = find_pdfs(directory)
    for pdf in pdf_files:
        old_name = pdf.name
        extracted_text = extract_text_from_pdf(pdf)
        if not extracted_text:
            print(f"Skipping {old_name}, no extractable text found.")
            continue
        new_title = generate_new_title(extracted_text)
        if not new_title:
            print(f"Skipping {old_name}, could not generate a new title.")
            continue
        new_title = new_title.replace('"', "").rstrip(".,!?")
        new_name = f"{new_title}.pdf"
        new_path = pdf.with_name(new_name)
        if dry_run:
            print(f"{old_name} -> {new_name}")
        else:
            os.rename(pdf, new_path)
            print(f"Renamed: {old_name} -> {new_name}")


if __name__ == "__main__":
    directory = input("Enter the directory containing PDFs: ")
    dry_run = input("Dry run? (yes/no): ").strip().lower() == "yes"
    rename_pdfs(directory, dry_run=dry_run)
