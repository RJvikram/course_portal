from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import UserBasicDetails
from django.db import transaction
User = get_user_model()
from django.core.validators import RegexValidator

class UserSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)  # <-- Add this line
    first_name = serializers.CharField(max_length=150, min_length=2, required=True)
    last_name = serializers.CharField(max_length=150, min_length=2, required=True)
    phone_number = serializers.CharField(max_length=13,
            validators=[
                RegexValidator(regex=r'^\+91\d{10}$', message="Phone number must start with +91 and have 10 digits.")
            ]
        )
    email = serializers.EmailField(required=True, allow_blank=False)

    def validate_phone_number(self, value):
        if not value.startswith("+91"):
            raise serializers.ValidationError("Phone number must start with +91.")
        return value
    
    def validate(self, data):
        if data["first_name"] == data["last_name"]:
            raise serializers.ValidationError("First name and last name cannot be the same.")
        return data

    def create(self, validated_data):
        return User.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        instance.email = validated_data.get("email", instance.email)
        instance.save()
        return instance
    
class UserBasicSerializers(serializers.ModelSerializer):
    user = UserSerializers()
    class Meta:
        model = UserBasicDetails
        exclude = ["full_name"]

    def validate_aadhaar_number(self, value):
        if value and len(value) != 12:
            raise serializers.ValidationError("Aadhaar number must be 12 digits.")
        return value
    
    def validate(self, data):
        if data['gender'] == 'Other' and not data.get('profile_image'):
            raise serializers.ValidationError("Profile image is mandatory if gender is 'Other'")
        return data


    def create(self, validated_data):
        user_data = validated_data.pop("user")
        with transaction.atomic():
            user = User.objects.create(**user_data)
            basic_details = UserBasicDetails.objects.create(user=user, **validated_data)
        return basic_details