import os, sys
from unicodedata import category
sys.path.append('..')
os.environ['DJANGO_SETTINGS_MODULE'] = 'Blog.settings'
import django
import json
django.setup()
from django.contrib.auth.models import User
from blogapp.models import Category, Profile, Blog, Post, Comment
from chat.models import Chat
import glob, random
from django.core.files import File
import uuid 



def createUserAndProfile(row):
    user = User.objects.create(username=row['username'],
        password=row['password'],
        email=row['email'])

        
    file_path_type = ["./dataset/users/**/*.jpg"]
    images = glob.glob(random.choice(file_path_type))
    random_image = random.choice(images)
    picture = File(open(random_image, 'rb'))

    profile = Profile.objects.create(user = user,
        first_name=row['first_name'],
        last_name=row['last_name'])
    
    profile.image.save("image", picture)

def createCategories():
    list = ['Art', 'Business', 'DIY', 'Fashion', 'Food', 'Health and fitness', 'Movie', 'Music', 'News', 'Other', 'Personal', 'Photography', 'Sport', 'Travel']

    for name in list:
        category = Category.objects.create(name=name)

def createBlog(row):

    file_path_type = ["./dataset/blog/*.jpg"]
    images = glob.glob(random.choice(file_path_type))
    random_image = random.choice(images)
    picture = File(open(random_image, 'rb'))
    random_string=uuid.uuid4().hex[:6].upper()
    blog = Blog.objects.create(author=User.objects.all().order_by('?').first(),
        category=Category.objects.all().order_by('?').first(),
        title=row['title']+random_string,
        description=row['description'])
    blog.image.save('image', picture)

    random_moderator_ammount = random.randint(0,15)
    moderators = User.objects.exclude(pk=blog.author.pk).order_by('?')[:random_moderator_ammount]
    for moderator in moderators:
        blog.moderators.add(moderator)

    random_subscriber_ammount = random.randint(0,180)
    subscribers = User.objects.exclude(pk=blog.author.pk).order_by('?')[:random_subscriber_ammount]
    for subscriber in subscribers:
        blog.subscribers.add(subscriber)


def createFriends():
    users = User.objects.order_by('username')[:70]
    users2 = User.objects.order_by('username')[70:140]

    select = [0, 1, 2]
    for user in users:
        for user2 in users2:
            if random.choice(select) == 0:
                continue
            user.profile.friends.add(user2)
            user2.profile.friends.add(user)

            Chat.objects.create(
                user1 = user,
                user2 = user2
            )

def createPost(row):

    file_path_type = ["./dataset/post/**/*.jpg"]
    images = glob.glob(random.choice(file_path_type))
    random_image = random.choice(images)
    picture = File(open(random_image, 'rb'))

    post = Post.objects.create(author=User.objects.all().order_by('?').first(),
        blog=Blog.objects.all().order_by('?').first(),
        title=row['title'],
        subtitle=row['subtitle'],
        text=row['text'])
    post.tags.add(row['tags'])
    post.image.save('image', picture)

    random_ammount = random.randint(0,100)
    likes = User.objects.all().order_by('?')[:random_ammount]
    for user in likes:
        post.likes.add(user)

def createComment(row):

    Comment.objects.create(author=User.objects.all().order_by('?').first(),
        post=Post.objects.all().order_by('?').first(),
        text=row['text'],)


f = open('./user_mock.json')
data = json.load(f)

i=0
for row in data:
    createUserAndProfile(row)
    i = i + 1
    if i == 250:
        break

createFriends()
createCategories()

f = open('./blog_mock.json')
data = json.load(f)

i=0
for row in data:
    createBlog(row)
    i = i + 1
    if i == 50:
        break

f = open('./post_mock.json')
data = json.load(f)

i=0
for row in data:
    createPost(row)
    i = i + 1
    if i == 700:
        break

f = open('./comment_mock.json')
data = json.load(f)

i=0
for row in data:
    createComment(row)
    i = i + 1
    if i == 1000:
        break