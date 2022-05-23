from django.contrib.auth.decorators import login_required
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .serializers import *


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer



class MyPaginationView(PageNumberPagination):
    page_size = 2
    def get_paginated_response(self, data):
        return super().get_paginated_response(data)

class NovellaViewSet(viewsets.ModelViewSet):
    queryset = Novella.objects.all()
    serializer_class = NovellaSerializer
    permission_classes = [IsAdminUser, ]
    pagination_class = MyPaginationView

    def get_permissions(self):
        """pereopredelim dannyi method"""
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            permissions = [IsAdminUser, ]
        # elif self.action == 'create':
        #     permissions = [IsAdminUser, ]
        else:
            permissions = [AllowAny, ]
        return [permission() for permission in permissions]

    # @action(detail=False, methods=['get'])
    # def own(self, request, pk=None):
    #     queryset = self.get_queryset()
    #     serializer = NovellaSerializer(queryset, many=True, context={'request': request})
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    @action(detail=False, methods=['GET'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) |
                                   Q(description__icontains=q) |
                                   Q(price__icontains=q))
        serializer = NovellaSerializer(queryset, many=True,
                                    context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def filtration(self, request):
        queryset = self.queryset

        title = request.query_params.get('title')
        genre = request.query_params.get('genre')
        price = request.query_params.get('price')

        if title == 'A-Z':
            queryset = self.get_queryset().order_by('title')
        elif title == 'Z-A':
            queryset = self.get_queryset().order_by('-title')
        elif genre:
            queryset = queryset.filter(genre=genre)
        elif price == 'asc':
            queryset = self.get_queryset().order_by('price')
        elif price == 'desc':
            queryset = self.get_queryset().order_by('-price')
        else:
            queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class NovellaImageViewSet(viewsets.ModelViewSet):
    queryset = NovellaImage.objects.all()
    serializer_class = NovellaImageSerializer

    def get_serializer_context(self):
        return {'request': self.request}


@api_view(['GET'])
@login_required
def toggle_like(request, id):
    novella = Novella.objects.get(id=id)
    if Like.objects.filter(user=request.user, novella=novella):
        Like.objects.get(user=request.user, novella=novella).delete()
    else:
        Like.objects.create(user=request.user, novella=novella)
    serializer = NovellaSerializer(novella)
    return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)