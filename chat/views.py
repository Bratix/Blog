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
from django.db.models import Q


class ChatDetail(LoginRequiredMixin, generic.DetailView):
    login_url = reverse_lazy('login')
    model = Chat
    paginate_by = 4
    context_object_name = 'chat'
    template_name = 'index.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'chat'
        return context

    def get(self, request, *args, **kwargs):
        chat = self.get_object()
        if (chat.user1 != self.request.user and chat.user2 != self.request.user) or chat.active == False :
            return redirect("blog:index")
        return super(ChatDetail, self).get(self, request, *args, **kwargs)

class ChatSideMenu(LoginRequiredMixin,  generic.View):
    def get(self, request, *args, **kwargs):
        chat = Chat.objects.filter((Q(user1 = request.user) | Q(user2 = request.user))&Q(active=True)).order_by('-last_message').first()

        if chat:
            return redirect('chat:chat_detail', chat.id)

        return render(request, "no_chats.html")
        

        
        
