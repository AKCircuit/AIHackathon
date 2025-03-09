from openai import OpenAI
from dotenv import load_dotenv
import os
import pymupdf
import base64
from pydantic import BaseModel
from json import loads

pdffile = "Back end/ExP/electromag/CRIB_EP01.pdf"
doc = pymupdf.open(pdffile)
zoom = 4
mat = pymupdf.Matrix(zoom, zoom)
count = 0
# Count variable is to get the number of pages in the pdf
for p in doc:
    count += 1
for i in range(count):
    val = f"Back end/ExP/electromag/CRIB_EP01_{i+1}.png"
    page = doc.load_page(i)
    pix = page.get_pixmap(matrix=mat)
    pix.save(val)
doc.close()

def encodeImage(path):
    with open(path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")

msgs = [{"role": "user",
            "content": [
                {"type": "text", "text": "Generate two sections of summary for the answer of each question. Each summary should be a separate JSON object, labelled by question number and summary number."},
            ],
}]

for i in range(count):
    encodedImage = encodeImage(f"Back end/ExP/electromag/CRIB_EP01_{i+1}.png")
    
    msgs[0]["content"].append({"type":"image_url", "image_url":{"url":f"data:image/png;base64,{encodedImage}"}, "detail":"low"})

load_dotenv(".env")

client = OpenAI(api_key=os.getenv("API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o",
    messages=msgs,
    max_tokens=2048,
)

print(response.choices[0])