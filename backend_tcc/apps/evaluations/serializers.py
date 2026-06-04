from rest_framework import serializers
from .models import (
    EvaluationQuestion,
    EvaluationResponse,
    EvaluationAnswer,
    StandardQuestion,
)


class StandardQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StandardQuestion
        fields = ["id", "text", "question_type", "order", "is_active"]


class EvaluationQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationQuestion
        fields = ["id", "course", "text", "question_type", "order"]


class EvaluationAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationAnswer
        fields = ["id", "question", "scale_value", "text_value"]


class EvaluationResponseSerializer(serializers.ModelSerializer):
    answers = EvaluationAnswerSerializer(many=True)

    class Meta:
        model = EvaluationResponse
        fields = ["id", "course", "submitted_at", "external_response_id", "answers"]
        read_only_fields = ["submitted_at"]

    def create(self, validated_data):
        answers_data = validated_data.pop("answers", [])
        response = EvaluationResponse.objects.create(**validated_data)

        for answer_data in answers_data:
            EvaluationAnswer.objects.create(response=response, **answer_data)

        return response
