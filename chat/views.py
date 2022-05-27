from django.contrib.humanize.templatetags.humanize import  intcomma
from django.shortcuts import redirect
from django.views import generic
from .models import Chat, Message
from django.views.generic import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User


class ChatDetail(LoginRequiredMixin, generic.DetailView):
    
    model = Chat
    paginate_by = 4
    context_object_name = 'chat'
    template_name = 'index.html'

