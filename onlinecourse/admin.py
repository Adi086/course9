from django.contrib import admin

from .models import (
    Course,
    Instructor,
    Learner,
    Lesson,
    Question,
    Choice,
    Submission
)


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 2


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ("question_text", "lesson")


class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ("title", "course")


admin.site.register(Course)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Submission)

admin.site.register(Question, QuestionAdmin)
admin.site.register(Lesson, LessonAdmin)
