from django.dispatch import receiver
from django.views import generic, View
from django.shortcuts import render
from ..models import Friend_Request, Profile, Notification
from chat.models import Chat
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .constants import FRIEND_REQUEST, FRIENDS, NOTIFICATION_FRIEND_REQUEST, NOTIFICATION_FRIEND_REQUEST_ACCEPTED
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.core import serializers
import json
from datetime import  timedelta
from dateutil.relativedelta import *
from dateutil import parser

class GetNotifications(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.user.is_authenticated :
            notifications = Notification.objects.filter(Q(user=request.user))

            data = json.loads(serializers.serialize('json',notifications))          
            return JsonResponse(data,safe=False)


class NewNotifications(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.user.is_authenticated :
            last_time =parser.isoparse(kwargs.get('last_time'))
            notifications = Notification.objects.filter(Q(user=request.user) & Q(created_at__gte =last_time + timedelta(seconds=1)))
            data = json.loads(serializers.serialize('json',notifications))         
            
            return JsonResponse(data,safe=False)


class DeleteNotification(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            notification = Notification.objects.get(id=kwargs['pk'])
            if notification.user == request.user:
                Notification.objects.get(id=kwargs.get('pk')).delete()

            data = {
            'status': 'success'
            }
            
            return JsonResponse(data, safe=False)