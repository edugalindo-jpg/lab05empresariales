from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Count, Q
from .models import Movie, Genre


def movie_list(request):
    """Catálogo público con filtros y tarjetas responsivas."""
    movies = Movie.objects.annotate(
        avg_score=Avg("ratings__score"),
        ratings_count=Count("ratings")
    ).prefetch_related("genres", "people")

    # Filtros GET
    query = request.GET.get("q", "").strip()
    genre_id = request.GET.get("genre")
    year = request.GET.get("year")

    if query:
        movies = movies.filter(
            Q(title__icontains=query) |
            Q(genres__name__icontains=query) |
            Q(people__name__icontains=query)
        ).distinct()

    if genre_id:
        movies = movies.filter(genres__id=genre_id)

    if year:
        movies = movies.filter(year=year)

    movies = movies.order_by("-year", "title")[:50]

    # Datos para filtros
    genres = Genre.objects.all()
    years = Movie.objects.values_list("year", flat=True).distinct().order_by("-year")

    return render(request, "movies/movie_list.html", {
        "movies": movies,
        "genres": Genre.objects.all(),
        "years": years,
        "current_genre": int(genre_id) if genre_id else None,
        "current_year": int(year) if year else None,
        "query": query,
    })


def movie_recommendation(request, movie_id):
    """Recomendaciones: mismo género, mejor puntuación media."""
    movie = get_object_or_404(
        Movie.objects.prefetch_related("genres", "people"),
        pk=movie_id
    )
    genres = movie.genres.all()

    if not genres.exists():
        recommendations = Movie.objects.none()
    else:
        recommendations = (
            Movie.objects.filter(genres__in=genres)
            .exclude(pk=movie_id)
            .annotate(avg_score=Avg("ratings__score"))
            .filter(avg_score__isnull=False)
            .distinct()
            .order_by("-avg_score")[:12]
        )

    return render(request, "movies/recommendation.html", {
        "movie": movie,
        "recommendations": recommendations,
    })