from rest_framework import serializers
from .models import Movie, Review


class MovieListSerializer(serializers.ModelSerializer):
    """Films list

    """

    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'category')


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Review create serializer

    """

    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Review serializer

    """

    class Meta:
        model = Review
        fields = ('name', 'text', 'parent')


class MovieDetailSerializer(serializers.ModelSerializer):
    """Films detail

    """
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    directors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('draft',)
