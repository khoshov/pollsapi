from rest_framework import generics
from rest_framework import viewsets
from .models import Poll, Question, Choice, Vote
from .serializers import (
    PollSerializer, QuestionSerializer, ChoiceSerializer, VoteSerializer,
    VoteResultsSerializer, UserSerializer,
)


class CreateVote(generics.CreateAPIView):
    serializer_class = VoteSerializer

    def get_serializer(self, *args, **kwargs):
        if 'data' in kwargs:
            data = kwargs['data']

            if isinstance(data, list):
                kwargs['many'] = True

        return super(CreateVote, self).get_serializer(*args, **kwargs)


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class VoteResults(generics.ListAPIView):
    def get_queryset(self):
        queryset = Vote.objects.filter(
            choice__question__poll=self.kwargs["poll_pk"],
            voted_by=self.request.user.pk,
        )
        return queryset

    serializer_class = VoteResultsSerializer


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer
