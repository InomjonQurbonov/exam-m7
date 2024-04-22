import random
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model, update_session_auth_hash, login, logout
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, DetailView
from drf_yasg.openapi import Response
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from config.settings import EMAIL_HOST_USER
from .forms import RegistrationForm
from .serializers import UserSerializer, ChangePasswordSerializer
from django.contrib.auth.models import User


def send_email_view(request):
    if request.method == 'POST':
        email_subject = request.POST['subject']
        email_message = request.POST['message']
        email_from = EMAIL_HOST_USER
        email_to = [user.email for user in User.objects.all()]

        try:
            send_mail(email_subject, email_message, email_from, email_to)
            return HttpResponse('<h1>Email sent!</h1>')
        except Exception as e:
            return HttpResponse(f'<h1>Something went wrong</h1><p>{e}</p>', status=500)
    return render(request, 'superuser/email_message.html')


class RegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        login(self.request, user)
        return redirect(self.success_url)


class UserLogInView(LoginView):
    template_name = 'registration/login.html'
    next_page = reverse_lazy('home')


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class UserDetailView(DetailView):
    model = User
    template_name = 'superuser/user.html'


class SendVerificationEmailView(View):
    def get(self, request):
        return render(request, 'registration/confirm_mail.html')

    def post(self, request):
        email = request.POST.get('email')
        verification_code = random.randint(100000, 999999)
        user = get_user_model().objects.get(email=email)
        user.profile.verification_code = verification_code
        user.profile.save()
        email_subject = 'Your email verification code'
        email_body = f'Your verification code is: {verification_code}'
        send_mail(email_subject, email_body, 'your-email@example.com', [email])
        return render(request, 'registration/confirm_send_email.html')


class RegisterAPIView(CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
