from django.db.models import Count, Q, Sum, F
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie
from .serializers import MovieListSerializer, MovieDetailSerializer, \
    ReviewCreateSerializer, CreateRatingSerializer
from .service import get_client_ip


class MovieListView(APIView):
    """Movie list api view"""

    def get(self, request):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=Count(
                'ratings', filter=Q(ratings__ip=get_client_ip(request))
            ),
        ).annotate(
            middle_star=Sum(F('ratings__star')) / Count(F('ratings'))
        )
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetailView(APIView):
    """Movie detail view"""

    def get(self, request, pk):
        movie = Movie.objects.get(id=pk, draft=False)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)


class ReviewCreateView(APIView):
    """Review create view

    """

    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)


class AddStarRatingView(APIView):
    """Adding rating for movie

    """

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)
