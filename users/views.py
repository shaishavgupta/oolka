from rest_framework import generics, status
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer

# Create your views here.
class SignupView(generics.ListCreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        name = request.data.get("name")
        email = request.data.get("email")
        password = request.data.get("password")

        if not name:
            return Response({"message": "name is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not email:
            return Response({"message": "email is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({"message": "password is required"}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(email=email, defaults={"name": name, "password": hash(password)})

        if created:
            return Response({"message": "user created", "data":self.serializer_class(user).data}, status=status.HTTP_201_CREATED)
        
        return Response({"message": "user already exists", "data": self.serializer_class(user).data}, status=status.HTTP_200_OK)
