from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views import (
    PollViewSet, QuestionViewSet, ChoiceViewSet, CreateVote, UserCreate,
    VoteResults
)

router = DefaultRouter()

router.register('polls', PollViewSet, base_name='polls')
router.register('questions', QuestionViewSet, base_name='questions')
router.register('choices', ChoiceViewSet, base_name='choices')

urlpatterns = [
    path('', include(router.urls)),
    path('users/', UserCreate.as_view(), name="user_create"),
    path('login/', obtain_auth_token, name='login'),
    path('questions/<int:question_pk>/vote/', CreateVote.as_view(),
         name="create_vote"),
    path('results/<int:poll_pk>/', VoteResults.as_view(), name='results'),
]
