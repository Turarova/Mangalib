from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import *
from .serializers import *



class MyPaginationView(PageNumberPagination):
    page_size = 2
    def get_paginated_response(self, data):
        for i in range(self.page_size):
            text = data[i]['text']
            data[i]['text'] = text[:15] + ' ...'
        return super().get_paginated_response(data)

class NovellaViewSet(viewsets.ModelViewSet):
    queryset = Novella.objects.all()
    serializer_class = NovellaSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = MyPaginationView

    # def get_permissions(self):
    #     if permissions = [IsAuthenticated, ]
    #     return [permission() for permission in permissions]



    # @action(detail=False, methods=['get'])
    # def own(self, request, pk=None):
    #     queryset = self.get_queryset()
    #     queryset = queryset.filter(author=request.user)
    #     serializer = PostSerializer(queryset, many=True, context={'request': request})
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    #
    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context['action'] = self.action
    #     return context
    #
    # @action(detail=False, methods=['get'])
    # def search(self, request, pk=None):
    #     q = request.query_params.get('q')
    #     queryset = self.get_queryset()
    #     queryset  = queryset.filter(Q(title__icontains=q) |
    #                                 Q(text__icontains=q))
    #     serializer = PostSerializer(queryset, many=True,
    #                                 context={'request':request})
    #     return Response(serializer.data, status=status.HTTP_200_OK)