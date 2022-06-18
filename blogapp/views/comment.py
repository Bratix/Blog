from django.contrib.humanize.templatetags.humanize import naturalday, intcomma, naturaltime
from ..models import Post, Comment
from django.views.generic import CreateView, DeleteView, UpdateView
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
import datetime
from django.core.exceptions import PermissionDenied



class CommentCreate(CreateView):
    model = Comment
    fields = ['text']

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse(form.errors, status=400)
        else:
            return response
        
    def form_valid(self, form): 
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
        response = super(CommentCreate, self).form_valid(form)

        #if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'pk' : self.object.pk,
            'text' : self.object.text,
            'user' : str(self.object.author),
            'image' : "random",
            'creation_date' : naturaltime(self.object.creation_date),
            'comment_count' : intcomma(self.object.post.comment_set.count()),
            'update_link' : reverse("blog:comment_update", args=[self.object.pk]),
            'delete_link' : reverse("blog:comment_delete", args=[self.object.pk])
        }
        return JsonResponse(data)
        #else:
            #return response

        

class CommentUpdate(UpdateView):
    model = Comment
    fields = ['text']

    def post(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != self.request.user:
            return redirect("blog:index")
        return super(CommentUpdate, self).post(self, request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.edited = True
        form.instance.edit_date = datetime.datetime.now()
        response = super(CommentUpdate, self).form_valid(form)

        #if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'pk' : self.object.pk,
            'text' : self.object.text,
            'user' : str(self.object.author),
            'creation_date' : naturaltime(self.object.edit_date),
            'edited' : self.object.edited,
            'comment_count' : self.object.post.comment_set.count(),
        }
        return JsonResponse(data)
        #else:
            #return response

class CommentDelete(DeleteView):
    model = Comment

    def post(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != self.request.user:
            return redirect("blog:index")
        return super(CommentDelete, self).post(self, request, *args, **kwargs)

    def form_valid(self, form):
            comment_id = self.kwargs['pk']
            Comment = Comment.objects.get(pk=comment_id)
            if Comment.author != self.request.user:
                raise PermissionDenied()
            return super(CommentDelete, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',kwargs = {'pk': Comment.objects.get(id=self.kwargs['pk']).post.id})

