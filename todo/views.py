from rest_framework import generics, views, status, response
from rest_framework.permissions import IsAuthenticated

from .models import ToDo
from .serializers import ToDoSerializer


# Create your views here.
class ToDoListCreateView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ToDoSerializer

    def get_queryset(self):
        return ToDo.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        request.data["user"] = self.request.user.id
        serializer = ToDoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)


class ToDoDeleteView(generics.RetrieveDestroyAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ToDoSerializer
    lookup_field = "id"

    def get_queryset(self):
        return ToDo.objects.filter(user=self.request.user)


class ToDoMarkCompleteView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ToDoSerializer
    lookup_field = "id"

    def get_queryset(self):
        return ToDo.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):

        instance = self.get_object()
        instance.completed = True
        instance.save()
        serializer = self.get_serializer(instance)

        return response.Response(serializer.data, status=status.HTTP_202_ACCEPTED)
