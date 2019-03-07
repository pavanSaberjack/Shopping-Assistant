from django.shortcuts import render

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView

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

    def list(self, serializer, *kwargs):

        queryset = models.ShoppingListItem.objects.filter(user_profile=self.request.user.id)

        item_list = []
        for shoppingListItem in queryset:
            item_id = shoppingListItem.shopping_item.id
            item = models.ShoppingItem.objects.filter(id=item_id).first()
            item_list.append(item)

        results = serializers.ShoppingItemSerializer(item_list, many=True).data
        return Response(results)


        # queryset = models.ShoppingListItem.objects.filter(user_profile=self.request.user.id)
        #
        # return Response({ 'result': serializers.ResponseShoppingListItemSerializer(queryset, many=True).data })

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user."""
        item_id = self.request.data.get("shopping_item", 0)
        item = models.ShoppingItem.objects.filter(id=item_id).first()

        print(item_id)

        if not item:
            raise ValueError('Invalid item id')

        # Found valid item
        serializer.save(user_profile=self.request.user, shopping_item=item)
