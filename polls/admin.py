from django.contrib import admin

from .models import Poll, Question, Choice


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0
    ordering = ('order',)


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 0
    ordering = ('order',)


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    inlines = (QuestionInline,)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = (ChoiceInline,)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    pass
