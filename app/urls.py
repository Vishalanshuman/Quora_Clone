from django.urls import path
from .views import signup
from . import views

urlpatterns = [
    path("", views.base),
    path("signup/", signup, name="user_signup"),
    path("login/", views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),
    path("view_questions/", views.view_questions, name="view_questions"),
    path(
        "answer_question/<int:question_id>/",
        views.answer_question,
        name="answer_question",
    ),
    path("like_answer/<int:answer_id>/", views.like_answer, name="like_answer"),
    path("post_question/", views.AddQuestion.as_view(), name="create_question"),
]
