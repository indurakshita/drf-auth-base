from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import UserRegisterSerializer

@api_view(["POST"])
def logout_user(request):
    if request.method == "POST":
        request.user.auth_token.delete()
        return Response({"Message": "Logout Successfully"}, status=status.HTTP_200_OK)

@api_view(["POST"])
def user_register_view(request):
    if request.method == "POST":
        serializer = UserRegisterSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            account = serializer.save()
            data["response"] = "Account has been created"
            data["username"] = account.username

            # Avoid including password in the response

            # Generate the URL dynamically using reverse
            login_url = reverse('login')  # 'login' is the name of your login URL pattern

            data['login_url'] = request.build_absolute_uri(login_url)

            token = Token.objects.get(user=account).key
            data['token'] = token

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors

        return Response(data, status=status.HTTP_400_BAD_REQUEST)
