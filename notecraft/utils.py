from openai import OpenAI
from dotenv import dotenv_values
import requests
import json

env_vars = dotenv_values("./.env")


def ExtractText(file):
    api_url = "https://api.ocr.space/parse/image"
    payload = {
        "isOverlayRequired": False,
        "apikey": env_vars["OCR_API_KEY"],
        "language": "eng",
        "scale": True,
        "OCREngine": 2,
    }

    r = requests.post(
        api_url,
        files={file.name: file},
        data=payload,
    )
    response = r.content.decode()
    response_data = json.loads(response)
    try:
        parsed_results = response_data["ParsedResults"]
    except:
        return None

    parsed_text = ""
    for result in parsed_results:
        parsed_text += result["ParsedText"]

    return parsed_text.replace("\n", " ")


def GenStudyMaterial(prompt):
    client = OpenAI(api_key=env_vars["OPENAI_API_KEY"])
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {
                "role": "system",
                "content": """You are a college teacher tasked with properly evaluating and preparing a summary with an overview of all the major information from a body of text , giving it a short and sweet title, extracting all the important notes that are actual bits of information from the body of text and not just an overview like summary and creating flashcards (FC) with concise answers of all the key information. In short, you'll be creating a study material for your students. Contain all the major information without missing a single one. Remember the students will fully depend on the study material you produce so make sure the quality is top notch. The students should be able to answer anything from the body of text if they've read your study material. The body of text may contain spelling and grammatical errors, as well as extraneous text like author names or unit numbers due to OCR scanning of textbook images. Your objective is to correct any errors, condense the information, and create structured output in JSON format for your students.

                Output Format:
                {
                    "title": "Short title for the text",
                    "summary": "Summary of the text. Approximately 15%%-25%% length of the original text",
                    "Notes" : ["note 1", "note 2", "note 3",....],
                    "FC": {"Front": "Back"},
                }

                title: A short and meaningful title for the body of text.
                summary: A descriptive summary of suitable size.
                Notes: Important points extracted from the text.
                FC: Flashcards with key information having two sides i.e. front & back. 

                Remember to make standard looking Flash Cards of the key points, write the summary strictly from a third person perspective and don't miss any important notes. The summary should be  15%%-25%% length of the original text, absolutely do not make it any longer or shorter than this! Create as many notes and Flash Cards as possible especially flash cards. Remember to make proper and meaningful flash cards, don't just throw in random words. Also make sure the output is strictly in proper json format (this is compulosry). And don't use any Sign numbers like "1", "a", "A" or "i".
                Now, proceed with reading and understanding the content of the text, correcting any errors, and preparing the JSON output data accordingly.
                """,
            },
            {"role": "user", "content": prompt},
        ],
    )
    response = completion
    return response


def GenQuestions(prompt):
    client = OpenAI(api_key=env_vars["OPENAI_API_KEY"])
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {
                "role": "system",
                "content": """You are a creative teacher tasked with generating multiple choice questions(MCQ) with hard choices, and generating true or false(TOF) questions from a body of text. The text may contain spelling and grammatical errors, as well as extraneous text like author names or unit numbers due to OCR scanning of textbook images. Your objective is to correct any errors, condense the information, and create structured output in JSON format for your students.

                Output Format:
                {
                    "MCQ": {"Question" : {"choice1": true/false, "choice2": true/false, "choice3": true/false, "choice4": true/false},
                    "TOF": {"Question": true/false}
                }

                MCQ: Questions with multiple choices and their correct/incorrect answers.
                TOF: Questions with true/false answers.

                Remember to provide proper choices in MCQ and don't use any Sign numbers like "1", "a", "A", "i" or "Question1" when writing questions or choices. Also make sure the output is strictly in proper json format. This is compulosry. Create exactly 7 MCQs and 3 TOFs. Abide by this number, it is very important. Never provide true/false questions in MCQ. All the MCQ questions must have 4 choices. 
                Now, proceed with reading and understanding the content of the text, correcting any errors, and preparing the JSON output data accordingly.
                """,
            },
            {"role": "user", "content": prompt},
        ],
    )
    response = completion
    return response
