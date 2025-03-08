from openai import OpenAI
from dotenv import load_dotenv
import os
import pymupdf
from pydantic import BaseModel
from json import loads
import Database

class Hint(BaseModel):
    question_num: int
    hint_num: int
    hint: str

class Hints(BaseModel):
    hints: list[Hint]

load_dotenv("Back end/API keys.env")

client = OpenAI()

PATH = "Back end/ExP/" 
with open("Back end/Test filenames.json", "r") as file:
    FILENAMES = loads(file.read())

def getHints(path):

    file = pymupdf.open(path)
    contents = ""
    for j in file:
        contents += j.get_text("text")+"\n"

    file.close()

    chat_completion = client.beta.chat.completions.parse(
        messages=[{"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "Generate JSON giving between 2 and 4 hints for each question, labelled by question number and hint number.",
            },
            {
                "role":"user",
                "content":"The question paper is as follows: "+contents
            }
        ],
        model="gpt-4o",
        response_format=Hints
    )

    return loads(chat_completion.choices[0].message.content)

def addHintsToDatabase(db):

    for module in FILENAMES["module"].keys():
        for paper in range(len(FILENAMES["module"][module])):
            hintsDict = getHints(PATH+module+"/"+FILENAMES["module"][module][paper])

            for i in hintsDict["hints"]:
                question_id = db.addQuestion(module, paper+1, i["question_num"])
                db.addHint(i["hint"], question_id)
