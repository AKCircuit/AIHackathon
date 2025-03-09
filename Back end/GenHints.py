from openai import OpenAI
from dotenv import load_dotenv
import os
import pymupdf
from pydantic import BaseModel
from json import loads
import Database
import base64

class Hint(BaseModel):
    question_num: int
    hint_num: int
    hint: str

class Hints(BaseModel):
    hints: list[Hint]

load_dotenv(".env")

client = OpenAI(api_key=os.getenv("API_KEY"))

PATH = "Back end/ExP/" 
with open("Back end/Test filenames.json", "r") as file:
    FILENAMES = loads(file.read())

def getExPContents(path):
    file = pymupdf.open(path)
    contents = ""
    for j in file:
        contents += j.get_text("text")+"\n"

    file.close()
    return contents

def genCribImages(path):
    doc = pymupdf.open(path)
    zoom = 4
    mat = pymupdf.Matrix(zoom, zoom)
    count = 0
    # Count variable is to get the number of pages in the pdf
    for p in doc:
        count += 1
    imgPaths = []
    for i in range(count):
        val = path[:-4]+str(i+1)+".png"
        page = doc.load_page(i)
        pix = page.get_pixmap(matrix=mat)
        pix.save(val)
        imgPaths.append(val)
    doc.close()
    return imgPaths

def encodeImage(path):
    with open(path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")

def getHints(path):

    contents = getExPContents(path)
    cribPath = path[:-8]+"CRIB_"+path[-8:]
    imgPaths = genCribImages(cribPath)

    images = {"role": "user",
                "content": [
                    {"type": "text", "text": "The worked solutions are in the attached images."},
                ],
    }

    for i in imgPaths:
        encodedImage = encodeImage(i)
        images["content"].append({"type":"image_url", "image_url":{"url":f"data:image/png;base64,{encodedImage}", "detail":"low"}})

    chat_completion = client.beta.chat.completions.parse(
        messages=[{"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "Generate 2 hints for each question as JSON.  Each hint should be a separate JSON object, labelled by question number and hint number. Write maths in LaTex, using '$' delimiters.",
            },
            {
                "role":"user",
                "content":"The question paper is as follows: "+contents
            },
            images
        ],
        model="gpt-4o",
        response_format=Hints,
        max_tokens=2048
    )

    return loads(chat_completion.choices[0].message.content)

def addHintsToDatabase(db):

    for module in FILENAMES["module"].keys():
        for paper in range(len(FILENAMES["module"][module])):
            hintsDict = getHints(PATH+module+"/"+FILENAMES["module"][module][paper])

            for i in hintsDict["hints"]:
                questionExists, question_id = db.questionInDatabase(module, paper+1, i["question_num"])
                if not questionExists:
                    question_id = db.addQuestion(module, paper+1, i["question_num"])
                db.addHint(i["hint"], question_id, i["hint_num"])
    