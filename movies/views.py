from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Q, Count
from .models import Movie, Rating, Genre, Person


def home(request):
    """Página de inicio: catálogo público con filtros."""
    movies_qs = Movie.objects.annotate(
        avg_score=Avg('ratings__score'),
        ratings_count=Count('ratings')
    ).select_related('director').prefetch_related('genres', 'actors')

    # Filtros
    query = request.GET.get('q', '').strip()
    genre_id = request.GET.get('genre')
    year = request.GET.get('year')

    if query:
        movies_qs = movies_qs.filter(
            Q(title__icontains=query) |
            Q(synopsis__icontains=query) |
            Q(director__first_name__icontains=query) |
            Q(director__last_name__icontains=query) |
            Q(actors__first_name__icontains=query) |
            Q(actors__last_name__icontains=query)
        ).distinct()

    if genre_id:
        movies_qs = movies_qs.filter(genres__id=genre_id)

    if year:
        movies_qs = movies_qs.filter(release_year=year)

    movies = movies_qs.order_by('-release_year', 'title')[:50]

    # Datos para filtros
    genres = Genre.objects.annotate(movie_count=Count('movies')).filter(movie_count__gt=0).order_by('name')
    years = Movie.objects.values_list('release_year', flat=True).distinct().order_by('-release_year')

    # Stats
    total_movies = Movie.objects.count()
    total_genres = Genre.objects.count()
    total_people = Person.objects.count()
    total_ratings = Rating.objects.count()

    return render(request, 'movies/home.html', {
        'movies': movies,
        'genres': genres,
        'years': years,
        'total_movies': total_movies,
        'total_genres': total_genres,
        'total_people': total_people,
        'total_ratings': total_ratings,
    })


def movie_recommendation(request, movie_id):
    """Vista pública de recomendación: películas del mismo género mejor valoradas."""
    movie = get_object_or_404(
        Movie.objects.annotate(avg_score=Avg('ratings__score')).select_related('director').prefetch_related('genres'),
        pk=movie_id
    )

    genres = movie.genres.all()

    if not genres.exists():
        recommendations = Movie.objects.none()
    else:
        recommendations = Movie.objects.filter(
            genres__in=genres
        ).exclude(
            pk=movie_id
        ).annotate(
            avg_score=Avg('ratings__score')
        ).filter(
            avg_score__isnull=False
        ).distinct().order_by('-avg_score')[:10]

    return render(request, 'movies/recommendation.html', {
        'movie': movie,
        'recommendations': recommendations,
    })