from django.db.models import Count, Q, Sum, F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from .models import Movie, Actor
from .serializers import (
    MovieListSerializer, MovieDetailSerializer,
    ReviewCreateSerializer, CreateRatingSerializer,
    ActorListSerializer, ActorDetailSerializer
)
from .service import get_client_ip, MovieFilter, PaginationMovie


class MovieViewSet(ReadOnlyModelViewSet):
    """Movie list api view"""
    filter_backends = (DjangoFilterBackend,)
    filter_class = MovieFilter
    pagination_class = PaginationMovie

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=Count(
                'ratings', filter=Q(ratings__ip=get_client_ip(self.request))
            ),
        ).annotate(
            middle_star=Sum(F('ratings__star')) / Count(F('ratings'))
        )
        return movies

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        elif self.action == 'retrieve':
            return MovieDetailSerializer


class ReviewCreateView(ModelViewSet):
    """Review create view

    """
    serializer_class = ReviewCreateSerializer


class AddStarRatingView(ModelViewSet):
    """Adding rating for movie

    """
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsViewSet(ReadOnlyModelViewSet):
    """Actors list view

    """
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorListSerializer
        elif self.action == 'retrieve':
            return ActorDetailSerializer
