from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Poll, Question, Choice, Vote


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'

    def create(self, validated_data):
        choices_data = validated_data.pop('choice', None)
        question = Question.objects.create(**validated_data)
        if choices_data:
            for choice_data in choices_data:
                Choice.objects.create(question=question, **choice_data)
        return question


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    def create(self, validated_data):
        questions_data = validated_data.pop('questions', None)
        poll = Poll.objects.create(**validated_data)
        if questions_data:
            for question_data in questions_data:
                choices_data = question_data.pop('choice', None)
                question = Question.objects.create(set=poll, **question_data)
                if choices_data:
                    for choice_data in choices_data:
                        Choice.objects.create(question=question, **choice_data)
        return poll

    class Meta:
        model = Poll
        fields = '__all__'


class VoteListSerializer(serializers.ListSerializer):

    def create(self, validated_data):
        new_votes = []
        for vote in validated_data:
            new_votes.append(
                Vote(
                    choice=vote.get('choice'),
                    voted_by=self.context['request'].user,
                )
            )
        return Vote.objects.bulk_create(new_votes)

    def validate(self, attrs):
        try:
            context = self.context['request'].parser_context['kwargs']
            question_pk = context['question_pk']
            question = Question.objects.get(pk=question_pk)
            multiple_choice = question.multiple_choice
            for attr in attrs:
                pk = attr.get('choice').pk
                choice = Choice.objects.filter(pk=pk, question=question_pk)
                if not choice:
                    msg = 'Question with pk={} has no choice with pk={}'.format(
                        question_pk, pk)
                    raise serializers.ValidationError(msg)
            if not multiple_choice:
                msg = 'You are trying to select more then one choice but' \
                      ' question multiple_choice is {}'.format(multiple_choice)
                raise serializers.ValidationError(msg)
        except Choice.DoesNotExist:
            pass
        except KeyError:
            pass

        return attrs


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
        read_only_fields = ('voted_by',)
        list_serializer_class = VoteListSerializer

    def create(self, validated_data):
        return Vote.objects.create(
            choice=validated_data.get('choice'),
            voted_by=self.context['request'].user,
        )

    def validate(self, attrs):
        try:
            choice = Choice.objects.get(pk=attrs['choice'].pk)
            question = choice.question
            multiple_choice = question.multiple_choice
            has_votes = Vote.objects.filter(
                choice__question=question,
                voted_by=self.context['request'].user,
            )
            if has_votes:
                msg = 'You have already voted'.format(multiple_choice)
                raise serializers.ValidationError(msg)
        except Choice.DoesNotExist:
            pass
        except KeyError:
            pass

        return attrs


class VoteResultsSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = Vote
        fields = ('id', 'choice',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user
