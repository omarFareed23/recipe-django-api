"""
Serializers for user API Views
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        # tell django which model you want to base serializer on
        model = get_user_model()
        # list of fields that you want to make accessible in the API
        fields = ['email', 'password', 'name']
        # extra_kwargs is a dictionary that allows you to configure some extra settings in your model serializer
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8,
                'style': {
                    'input_type': 'password'
                }
            }
        }

    # override the create function
    # validated_data is the data that has been validated and is correct from the Meta fields
    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)
