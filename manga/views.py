from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import *


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer



# class MyPaginationView(PageNumberPagination):
#     page_size = 2
#     def get_paginated_response(self, data):
#         for i in range(self.page_size):
#             text = data[i]['text']
#             data[i]['text'] = text[:15] + ' ...'
#         return super().get_paginated_response(data)

class NovellaViewSet(viewsets.ModelViewSet):
    queryset = Novella.objects.all()
    serializer_class = NovellaSerializer
    # permission_classes = [IsAuthenticated, ]
    # pagination_class = MyPaginationView


    # def get_permissions(self):
    #     if self.action in ['update', 'partial_update', 'destroy']:
    #         permissions = [IsAuthenticated, ]
    #     return [permission() for permission in permissions]



    # @action(detail=False, methods=['get'])
    # def own(self, request, pk=None):
    #     queryset = self.get_queryset()
    #     serializer = NovellaSerializer(queryset, many=True, context={'request': request})
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    # @action(detail=False, methods=['get'])
    # def search(self, request, pk=None):
    #     q = request.query_params.get('q')
    #     queryset = self.get_queryset()
    #     queryset = queryset.filter(Q(title__icontains=q) |
    #                                Q(description__icontains=q) |
    #                                Q(price__icontains=q))
    #     serializer = NovellaSerializer(queryset, many=True,
    #                                 context={'request': request})
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # @action(methods=['get'], detail=False)
    # def filtration(self, request):





class NovellaImageViewSet(viewsets.ModelViewSet):
    queryset = NovellaImage.objects.all()
    serializer_class = NovellaImageSerializer

    def get_serializer_context(self):
        return {'request': self.request}