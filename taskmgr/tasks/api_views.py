from rest_framework import viewsets, permissions
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Task
from .serializers import TaskSerializer

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)
    def _broadcast(self, action, instance):
        layer = get_channel_layer()
        if not layer: return
        async_to_sync(layer.group_send)(f'tasks_{instance.owner_id}', {
            'type':'task.event','action':action,
            'task': TaskSerializer(instance).data,
        })
    def perform_create(self, s):
        obj = s.save(owner=self.request.user); self._broadcast('created', obj)
    def perform_update(self, s):
        obj = s.save(); self._broadcast('updated', obj)
    def perform_destroy(self, instance):
        oid = instance.id; owner = instance.owner_id
        instance.delete()
        layer = get_channel_layer()
        if layer:
            async_to_sync(layer.group_send)(f'tasks_{owner}', {
                'type':'task.event','action':'deleted','task':{'id':oid}})
