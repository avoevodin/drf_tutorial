from django.db.models import Count, Q, Sum, F
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Actor
from .serializers import (
    MovieListSerializer, MovieDetailSerializer,
    ReviewCreateSerializer, CreateRatingSerializer,
    ActorListSerializer, ActorDetailSerializer
)
from .service import get_client_ip, MovieFilter


class MovieListView(ListAPIView):
    """Movie list api view"""
    serializer_class = MovieListSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = MovieFilter

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=Count(
                'ratings', filter=Q(ratings__ip=get_client_ip(self.request))
            ),
        ).annotate(
            middle_star=Sum(F('ratings__star')) / Count(F('ratings'))
        )
        return movies


class MovieDetailView(RetrieveAPIView):
    """Movie detail view"""
    serializer_class = MovieDetailSerializer
    queryset = Movie.objects.filter(draft=False)


class ReviewCreateView(CreateAPIView):
    """Review create view

    """
    serializer_class = ReviewCreateSerializer


class AddStarRatingView(CreateAPIView):
    """Adding rating for movie

    """
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsListView(ListAPIView):
    """Actors list view

    """
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(RetrieveAPIView):
    """Actors detail view

    """
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
