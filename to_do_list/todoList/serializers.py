from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .models import Task

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'username'

    def validate(self, attrs):
        username = attrs.get('username', None)

        if '@' in username:
            self.username_field = 'email'
        else:
            self.username_field = 'username'

        if self.username_field != 'username':
            user = User.objects.filter(**{self.username_field: username}).first()
            if user is not None:
                username = user.username
            else:
                raise serializers.ValidationError('User not found.')

            self.username_field = 'username'
            attrs['username'] = username

        data = super().validate(attrs)
        return data


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'due_date', 'done_at']
        read_only_fields = ['id', 'done_at']
