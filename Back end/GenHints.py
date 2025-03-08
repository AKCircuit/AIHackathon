from openai import OpenAI
from dotenv import load_dotenv
import os
import pymupdf
from pydantic import BaseModel
from json import loads
import Database

class Hint(BaseModel):
    question_num: int
    hint: str

class Hints(BaseModel):
    hints: list[Hint]

load_dotenv("Back end/API keys.env")

client = OpenAI()

FILENAME = "Back end/maths/EP01.pdf"#"Back end/maths/CRIB_EP01.pdf", 

fileIDs = []
fileContents = []

file = pymupdf.open(FILENAME)
contents = ""
for j in file:
    contents += j.get_text("text")+"\n"
# response = client.files.create(file=open(i, "rb"), purpose="assistants")
# fileIDs.append(response.id)
fileContents.append(contents)
file.close()

chat_completion = client.beta.chat.completions.parse(
    messages=[{"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Generate JSON giving hints for each question, labelled by question number.",
            #"file_ids":fileIDs
        },
        {
            "role":"user",
            "content":"The question paper is as follows: "+contents
        }
    ],
    model="gpt-4o",
    response_format=Hints
)

hintsDict = loads(chat_completion.choices[0].message.content)

for i in hintsDict["hints"]:
    Database.