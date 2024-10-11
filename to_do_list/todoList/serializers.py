from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Task


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'username'

    def validate(self, attrs):
        username = attrs.get('username', None)

        if '@' in username:
            self.username_field = 'email'
        else:
            self.username_field = 'username'

        if self.username_field != 'username':
            username = models.User.objects.filter(
                **{self.username_field: username}
            ).values_list('username', flat=True).first()
            self.username_field = 'username'
            attrs['username'] = username

        data = super().validate(attrs)
        return data


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'due_date', 'done_at']
        read_only_fields = ['id', 'done_at']

