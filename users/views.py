from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

from users.serializers import RegisterSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]