import os
import django
import random
import re
from faker import Faker
from django.utils import timezone
from accounts.models import User, UserBasicDetails
from instructors.models import Instructor
from courses.models import Courses
from enrollment.models import Enrollment
from reviews.models import Review
from django.db import transaction

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course_portal.settings')
django.setup()

# Initialize Faker instance
fake = Faker()

# Function to validate mobile number
def valid_phone_number(phone_number):
    pattern = r"^\+91\d{10}$"  # India country code +91 followed by 10 digits
    return re.match(pattern, phone_number)

# Function to create a User with valid mobile number and email
def create_user():
    phone_number = None
    email = None
    
    # Ensure unique phone number and email
    while not phone_number or User.objects.filter(phone_number=phone_number).exists():
        phone_number = f"+91{fake.random_number(digits=10)}"
        if not valid_phone_number(phone_number):
            phone_number = None  # Re-generate if it's not valid
    
    while not email or User.objects.filter(email=email).exists():
        email = f"{fake.user_name()}@yopmail.com"
    
    user = User.objects.create_user(
        phone_number=phone_number,
        email=email,
        password="password123"  # Use a default password for all users
    )
    user.first_name = fake.first_name()
    user.last_name = fake.last_name()
    user.save()
    return user

# Function to create User's Basic Details
def create_user_basic_details(user):
    UserBasicDetails.objects.create(
        user=user,
        full_name=f"{user.first_name} {user.last_name}",
        gender=random.choice(['Female', 'Male', 'Other']),
        profile_image=f"user_profile/{random.choice(['user1.jpg', 'user2.jpg', 'user3.jpg'])}",
        date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=65),
        aadhaar_number=fake.random_int(min=100000000000, max=999999999999)
    )

# Function to create an Instructor
def create_instructor(user):
    Instructor.objects.create(user=user, bio=fake.text())

# Function to create a Course
def create_course():
    instructor = random.choice(Instructor.objects.all())
    course = Courses.objects.create(
        title=fake.bs(),
        description=fake.text(),
        instructor=instructor
    )
    return course

# Function to create Enrollment
def create_enrollment():
    student = random.choice(User.objects.all())
    course = random.choice(Courses.objects.all())
    Enrollment.objects.create(
        student=student,
        course=course,
        enrolled_on=fake.date_this_year(),
        completed=random.choice([True, False])
    )

# Function to create Review
def create_review():
    student = random.choice(User.objects.all())
    course = random.choice(Courses.objects.all())
    Review.objects.create(
        course=course,
        student=student,
        rating=random.randint(1, 5),
        comment=fake.text(),
        created_on=fake.date_this_year()
    )

# Main Function to populate dummy data
@transaction.atomic
def populate_data():
    # Create Users and their details
    for _ in range(20):  # Create 20 dummy users
        user = create_user()
        create_user_basic_details(user)
    
    # Create Instructors
    for _ in range(5):  # Create 5 instructors
        user = create_user()  # Instructor is also a User
        create_instructor(user)

    # Create Courses
    for _ in range(10):  # Create 10 courses
        create_course()

    # Create Enrollments
    for _ in range(30):  # Create 30 enrollments
        create_enrollment()

    # Create Reviews
    for _ in range(20):  # Create 20 reviews
        create_review()

    print("Data population completed successfully!")

if __name__ == "__main__":
    populate_data()
