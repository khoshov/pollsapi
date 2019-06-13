from django.contrib.auth.models import User
from django.db import models


class Poll(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    poll = models.ForeignKey(
        Poll, related_name='questions', on_delete=models.CASCADE)
    multiple_choice = models.BooleanField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('order',)


class Choice(models.Model):
    question = models.ForeignKey(
        Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    choice = models.ForeignKey(
        Choice, related_name='votes', on_delete=models.CASCADE)
    voted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.voted_by, self.choice)

    class Meta:
        unique_together = ('choice', 'voted_by')
