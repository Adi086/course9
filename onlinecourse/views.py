from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Question, Choice, Submission, Lesson


@login_required
def submit(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.method == "POST":
        questions = Question.objects.filter(lesson=lesson)

        for question in questions:
            selected_choice_id = request.POST.get(
                f"question_{question.id}"
            )

            if selected_choice_id:
                choice = get_object_or_404(
                    Choice,
                    id=selected_choice_id,
                    question=question
                )

                Submission.objects.create(
                    user=request.user,
                    question=question,
                    choice=choice
                )

        return redirect(
            "show_exam_result",
            lesson_id=lesson.id
        )

    return render(
        request,
        "onlinecourse/exam.html",
        {"lesson": lesson}
    )


@login_required
def show_exam_result(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    questions = Question.objects.filter(lesson=lesson)

    submissions = Submission.objects.filter(
        user=request.user,
        question__lesson=lesson
    )

    total_questions = questions.count()

    correct_answers = 0

    for submission in submissions:
        if submission.choice.is_correct:
            correct_answers += 1

    context = {
        "lesson": lesson,
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "score": correct_answers,
        "submissions": submissions
    }

    return render(
        request,
        "onlinecourse/exam_result.html",
        context
    )
