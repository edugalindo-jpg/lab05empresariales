import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()

from movies.models import Movie

for movie in Movie.objects.all().order_by('-release_year'):
    genres = ', '.join([g.name for g in movie.genres.all()])
    director = movie.director if movie.director else 'N/A'
    # Calcular promedio manualmente
    ratings = movie.ratings.all()
    if ratings.exists():
        avg = sum(r.score for r in ratings) / ratings.count()
        score_str = f"{avg:.1f}/10 ({ratings.count()} votos)"
    else:
        score_str = "Sin valorar"
    
    print(f"{movie.title} ({movie.release_year})")
    print(f"  Generos: {genres}")
    print(f"  Director: {director}")
    print(f"  Duracion: {movie.duration} min")
    print(f"  Puntuacion: {score_str}")
    print()