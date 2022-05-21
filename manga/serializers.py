from rest_framework import serializers
from .models import *


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class NovellaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Novella
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['genre'] = GenreSerializer(instance.genre.all(), many=True).data
        representation['likes'] = instance.likes.all().count()
        representation['images'] = NovellaImageSerializer(instance.images.all(),
                                                       many=True,
                                                     context=self.context).data
        return representation


class NovellaImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NovellaImage
        fields = '__all__'

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation


# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         exclude = ('novella', )
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['user'] = instance.user.username
#         return representation