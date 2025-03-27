import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PetConnect.settings')

import django
django.setup()

import random
from faker import Faker
from pets.models import UserProfile, Category, Post, Comment, Like, Forum, Pet

fake = Faker()

# Structured dictionary format
data = {
    "Users": [
        {"username": "lablover72", "email": "gabbysmith@example.com"},
        {"username": "petfan123", "email": "stevejobs@example.com"},
        {"username": "catdad4life", "email": "joshzimmerman@example.com"},
    ],
    "Pets": [
    {"name": "Cooper", "breed": "Labrador", "age": 4},
    {"name": "Layla", "breed": "Scottish Terrier", "age": 5},
    {"name": "Chip", "breed": "Tabby", "age": 2},
    ],
    "Categories": [
        {"category_name": "Dogs", "category_description": "All about dogs"},
        {"category_name": "Cats", "category_description": "All about cats"},
        {"category_name": "Birds", "category_description": "All about birds"},
    ],
    "Posts": [
        {"caption": "Cooper loves the beach!"},
        {"caption": "My fish doing backflips #swag"},
        {"caption": "Turtles are the superior animal."},
    ],
    "Comments": [
        {"comment_text": "Cool!"},
        {"comment_text": "Super cute!"},
        {"comment_text": "Your pet is so chill"},
    ],
    "Forum Questions": [
        {"question": "What’s the best food for a Poodle?"},
        {"question": "How do I train my kitten to use the litter box?"},
        {"question": "Are Bearded Dragons hard to take care of?"},
    ],
}


def add_user(username, email):
    user, created = UserProfile.objects.get_or_create(username=username, email=email)
    return user


def add_pet(owner, name, breed, age, description="A great pet"):
    pet, created = Pet.objects.get_or_create(owner=owner, name=name, breed=breed, age=age, description=description)
    return pet


def add_category(name, description):
    category, created = Category.objects.get_or_create(category_name=name, category_description=description)
    return category


def add_post(user, category, caption):
    post, created = Post.objects.get_or_create(user=user, category=category, caption=caption)
    return post


def add_comment(user, post, comment_text):
    comment, created = Comment.objects.get_or_create(user=user, post=post, comment_text=comment_text)
    return comment


def add_like(user, post):
    like, created = Like.objects.get_or_create(user=user, post=post)
    return like


def add_forum_question(user, question):
    forum, created = Forum.objects.get_or_create(user=user, question=question, answer=fake.paragraph())
    return forum


def populate():
    print("Populating database...")

    # Create users
    users = [add_user(u["username"], u["email"]) for u in data["Users"]]

    # Create pets
    for user, pet in zip(users, data["Pets"]):
        add_pet(user, pet["name"], pet["breed"], pet["age"])

    # Create categories
    categories = [add_category(c["category_name"], c["category_description"]) for c in data["Categories"]]

    # Create posts
    posts = [add_post(random.choice(users), random.choice(categories), p["caption"]) for p in data["Posts"]]

    # Create comments
    for post, comment in zip(posts, data["Comments"]):
        comment_user = random.choice([u for u in users if u != post.user])  # Ensure user isn't commenting on own post
        add_comment(comment_user, post, comment["comment_text"])

    # Create likes
    for _ in range(10):  # Create 10 random likes
        add_like(random.choice(users), random.choice(posts))

    # Create forum questions
    for q in data["Forum Questions"]:
        add_forum_question(random.choice(users), q["question"])

    print("Database populated successfully!")

    # Print out created objects
    print("\nUsers:")
    for user in UserProfile.objects.all():
        print(f"- {user.username}")

    print("\nCategories:")
    for category in Category.objects.all():
        print(f"- {category.category_name}")

    print("\nPosts:")
    for post in Post.objects.all():
        print(f"- {post.caption} by {post.user.username}")

    print("\nComments:")
    for comment in Comment.objects.all():
        print(f"- {comment.comment_text} on {comment.post.caption}")

    print("\nForum Questions:")
    for forum in Forum.objects.all():
        print(f"- {forum.question}")

if __name__ == "__main__":
    populate()

