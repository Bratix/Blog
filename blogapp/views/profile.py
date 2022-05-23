from audioop import reverse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from ..models import Profile
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy
from .views import BROWSE, BLOG, NEW_BLOG
from django.contrib.auth.mixins import LoginRequiredMixin



class ProfileDetail(LoginRequiredMixin, DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'profile/detail.html'

    def get_object(self):
        profile_id = self.kwargs['pk']
        return Profile.objects.get(pk = profile_id)

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