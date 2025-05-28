from rest_framework import serializers
from instructors.models import Instructor
from accounts.serializers import UserSerializers

class InstructorSerializer(serializers.ModelSerializer):
    # user = UserSerializers(read_only=True)
    class Meta:
        model = Instructor
        fields = "__all__"
        