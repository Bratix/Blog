from django.views import generic, View
from django.shortcuts import render
from ..models import Friend_Request, Profile
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .views import FRIEND_REQUEST, FRIENDS
from django.urls import reverse_lazy
from django.http import JsonResponse


class FriendList(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('login')
    model = Profile
    paginate_by = 4
    context_object_name = 'friends'
    template_name = 'friend/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = FRIENDS
        return context

    def get_queryset(self):
        return self.request.user.friends.order_by('user__username')

class RecievedFriendRequestList(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('login')
    model = Friend_Request
    paginate_by = 20
    context_object_name = 'friend_requests'
    template_name = 'friend_request/recieved.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = FRIEND_REQUEST
        return context

    def get_queryset(self):
        return Friend_Request.objects.filter(Q(reciever = self.request.user) &  Q(active = True)  ).order_by('-send_date')

class SentFriendRequestList(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('login')
    model = Friend_Request
    paginate_by = 10
    context_object_name = 'friend_requests'
    template_name = 'friend_request/sent.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = FRIEND_REQUEST
        return context

    def get_queryset(self):
        return Friend_Request.objects.filter(Q(submitter = self.request.user) &  Q(active = True)).order_by('-send_date')

class AcceptFriendRequest(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            friend_request_id = kwargs.get('pk')
            friend_request = Friend_Request.objects.get(id = friend_request_id)

            if request.user.is_authenticated and request.user == friend_request.reciever :
                friend_request.submitter.profile.friends.add(friend_request.reciever)
                friend_request.reciever.profile.friends.add(friend_request.submitter)
                friend_request.submitter.profile.pending_friends.remove(friend_request.reciever)
                friend_request.active = False
                friend_request.save()
                data = {
                'status': 'success'
                }
            
            return JsonResponse(data)

class CancelFriendRequest(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            friend_request_id = kwargs.get('pk')
            friend_request = Friend_Request.objects.get(id = friend_request_id)

            if request.user.is_authenticated and (request.user == friend_request.reciever or request.user == friend_request.submitter):
                friend_request.active = False
                friend_request.submitter.profile.pending_friends.remove(friend_request.reciever)
                friend_request.save()
                data = {
                'status': 'success'
                }
            
            return JsonResponse(data)

class SendFriendRequest(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            reciever_id = kwargs.get('pk')
            reciever = Profile.objects.get(pk=reciever_id)
            reciever = reciever.user

            friend_requests = Friend_Request.objects.filter(
                (Q(reciever = reciever) & Q(submitter = request.user) &  Q(active = True))  |
                (Q(reciever = request.user) & Q(submitter = reciever) & Q(active = True))
            )


            if not (len(friend_requests) > 0) and reciever != request.user:
                friend_request = Friend_Request.objects.create(
                    submitter = request.user,
                    reciever = reciever,
                    active = True
                )
                request.user.profile.pending_friends.add(reciever)
                data = {
                    "status" : 'success'
                }
            else:
                data = { 
                    "status" : 'failed',
                    "message" : 'This friend request already exists or this user sent you a friend request already'
                }
            
            return JsonResponse(data)

class DeleteFriend(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            reciever_id = kwargs.get('pk')
            reciever = Profile.objects.get(pk=reciever_id)

            request.user.profile.friends.remove(reciever.user)
            reciever.friends.remove(request.user)
            data = {
                "status" : 'success'
            }
            return JsonResponse(data)
