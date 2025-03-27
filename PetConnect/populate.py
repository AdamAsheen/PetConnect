import os
import django
import random
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PetConnect.settings')
django.setup()

from django.contrib.auth.models import User
from pets.models import UserProfile, Pet, Category, Post, Comment, Like, ChatRoom, Message, FavoriteCategory, Forum

fake = Faker()
pet_breeds = ["Labrador", "Golden Retriever", "Poodle", "Goldfish", "Siamese", "Persian", "Parrot", "Hamster", "Budgie"]

def add_user(username, email):
    user, _ = User.objects.get_or_create(username=username, email=email)
    user.set_password('password123')
    user.save()
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile

def add_pet(owner):
    return Pet.objects.create(
        owner=owner,
        name=fake.first_name(),
        breed=random.choice(pet_breeds),
        age=random.randint(1, 10),
        description=fake.sentence(),
        image='pet_images/default.jpg'
    )

def add_category(name, desc):
    category, _ = Category.objects.get_or_create(category_name=name, category_description=desc)
    return category

def add_post(user, category, caption):
    return Post.objects.create(
        user=user,
        category=category,
        title=caption,
        caption = caption,
        image='post_images/default.jpg'
    )

def add_comment(user, post, text):
    return Comment.objects.create(user=user, post=post, comment_text=text)

def add_like(user, post):
    return Like.objects.get_or_create(user=user, post=post)

def add_help_question(user, question):
    return Forum.objects.create(user=user, question=question, answer=fake.sentence())

def add_help_entry(user):
    return Forum.objects.create(
        user=user,
        question=fake.sentence(nb_words=8),
        answer=fake.paragraph(),
        image='help_images/default.jpg'
    )

def add_favorite_category(user, category):
    return FavoriteCategory.objects.get_or_create(user=user, category=category)

def create_chatroom(name, users):
    chat = ChatRoom.objects.create(chat_name=name)
    for u in users:
        chat.users.add(u.user)
    return chat

def add_message(chat, sender):
    return Message.objects.create(
        chat_room=chat,
        sender=sender.user,
        content=fake.sentence()
    )

def populate():
    print("Populating database...")

    users = [add_user(u["username"], u["email"]) for u in [{'username': 'lablover72', 'email': 'gabbysmith@example.com'}, {'username': 'petfan123', 'email': 'stevejobs@example.com'}, {'username': 'catdad4life', 'email': 'joshzimmerman@example.com'}]]
    categories = [add_category(c["category_name"], c["category_description"]) for c in [{'category_name': 'Dogs', 'category_description': 'All about dogs'}, {'category_name': 'Cats', 'category_description': 'All about cats'}, {'category_name': 'Birds', 'category_description': 'All about birds'}]]
    posts = [add_post(random.choice(users), random.choice(categories), p["caption"]) for p in [{'caption': 'Cooper loves the beach!'}, {'caption': 'My fish doing backflips #swag'}, {'caption': 'Turtles are the superior animal.'}]]

    for post in posts:
        commenters = random.sample(users, k=2)
        for commenter in commenters:
            if commenter != post.user:
                sample_comments = [
                    "Cute!",
                    "Love this!",
                    "Where was this taken?",
                    "What a cool pet!",
                    "So adorable!"
                ]
                add_comment(commenter, post, random.choice(sample_comments))
        likers = random.sample(users, k=random.randint(1, len(users)))
        for liker in likers:
            add_like(liker, post)

    for user in users:
        add_pet(user)
        fav_cat = random.choice(categories)
        add_favorite_category(user, fav_cat)

    for q in [{'question': 'What’s the best food for a Poodle?'}, {'question': 'How do I train my kitten to use the litter box?'}, {'question': 'Are Bearded Dragons hard to take care of?'}]:
        add_help_question(random.choice(users), q["question"])
    
    for _ in range(3):
        add_help_entry(random.choice(users))

    # Create chatrooms and messages
    chatroom = create_chatroom("AnimalLovers", users)
    for _ in range(5):
        add_message(chatroom, random.choice(users))

    print("Database populated successfully!")

if __name__ == "__main__":
    populate()
