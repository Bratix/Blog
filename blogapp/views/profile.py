from django.shortcuts import redirect
from ..models import Friend_Request, Profile, Notification
from chat.models import Chat
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy, reverse
from .constants import NOTIFICATION_FRIEND_REQUEST_ACCEPTED
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q



class ProfileDetail(LoginRequiredMixin, DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'profile/detail.html'

    def get(self, request, *args, **kwargs):
        Notification.objects.filter(Q(user = request.user) & Q(type = NOTIFICATION_FRIEND_REQUEST_ACCEPTED) & Q(url = request.get_full_path())).delete()
        return super().get(request, *args, **kwargs)

    def get_object(self):
        profile_id = self.kwargs['pk']
        return Profile.objects.get(pk = profile_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        friend_request = Friend_Request.objects.filter( Q(reciever = self.request.user) &  Q(submitter = profile.user ) &  Q(active = True))
              
        if len(friend_request) > 0:
            context['friend_request_id'] = friend_request[0].id

        
        if self.request.user in profile.friends.all():
            chat = Chat.objects.filter((Q(user1 = profile.user) & Q(user2 = self.request.user)) | 
                                       (Q(user2 = profile.user) & Q(user1 = self.request.user))).first()
            chat_url = reverse("chat:chat_detail", args=[chat.id])
            context['chat_url'] = chat_url

        return context
        

class ProfileEdit(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Profile
    template_name = "profile/edit.html"
    fields = ['first_name', 'last_name', 'image']

    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        if profile.user != self.request.user:
            return redirect("blog:index")
        return super(ProfileEdit, self).get(self, request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        profile = self.get_object()
        if profile.user != self.request.user:
            return redirect("blog:index")
        return super(ProfileEdit, self).post(self, request, *args, **kwargs)