import random

json_questions = {"MCQ" : {"Question1": {"A":True, "B":False, "C":False, "D":False}, "Question2": {"A":True, "B":False, "C":False, "D":False}, "Question3": {"A":True, "B":False, "C":False, "D":False}, "Question4": {"A":True, "B":False, "C":False, "D":False}, "Question5": {"A":True, "B":False, "C":False, "D":False}}, "TOF" : {"Question1": True, "Question2": False, "Question3": True}}
list_mcq = list(json_questions["MCQ"].items())
list_tof = list(json_questions["TOF"].items())
random.shuffle(list_mcq)
random.shuffle(list_tof)
json_questions["MCQ"] = dict(list_mcq)
json_questions["TOF"] = dict(list_tof)
for key,value in json_questions["MCQ"].items():
    list_choices = list(value.items())
    random.shuffle(list_choices)
    json_questions["MCQ"][key] = dict(list_choices)
print(json_questions)