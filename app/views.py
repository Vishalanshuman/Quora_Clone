from django.views.generic.edit import CreateView
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from app.forms import CreateUserForm, QuestionForm
from app.models import Question, Answer

# Create your views here.


def base(request):
    return render(request, "base.html")


def signup(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("User Created Successfully.")
        else:
            return HttpResponse(form.error_messages)
    return render(request, "user/signup.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("/")  # Replace 'home' with the name of your home page URL
        else:
            error_message = "Invalid credentials. Please try again."
    else:
        error_message = None
    return render(request, "user/login.html", {"error_message": error_message})


@login_required
def user_logout(request):
    logout(request)
    return redirect("user_login")


@login_required
def view_questions(request):
    questions = Question.objects.all().order_by("-pub_date")
    return render(request, "QA/view_question.html", {"questions": questions})


@login_required
def answer_question(request, question_id):
    question = Question.objects.get(pk=question_id)
    if request.method == "POST":
        content = request.POST["content"]
        answer = Answer(user=request.user, question=question, content=content)
        answer.save()
    answers = Answer.objects.filter(question=question).order_by("-pub_date")
    return render(
        request, "QA/answer_question.html", {"question": question, "answers": answers}
    )


@login_required
def like_answer(request, answer_id):
    answer = Answer.objects.get(pk=answer_id)
    if request.user not in answer.likes.all():
        answer.likes.add(request.user)
    return redirect(
        "view_questions"
    )  # Replace 'view_questions' with the name of your view questions URL


class AddQuestion(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = "QA/post_question.html"
    success_url = ""
