from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .utils import ExtractText, GenStudyMaterial, GenQuestions
from .models import Chapter, User
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.paginator import Paginator
import json, random

# Create your views here.

@login_required
def index(request):
    return render(
        request,
        "notecraft/index.html",
        {"studMats": request.user.UserChapters.order_by("-created_at")[:5]},
    )

@login_required
def myChapters(request):
    sortBy = request.GET.get("sortBy", "created_at")
    order = request.GET.get("order", "asc")
    pageNum = request.GET.get("page", 1)

    if order == "desc":
        studMats = request.user.UserChapters.all().order_by(sortBy)
    else:
        studMats = request.user.UserChapters.all().order_by(f"-{sortBy}")

    try:
        p = Paginator(studMats, 15)
        page = p.get_page(pageNum);
    except Exception as e:
        return JsonResponse({"success": False, "Error": e})

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({"studMats" : list(page.object_list.values()), "hasNext": page.has_next(), "success" : True})

    return render(
        request,
        "notecraft/myChapters.html",
        {"studMats": p.get_page(1), "hasNext": p.get_page(1).has_next()},
    )

def auth(request):
    if request.user.is_authenticated:
        return redirect("index")
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
            except IntegrityError as e:
                if "username" in str(e):
                    return JsonResponse({"success": False, "Error": "Username already taken!"})
                else:
                    return JsonResponse({"success": False, "Error": "Email already in use!"})
            except:
                return JsonResponse({"success": False, "Error": "Failed to register user."})
            
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "Error": "Fields cannot be left empty!"})
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

@login_required
def logoutUser(request):
    if request.method == "POST":
        logout(request)
    return redirect("index")

@login_required
def image2text(request):
    if request.method == "POST":
        result = ""
        images = request.FILES.getlist("images")
        pdf = request.FILES.get("pdf")
        if len(images) > 0:
            for image in images:
                if image.size > 1000000:
                    return JsonResponse({"success": False, "Error": f"{image.name} is larger than 1 MB. Please upload a smaller image."})
                text = ExtractText(image)
                if text:
                    result += text
                    result += "\n"
                else:
                    return JsonResponse({"success" : False, "Error" : f"Couldnt read the text from {image.name}"})

        elif pdf:
            if pdf.size > 1000000:
                return JsonResponse(
                    {"success": False, "Error": f"{pdf.name} is larger than 1 MB. Please upload a smaller PDF."}
                )
            text = ExtractText(pdf)
            result = text
        else:
            return JsonResponse({"success": False, "Error": "No file uploaded"})
        return JsonResponse({"success": True, "text": result})
    return redirect("index")

@login_required
def text2studMat(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        ogPrompt = data.get("prompt").strip()
        prompt = ogPrompt
        error = None
        studMat = None
        if len(prompt)/4 > 35000:
            return JsonResponse({"success": False, "Error": "Text too long."}) 
        count = 1
        
        while count<4:
            try:
                studMat = GenStudyMaterial(prompt, "anthropic")
                json_studMat = json.loads(studMat)
                
                if len(json_studMat["FC"]) < 3:
                    raise ValueError("Invalid Output: Not enough flashcards")
                break
        
            except Exception as e:  
                error = str(e)    
                if "Invalid API" in error or "Error code: 429" in error: 
                    return JsonResponse({"success": False, "Error": error, "output" : studMat, "tries" : count})
                elif "Not enough flashcards" in str(e):
                    prompt = ogPrompt + "\nYou must provide at least 5 flashcards."
                else:
                    prompt = ogPrompt + "\nDon't wrap the output in ```json``` this way. Just provide the json data only. The entire output must be in proper JSON format."
            count += 1

        if count >= 4:
            return JsonResponse({"success": False, "Tries Taken" : count, "Response": studMat, "Error" : error, "prompt": prompt})
        
        chapter = Chapter.objects.create(
            user=request.user,
            OCRText=prompt,
            title=json_studMat["title"],
            summary=json_studMat["summary"],
            notes=json_studMat["Notes"],
            flashcards=json_studMat["FC"],
        )
        chapter.save()

        return JsonResponse({"success": True, "id": chapter.id})
    return redirect("index")

@login_required
def test(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        try:
            chapter = Chapter.objects.get(user=request.user, id=data.get("id"))
        except:
            return JsonResponse({"success": False, "Error": "Invalid Chapter"})
        prompt = chapter.OCRText
        json_questions = None
        count = 1
        error = None

        while count < 4:
            try:
                questions = GenQuestions(prompt, "anthropic")
                json_questions = json.loads(questions)
                mcq_key = next(iter(json_questions["MCQ"]))
                tof_key = next(iter(json_questions["TOF"]))

                if len(json_questions["TOF"][tof_key]) != 2:
                    raise ValueError("Invalid Output: Not enough TOF choices")
                
                elif len(json_questions["MCQ"][mcq_key]) != 4:
                    raise ValueError("Invalid Output: Not enough MCQ choices")

                elif any(choice in json_questions["MCQ"][mcq_key] for choice in ["a", "A", "i", "1"]) or any(choice in str(json_questions["MCQ"][mcq_key]).lower().replace(" ", "") for choice in ["optiona", "option1"]):
                    raise ValueError("Invalid Output: Wrong MCQ choices")
                
                elif "Question1" in json_questions["TOF"] or "Question1" in json_questions["MCQ"]:
                    raise ValueError("Invalid Output: Wrong TOF/MCQ questions")
                
                elif (len(json_questions["MCQ"]) + len(json_questions["TOF"])) != 10:
                    raise ValueError("Invalid Output: Not enough questions")
                break

            except Exception as e:
                error = str(e)
                if "Invalid API" in error or "Error code: 429" in error: 
                    return JsonResponse({"success": False, "Error": error, "output" : questions, "tries" : count})

                elif "Not enough TOF choices" in error:
                    prompt = chapter.OCRText + '\nRemember to provide exactly 2 choices for each TOF question in this format {"True":true/false, "False":true/false and check the output format for TOF questions again.}.'

                elif "Not enough MCQ choices" in error:
                    prompt = chapter.OCRText + "\nRemember to provide exactly 4 choices for MCQ questions."

                elif "Wrong MCQ choices" in error:
                    prompt = chapter.OCRText + "\nRemember the choices in MCQ should not contain any sign numbers like '1', 'a' or 'i' and the 'Question'/'choice' keys in the output format should be replaced with the actual question/choice."

                elif "Wrong TOF/MCQ questions" in error:
                    prompt = chapter.OCRText + "\nRemember to provide proper questions in TOF and MCQ. DOn't mistakenly write just 'Question' or 'Question' instead of actual questions."

                elif "Not enough questions" in error:
                    prompt = chapter.OCRText + "\nRemember to provide 7 MCQs and 3 MCQs exactly."

                else:
                    prompt = chapter.OCRText + "\nDon't wrap the output in ```json``` this way. Just provide the json data only. The entire output must be in proper JSON format."
            
            count += 1

        if count >= 4:
            return JsonResponse({"success": False, "Error": error, "output" : questions, "tries" : count})
        # shuffling the questions
        json_questions = {**json_questions["MCQ"], **json_questions["TOF"]}
        list_questions = list(json_questions.items())
        random.shuffle(list_questions)
        json_questions = dict(list_questions)
        for key, value in json_questions.items():
            list_choices = list(value.items())
            random.shuffle(list_choices)
            json_questions[key] = dict(list_choices)

        return JsonResponse({"success": True, "questions": json_questions})

@login_required
def chapter(request):
    id = request.GET.get("studMat", None)
    try:
        chapter = Chapter.objects.get(user=request.user, id=id)
        chapter.update_last_opened()
    except Exception:
        chapter = None
    return render(request, "notecraft/studyMaterial.html", {"studMat": chapter})
