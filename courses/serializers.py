from rest_framework import serializers
from courses.models import Courses
from instructors.serializers import InstructorSerializer
from instructors.models import Instructor
class CoursesSerializers(serializers.ModelSerializer):
    instructor = InstructorSerializer()
    class Meta:
        model = Courses
        fields = "__all__"
    
    def create(self, validated_data):
        instructor_data = validated_data.pop("instructor")
        print(instructor_data)
        instructor = Instructor.objects.create(**instructor_data)
        return Courses.objects.create(instructor=instructor, **validated_data)
    
    def update(self, instance, validated_data):
        instructor_data = validated_data.get("instructor", None) 
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.created_on = validated_data.get("created_on", instance.created_on)
        instance.save()
        if instructor_data is not None:
            instructor = instance.instructor
            instructor.bio = instructor_data.get("bio", instructor.bio)
            instructor.user_id = instructor_data.get("user", instructor.user_id)
            instructor.save()
        return instance
