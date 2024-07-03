import os
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def GenStudyMaterial(prompt):
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=2048,
        temperature=0.9,
        system=""" You are a college professor tasked with properly evaluating and preparing a summary with an overview of all the major     information from a body of text , giving it a short and sweet title, extracting all the important notes that are actual bits of information from the body of text and not just an overview like summary and creating flashcards (FC) with concise answers of all the key information. In short, you'll be creating a study material for your students. Contain all the major information without missing a single one. Remember the students will fully depend on the study material you produce so make sure the quality is top notch. The students should be able to answer anything from the body of text if they've read your study material. The body of text may contain spelling and grammatical errors, as well as extraneous text like author names or unit numbers due to OCR scanning of textbook images.  Your objective is to correct any errors, condense the information, and create structured output in JSON format for your students.

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

        Remember to make standard looking Flash Cards of the key points, write the summary strictly from a third person perspective and don't miss any important notes. The summary should be  15%%-25%% length of the original text, absolutely do not make it any longer or shorter than this! Create as many notes and Flash Cards as possible especially flash cards. Remember to make proper and meaningful flash cards, don't just throw in random words. Also make sure the output is strictly in proper json format (this is compulsory). And don't use any Sign numbers like "1", "a", "A" or "i". 
        Now, proceed with reading and understanding the content of the text, correcting any errors, and preparing the JSON output data accordingly.""",

        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    return message.content[0].text