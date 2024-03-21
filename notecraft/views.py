from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .utils import ExtractText, GenStudyMaterial, GenQuestions
from .models import Chapter, User
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
import time, json, random

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return render(
            request,
            "notecraft/index.html",
            {"studMats": request.user.UserChapters.all()},
        )
    return render(request, "notecraft/auth.html")


def registerUser(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        if username and password and email:
            try:
                user = User.objects.create_user(
                    username=username, email=email, password=password
                )
                user.save()
                login(request, user)
            except Exception as e:
                return JsonResponse({"success": False, "Error": str(e)})
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "Error": "empty fields"})
    return redirect("index")


def loginUser(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        username = data.get("username")
        password = data.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "Error": "Invalid credentials"})

    return redirect("index")


def logoutUser(request):
    logout(request)
    return redirect("index")


def image2text(request):
    result = ""
    if request.method == "POST":
        images = request.FILES.getlist("images")

        if len(images) > 0:
            for image in images:
                if image.size > 1000000:
                    return HttpResponse(
                        f"{image.name} is larger than 1 MB. Please upload a smaller image."
                    )
                text = ExtractText(image)
                if text:
                    result += text
                    result += "\n"
                else:
                    return HttpResponse(f"Couldnt read the text from {image.name}")

        return render(request, "notecraft/OCR.html", {"text": result})
    return redirect("index")


def text2studMat(request):
    if request.method == "POST":
        prompt = request.POST.get("ai_prompt")
        studMat = GenStudyMaterial(prompt)
        json_studMat = None
        count = 1
        while count < 3:
            try:
                json_studMat = json.loads(studMat.choices[0].message.content)
                if len(json_studMat["FC"]) < 5:
                    raise ValueError("Invalid Output: Not enough flashcards")
                break
            except Exception as e:
                count += 1
                json_studMat = None
                if "Not enough flashcards" in str(e):
                    studMat = GenStudyMaterial(
                        prompt + "\nYou must provide at least 5 flashcards."
                    )
                else:
                    studMat = GenStudyMaterial(
                        prompt + "\nThe output must be in proper JSON format."
                    )

        if not json_studMat:
            try:
                json_studMat = json.loads(studMat.choices[0].message.content)
            except Exception as error:
                return HttpResponse(f"\n{count}\n\n{studMat}\n\n{str(error)}")
            
        chapter = Chapter.objects.create(
            user=request.user,
            OCRText=prompt,
            title=json_studMat["title"],
            summary=json_studMat["summary"],
            notes=json_studMat["Notes"],
            flashcards=json_studMat["FC"],
        )
        chapter.save()
        
        return redirect(f"{reverse('chapter')}?studMat={chapter.id}")
    return redirect("index")


def test(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        try:
            chapter = Chapter.objects.get(user=request.user, id=data.get("id"))
        except:
            return JsonResponse({"success": False, "Error": "Invalid Chapter"})
        prompt = chapter.OCRText
        questions = GenQuestions(prompt)
        json_questions = None
        count = 1

        while count < 3:
            try:
                json_questions = json.loads(questions.choices[0].message.content)
                first_key = next(iter(json_questions["MCQ"]))
                if (
                    "A" in json_questions["MCQ"][first_key]
                    or "a" in json_questions["MCQ"][first_key]
                ):
                    raise ValueError("Invalid Output: Wrong MCQ choices")
                elif "Question1" in json_questions["TOF"]:
                    raise ValueError("Invalid Output: Wrong TOF questions")
                elif (len(json_questions["MCQ"]) + len(json_questions["TOF"])) != 10:
                    raise ValueError("Invalid Output: Not enough questions")
                break

            except Exception as e:
                count += 1
                json_questions = None
                if "Wrong MCQ choices" in str(e):
                    questions = GenQuestions(
                        prompt
                        + "\nRemember the choices in MCQ should not contain any sign numbers like '1', 'a' or 'i'."
                    )
                elif "Wrong TOF questions" in str(e):
                    questions = GenQuestions(
                        prompt
                        + "\nRemember to provide proper questions in TOF and MCQ. DOn't mistakenly write just 'Question1' or 'QuestionA' instead of actual questions."
                    )
                elif "Not enough questions" in str(e):
                    questions = GenQuestions(
                        prompt + "\nRemember to provide 7 MCQs and 3 MCQs exactly."
                    )
                else:
                    questions = GenQuestions(
                        prompt + "\n The output must be in proper JSON format."
                    )

        if not json_questions:
            try:
                json_questions = json.loads(questions.choices[0].message.content) 
            except Exception as error:
                return JsonResponse({"success": False, "Error": str(error)})
            
        # shuffling the questions
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

        return JsonResponse({"success": True, "questions": json_questions})



def chapter(request):
    if request.user.is_authenticated:
        id = request.GET.get("studMat", None)
        try:
            chapter = Chapter.objects.get(user=request.user, id=id)
        except:
            chapter = None
        return render(request, "notecraft/studyMaterial.html", {"studMat": chapter})
    return redirect("index")
