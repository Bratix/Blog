from django.views import generic, View
from django.views.generic import CreateView, DeleteView, UpdateView, RedirectView
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User
import json
from django.core import serializers
from django.http import JsonResponse
# from operator import and_, or_
# import functools
# from django.db.models import Q


BROWSE = 'browse'
BLOG = 'blog'
SUBSCRIBED = 'subscribed'
NEW_BLOG = 'new_blog'
CATEGORY = "category"






    
