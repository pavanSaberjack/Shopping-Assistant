from rest_framework import serializers

from . import models

class UserProfileSerializer(serializers.ModelSerializer):
    """A serializer for our user profile objects."""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        """Create and return a new user."""

        user = models.UserProfile(
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

class ShoppingItemSerializer(serializers.ModelSerializer):
    """Serializer for feed item"""

    class Meta:
        model = models.ShoppingItem
        fields = ('id', 'item_name')


class ShoppingListItemSerializer(serializers.ModelSerializer):
    """Serializer for feed item"""

    class Meta:
        model = models.ShoppingListItem
        fields = ('id', 'user_profile', 'shopping_item')
        extra_kwargs = {'user_profile': {'read_only': True}}

class ResponseShoppingListItemSerializer(serializers.Serializer):
    """Serializer for feed item"""

    item_id = serializers.IntegerField()
    item_name = serializers.CharField()


    # class Meta:
    #     """Your data serializer, define your fields here."""
    #
    #     model = models.ShoppingListItem
    #     fields = ('shopping_item',)
