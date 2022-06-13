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


class FriendList(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('login')
    model = Profile
    paginate_by = 16
    context_object_name = 'friends'
    template_name = 'friend/detail.html'

    def get(self, request, *args, **kwargs):
        Notification.objects.filter(Q(user = request.user) & Q(type = NOTIFICATION_FRIEND_REQUEST_ACCEPTED)).delete()
        return super().get(request, *args, **kwargs)

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

    def get(self, request, *args, **kwargs):
        Notification.objects.filter(Q(user = request.user) & Q(type = NOTIFICATION_FRIEND_REQUEST)).delete()
        return super().get(request, *args, **kwargs)
    
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
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            friend_request_id = kwargs.get('pk')
            friend_request = Friend_Request.objects.get(id = friend_request_id)

            if request.user.is_authenticated and request.user == friend_request.reciever :
                friend_request.submitter.profile.friends.add(friend_request.reciever)
                friend_request.reciever.profile.friends.add(friend_request.submitter)
                friend_request.submitter.profile.pending_friends.remove(friend_request.reciever)
                friend_request.active = False
                friend_request.save()
                inactive_chat = Chat.objects.filter(
                    ((Q(user1 = friend_request.submitter) & Q(user2 = friend_request.reciever)) | 
                    (Q(user2 = friend_request.submitter) & Q(user1 = friend_request.reciever))) & Q(active=False) ).first()
                
                Notification.objects.create(
                    user = friend_request.submitter,
                    thumb_image = friend_request.reciever.profile.image.url,
                    title = "Friend request accepted",
                    url = reverse('blog:profile_detail', args=[friend_request.reciever.profile.id]),
                    text = friend_request.reciever.username + " accepted your friend request",
                    type = NOTIFICATION_FRIEND_REQUEST_ACCEPTED
                )


                if inactive_chat: 
                    inactive_chat.active = True
                    inactive_chat.save()
                else:
                    Chat.objects.create(
                        user1 = friend_request.submitter,
                        user2 = friend_request.reciever
                    )

                data = {
                'status': 'success'
                }
            
            return JsonResponse(data)

class CancelFriendRequest(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
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
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            reciever_id = kwargs.get('pk')
            reciever = Profile.objects.get(pk=reciever_id)
            reciever = reciever.user

            friend_requests = Friend_Request.objects.filter(
                (Q(reciever = reciever) & Q(submitter = request.user) &  Q(active = True))  |
                (Q(reciever = request.user) & Q(submitter = reciever) & Q(active = True))
            )


            if not (len(friend_requests) > 0) and reciever != request.user:
                Friend_Request.objects.create(
                    submitter = request.user,
                    reciever = reciever,
                    active = True
                )
                request.user.profile.pending_friends.add(reciever)

                Notification.objects.create(
                    user = reciever,
                    thumb_image = request.user.profile.image.url,
                    title = "New friend request",
                    url = reverse('blog:recieved_friend_requests'),
                    text = request.user.username + " sent you a friend request",
                    type = NOTIFICATION_FRIEND_REQUEST
                )
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
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            reciever_id = kwargs.get('pk')
            reciever = Profile.objects.get(pk=reciever_id)

            request.user.profile.friends.remove(reciever.user)
            reciever.friends.remove(request.user)
            print("Reciever : ", reciever.user, "Submitter:", request.user)
            active_chat = Chat.objects.filter(
                ((Q(user1 = request.user) & Q(user2 = reciever.user)) | 
                (Q(user2 = request.user) & Q(user1 = reciever.user))) & Q(active=True) ).first()
            print(active_chat)
            active_chat.active = False
            active_chat.save()

            data = {
                "status" : 'success'
            }
            return JsonResponse(data)
