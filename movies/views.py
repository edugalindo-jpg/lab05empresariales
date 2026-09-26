from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from .models import Movie, Rating


def home(request):
    """Página de inicio: redirige al admin o lista películas."""
    return redirect('admin:index')


def movie_recommendation(request, movie_id):
    """
    Vista pública de recomendación: películas del mismo género mejor valoradas.
    """
    movie = get_object_or_404(Movie, pk=movie_id)
    
    # Obtener los géneros de la película
    genres = movie.genres.all()
    
    if not genres.exists():
        # Si no tiene géneros, no podemos recomendar
        recommendations = Movie.objects.none()
    else:
        # Buscar películas que compartan al menos un género
        # Excluir la película actual
        # Anotar con la puntuación media y ordenar
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