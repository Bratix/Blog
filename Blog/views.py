from django.views import generic
from django.views.generic import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm

class UserFormView(View):
    form_class = UserForm
    template_name = 'registration/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            
            #cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            #returns User objects if credentials are correct
            user = authenticate(username = username, password = password)

            if user is not None:

                if user.is_active:

                    login(request, user)
                    return redirect('blog:index')

        return render(request, self.template_name, {'form':form})