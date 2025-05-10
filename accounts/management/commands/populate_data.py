import random
import re
from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import User, UserBasicDetails
from instructors.models import Instructor
from courses.models import Courses
from enrollment.models import Enrollment
from reviews.models import Review
from django.db import transaction
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    # Initialize Faker instance
    fake = Faker()

    # Function to validate mobile number
    def valid_phone_number(self, phone_number):
        pattern = r"^\+91\d{10}$"  # India country code +91 followed by 10 digits
        return re.match(pattern, phone_number)

    # Function to create a User with valid mobile number and email
    def create_user(self):
        phone_number = None
        email = None
        
        # Ensure unique phone number and email
        while not phone_number or User.objects.filter(phone_number=phone_number).exists():
            phone_number = f"+91{self.fake.random_number(digits=10)}"
            if not self.valid_phone_number(phone_number):
                phone_number = None  # Re-generate if it's not valid
        
        while not email or User.objects.filter(email=email).exists():
            email = f"{self.fake.user_name()}@yopmail.com"
        
        user = User.objects.create_user(
            phone_number=phone_number,
            email=email,
            password="password123"  # Use a default password for all users
        )
        user.first_name = self.fake.first_name()
        user.last_name = self.fake.last_name()
        user.save()
        return user

    # Function to create User's Basic Details
    def create_user_basic_details(self, user):
        UserBasicDetails.objects.create(
            user=user,
            full_name=f"{user.first_name} {user.last_name}",
            gender=random.choice(['Female', 'Male', 'Other']),
            profile_image=f"user_profile/{random.choice(['user1.jpg', 'user2.jpg', 'user3.jpg'])}",
            date_of_birth=self.fake.date_of_birth(minimum_age=18, maximum_age=65),
            aadhaar_number=self.fake.random_int(min=100000000000, max=999999999999)
        )

    # Function to create an Instructor
    def create_instructor(self, user):
        Instructor.objects.create(user=user, bio=self.fake.text())

    # Function to create a Course
    def create_course(self):
        instructor = random.choice(Instructor.objects.all())
        course = Courses.objects.create(
            title=self.fake.bs(),
            description=self.fake.text(),
            instructor=instructor,
            created_on=timezone.now()  # Ensure that created_on is set
        )
        return course

    # Function to create Enrollment
    def create_enrollment(self):
        student = random.choice(User.objects.all())
        course = random.choice(Courses.objects.all())
        Enrollment.objects.create(
            student=student,
            course=course,
            enrolled_on=self.fake.date_this_year(),
            completed=random.choice([True, False])
        )

    # Function to create Review
    def create_review(self):
        student = random.choice(User.objects.all())
        course = random.choice(Courses.objects.all())
        Review.objects.create(
            course=course,
            student=student,
            rating=random.randint(1, 5),
            comment=self.fake.text(),
            created_on=self.fake.date_this_year()
        )

    # Main Function to populate dummy data
    @transaction.atomic
    def handle(self, *args, **kwargs):
        # Create Users and their details
        for _ in range(20):  # Create 20 dummy users
            user = self.create_user()
            self.create_user_basic_details(user)
        
        # Create Instructors
        for _ in range(5):  # Create 5 instructors
            user = self.create_user()  # Instructor is also a User
            self.create_instructor(user)

        # Create Courses
        for _ in range(10):  # Create 10 courses
            self.create_course()

        # Create Enrollments
        for _ in range(30):  # Create 30 enrollments
            self.create_enrollment()

        # Create Reviews
        for _ in range(20):  # Create 20 reviews
            self.create_review()

        self.stdout.write(self.style.SUCCESS('Data population completed successfully!'))
