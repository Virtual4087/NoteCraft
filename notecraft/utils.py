import os
import requests
import json
from notecraft.api_services import anthropicApi as anthropic
from notecraft.api_services import geminiApi as gemini
from notecraft.api_services import openaiApi as openai

def ExtractText(file):
    api_url = "https://api.ocr.space/parse/image"
    payload = {
        "isOverlayRequired": False,
        "apikey": os.getenv("OCR_API_KEY"),
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

def GenStudyMaterial(prompt, api):
    if api == "anthropic":
        return anthropic.GenStudyMaterial(prompt)
    elif api == "gemini":
        return gemini.GenStudyMaterial(prompt)
    elif api == "openai":
        return openai.GenStudyMaterial(prompt)
    else:
        raise ValueError("Invalid API")
        
def GenQuestions(prompt, api):
    if api == "anthropic":
        return anthropic.GenQuestions(prompt)
    elif api == "gemini":
        return gemini.GenQuestions(prompt)
    elif api == "openai":
        return openai.GenQuestions(prompt)
    else:
        raise ValueError("Invalid API")