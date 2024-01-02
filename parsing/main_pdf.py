import Quartz
from Foundation import NSURL
import tiktoken
from dotenv import load_dotenv
from openai import OpenAI
import os
import json

load_dotenv()
oai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

encoding = "gpt-3.5-turbo"
def num_tokens(string: str, encoding_name: str) -> int:
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

url = "/Users/christianreetz/Downloads/19pages.pdf"
pdf_url = NSURL.fileURLWithPath_(url)
pdf_document = Quartz.PDFDocument.alloc().initWithURL_(pdf_url)

number_of_pages = pdf_document.pageCount()
# extracted_text = ""
# 
# 
# for page in range(number_of_pages):
#     pdf_page = pdf_document.pageAtIndex_(page)
#     page_text = pdf_page.string()
#     extracted_text += page_text
# 
# extracted_text = extracted_text.replace('\n', '')
# tokens = num_tokens(extracted_text, encoding)
# print(f"Number of tokens: {tokens}")
# 
# 
# completion = oai.chat.completions.create(
#     model="gpt-4-1106-preview",
#     messages=[
#         {"role":"system","content":"You are a helpful assistant."},
#         {"role":"user","content":f"Please list the top 10 concepts throughout this paper, in pullet point format.\n\n{extracted_text}"},
#     ]
# )
# response = completion.choices[0].message.content
#print(response)

def print_page_text(page_number: int):
    if page_number < 0 or page_number >= number_of_pages:
        print("Invalid page number")
        return

    pdf_page = pdf_document.pageAtIndex_(page_number)
    page_text = pdf_page.string().replace('\n', '')
    print(page_text)

def create_page_text_json():
    page_text_list = []
    for page in range(number_of_pages):
        pdf_page = pdf_document.pageAtIndex_(page)
        page_text = pdf_page.string()
        page_text_list.append({"chunk": page_text})
    return page_text_list

def write_json_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

page_text_list = create_page_text_json()
write_json_to_file(page_text_list, 'input_chunks.json')