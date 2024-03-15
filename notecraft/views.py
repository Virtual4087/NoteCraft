from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .utils import ExtractText, GenStudyMaterial
from .models import Chapter, User
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
import time, json
# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return render(request, "notecraft/index.html", {"chapters" : request.user.UserChapters.all()})
    return render(request, "notecraft/auth.html")

def registerUser(request):  
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        if username and password and email:
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                login(request, user)
            except Exception as e:
                return JsonResponse({"success":False, "Error": str(e)})
            return JsonResponse({"success":True})
        return JsonResponse({"success":False, "Error": "empty fields"})
    return redirect("index")

def loginUser(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        username = data.get("username")
        password = data.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({"success":True})
        return JsonResponse({"success":False, "Error": "Invalid credentials"})
    
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


def text2QNA(request):
    if request.method == "POST":
        prompt = request.POST.get("ai_prompt")
        response = GenStudyMaterial(prompt)
        count = 1
        while count < 4:
            try:
                output = response.choices[0].message.content
                json_output = json.loads(output)
                first_key = next(iter(json_output["MCQ"]))
                if (
                    "A" in json_output["MCQ"][first_key]
                    or "a" in json_output["MCQ"][first_key]
                ):
                    raise ValueError("Invalid Output: Wrong MCQ choices")
                elif "Question1" in json_output["TOF"]:
                    raise ValueError("Invalid Output: Wrong TOF questions")
                elif len(json_output["FC"]) < 5 or len(json_output["MCQ"]) < 5 or len(json_output["TOF"]) < 5:
                    raise ValueError("Invalid Output: Not enough questions")
                break

            except Exception as e:
                count += 1
                if count > 3:
                    json_output = None
                    break

                if "Wrong MCQ choices" in str(e):
                    response = GenStudyMaterial(
                        prompt
                        + "\nRemember the choices in MCQ should not contain any sign numbers like '1', 'a' or 'i'."
                    )
                elif "Wrong TOF questions" in str(e):
                    response = GenStudyMaterial(
                        prompt
                        + "\nRemember to provide proper questions in TOF and MCQ. DOn't mistakenly write just 'Question1' or 'QuestionA' instead of actual questions."
                    )
                elif "Not enough questions" in str(e):
                    response = GenStudyMaterial(
                        prompt
                        + "\nRemember to provide at least 5 flashcards, 5 MCQs and 5 TOFs."
                    )
                else:                
                    response = GenStudyMaterial(prompt + "\n The output must be in proper JSON format.")

        if json_output:
            chapter = Chapter.objects.create(
                user=request.user,
                OCRText=prompt,
                title=json_output["title"],
                summary=json_output["summary"],
                notes=json_output["Notes"],
                flashcards=json_output["FC"],
                mcqs=json_output["MCQ"],
                tofs=json_output["TOF"],
            )
            chapter.save()
        else:
            chapter = None
            return HttpResponse(f"\n{count}\n\n{output}\n\n{response}")
        return redirect(f"{reverse('chapter')}?studMat={chapter.id}")
    return redirect("index")

def chapter(request):
    if request.user.is_authenticated:
        id = request.GET.get("studMat", None)
        try:
            chapter = Chapter.objects.get(user=request.user, id=id)
        except:
            chapter = None
        return render(request, "notecraft/studyMaterial.html", {"studMat": chapter})
    return redirect("index")