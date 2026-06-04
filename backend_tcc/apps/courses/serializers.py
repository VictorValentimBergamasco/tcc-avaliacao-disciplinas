from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    professor_name = serializers.SerializerMethodField()
    qr_code_url = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "code",
            "professor",
            "professor_name",
            "google_form_link",
            "qr_code_image",
            "qr_code_url",
            "is_active",
            "created_at",
        ]

    def get_professor_name(self, obj):
        return f"{obj.professor.first_name} {obj.professor.last_name}".strip() or obj.professor.institutional_email

    def get_qr_code_url(self, obj):
        request = self.context.get("request")
        if obj.qr_code_image and request:
            return request.build_absolute_uri(obj.qr_code_image.url)
        return obj.qr_code_image.url if obj.qr_code_image else None
