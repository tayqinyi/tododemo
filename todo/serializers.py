from rest_framework import serializers

from .models import ToDo


class ToDoSerializer(serializers.ModelSerializer):

    # title = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = ToDo
        fields = "__all__"
