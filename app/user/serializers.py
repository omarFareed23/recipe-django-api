"""
Serializers for user API Views
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers, authentication
from django.utils.translation import gettext as _


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

    def update(self, instance, validated_data):
        """Update current user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password is not None:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={
            'input_type': 'password'
        },
        # avoid trimming white spaces
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authentication.authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')
        attrs['user'] = user
        return attrs
