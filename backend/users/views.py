from .forms import LoginForm, SignUpForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import login as auth_login, authenticate
from django.views.generic import CreateView
from django.contrib.auth import views as auth_view
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(auth_view.LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('channels:channel_home')


class LogoutView(auth_view.LogoutView):
    success_url = reverse_lazy('users:login')


class SignupView(CreateView):
    form_class = SignUpForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('channels:channel_home')
    
    # formの検証が成功した場合に実行される
    def form_valid(self, form):
        # ユーザー作成後にログイン
        response = super().form_valid(form) # フォームの正常処理後のレスポンス取得
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        print(f"username: {username}, password: {password}")
        user = authenticate(self.request, username=username, password=password) # データベース内のユーザー情報を検証
        auth_login(self.request, user) # ログイン状態へ
        return response


# パスワード変更
class PasswordChange(auth_view.PasswordChangeView):
    print("PasswordChange")
    success_url = reverse_lazy('users:login')
    template_name = 'users/password_change.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Password changed successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = "password_change" # Djangoのフォームをそのまま使用
        return context


# Login API
@api_view(['POST'])
def login_api_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)  # トークンを返す
    else:
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)