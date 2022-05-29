from django.contrib.humanize.templatetags.humanize import  intcomma
from django.shortcuts import redirect
from django.views import generic
from .models import Chat, Message
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q


class ChatDetail(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('login')
    model = Message
    paginate_by = 12
    context_object_name = 'messages'
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chat_id = self.kwargs.get('pk')
        context['chat'] = Chat.objects.get(pk=chat_id)
        context['active_tab'] = 'chat'
        return context

    def get_queryset(self):
        chat_id = self.kwargs.get('pk')
        return Message.objects.filter(chat=Chat.objects.get(pk=chat_id)).order_by("-time")

    def get(self, request, *args, **kwargs):
        chat_id = self.kwargs.get('pk')
        chat = Chat.objects.get(pk=chat_id)
        if (chat.user1 != self.request.user and chat.user2 != self.request.user) or chat.active == False :
            return redirect("blog:index")
        return super(ChatDetail, self).get(self, request, *args, **kwargs)

class ChatSideMenu(LoginRequiredMixin,  generic.View):
    def get(self, request, *args, **kwargs):
        chat = Chat.objects.filter((Q(user1 = request.user) | Q(user2 = request.user))&Q(active=True)).order_by('-last_message').first()

        if chat:
            return redirect('chat:chat_detail', chat.id)

        return render(request, "no_chats.html")
        
class FriendChat(LoginRequiredMixin,  generic.View):
    def get(self, request, *args, **kwargs):
        user1 = request.user
        user2 = User.objects.get(pk=kwargs.get('pk'))
        chat = Chat.objects.filter(
            ( (Q(user1 = user1) & Q(user2 = user2)) | (Q(user2 = user1) & Q(user1 = user2))) 
            & Q(active=True) ).first()
            
        if chat:
            return redirect('chat:chat_detail', chat.id)

        return render(request, "no_chats.html")

        
        
