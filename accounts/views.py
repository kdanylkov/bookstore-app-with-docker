from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate

from accounts.forms import CustomUserCreationForm


class SignUpPageView(CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')

        user = authenticate(
                self.request,
                username=username,
                password=password
                )
        login(request=self.request, user=user)

        return response
