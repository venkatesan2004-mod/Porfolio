from rest_framework import serializers
from .models import *
import base64

class SkillsMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillsMaster
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

 

class ProfileSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = "__all__"

    def get_photo(self, obj):
        if obj.photo:
            encoded = base64.b64encode(obj.photo).decode("utf-8")
            return f"data:{obj.photo_type};base64,{encoded}"
        return None