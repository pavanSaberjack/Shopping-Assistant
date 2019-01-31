from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated

from . import serializers
from . import models
from . import permissions

# Create your views here.
class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profiles"""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email')

class LoginViewSet(viewsets.ViewSet):
    """Checks email and password and returns authtoken"""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """Use the ObtainAuthToken APIView to validate and create a token."""

        return ObtainAuthToken().post(request)


class ShoppingItemViewSet(viewsets.ModelViewSet):
    """Handles creating shopping item and adding it to user list"""

    # authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ShoppingItemSerializer
    queryset = models.ShoppingItem.objects.all()
    # permission_classes = (permissions.PostOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user."""

        serializer.save()


class ShoppingListItemViewSet(viewsets.ModelViewSet):
    """Handles creating shopping item and adding it to user list"""

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ShoppingListItemSerializer
    queryset = models.ShoppingListItem.objects.all()
    permission_classes = (permissions.AddToYourList, IsAuthenticated,)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user."""

        item_id = self.request.data.get("item_id", 0)

        print("Its hereeeeeee 2222222")

        item = models.ShoppingItem.objects.filter(id=item_id).first()

        print("Its hereeeeeee 333333")

        print(item)

        # user = models.UserProfile.objects.filter(id=1)[0]

        serializer.save(user_profile=self.request.user, shopping_item=item)
