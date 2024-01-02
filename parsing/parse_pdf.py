import Quartz
from Foundation import NSURL
import tiktoken
from dotenv import load_dotenv
from openai import OpenAI
import os

PDF_PATH = "/Users/christianreetz/Downloads/19pages.pdf"
ENCODING = "gpt-3.5-turbo"
AI_MODEL = "gpt-4-1106-preview"

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
oai = OpenAI(api_key=openai_api_key)

def count_tokens(text: str, encoding_name: str) -> int:
    """ Count the number of tokens in a given string using specified encoding. """
    encoding = tiktoken.encoding_for_model(encoding_name)
    return len(encoding.encode(text))

def extract_pdf_text(pdf_path: str) -> str:
    """ Extract text from a PDF file and return it as a single string. """
    pdf_url = NSURL.fileURLWithPath_(pdf_path)
    pdf_document = Quartz.PDFDocument.alloc().initWithURL_(pdf_url)
    number_of_pages = pdf_document.pageCount()

    extracted_text = ""
    for page in range(number_of_pages):
        pdf_page = pdf_document.pageAtIndex_(page)
        page_text = pdf_page.string()
        extracted_text += page_text

    return extracted_text.replace('\n', '')

def print_pdf_page(pdf_document, page_number: int):
    """ Print text of a specific page from a PDF document. """
    if page_number < 0 or page_number >= pdf_document.pageCount():
        print("Invalid page number")
        return

    pdf_page = pdf_document.pageAtIndex_(page_number)
    print(pdf_page.string())

# Main execution
extracted_text = extract_pdf_text(PDF_PATH)
tokens = count_tokens(extracted_text, ENCODING)
print(f"Number of tokens: {tokens}")

completion = oai.chat.completions.create(
    model=AI_MODEL,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Please list the top 10 concepts throughout this paper, in bullet point format.\n\n{extracted_text}"}
    ]
)
response = completion.choices[0].message.content
# print(response)

# Example of using the print_pdf_page function
# print_pdf_page(Quartz.PDFDocument.alloc().initWithURL_(NSURL.fileURLWithPath_(PDF_PATH)), page_number=0)
