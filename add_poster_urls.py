import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from movies.models import Movie

# Usar placeholders de imágenes reales que funcionan
poster_urls = {
    'Inception': 'https://via.placeholder.com/300x450/1a1a2e/ffffff?text=Inception',
    'The Dark Knight': 'https://via.placeholder.com/300x450/000000/ffff00?text=The+Dark+Knight',
    'Interstellar': 'https://via.placeholder.com/300x450/0c0c0c/ffd700?text=Interstellar',
    'Pulp Fiction': 'https://via.placeholder.com/300x450/8b0000/ffffff?text=Pulp+Fiction',
    'Django Unchained': 'https://via.placeholder.com/300x450/2f4f4f/ffd700?text=Django',
    'Forrest Gump': 'https://via.placeholder.com/300x450/228b22/ffffff?text=Forrest+Gump',
    'Saving Private Ryan': 'https://via.placeholder.com/300x450/8b4513/ffffff?text=Saving+Private+Ryan',
    'Goodfellas': 'https://via.placeholder.com/300x450/1a1a1a/ff6347?text=Goodfellas',
    'The Departed': 'https://via.placeholder.com/300x450/2c2c2c/ffffff?text=The+Departed',
    'The Matrix': 'https://via.placeholder.com/300x450/006400/00ff00?text=The+Matrix',
}

for movie in Movie.objects.all():
    url = poster_urls.get(movie.title)
    if url:
        movie.poster_url = url
        movie.save()
        print(f"URL asignada a: {movie.title}")

print("URLs actualizadas. Ahora prueba la acción 'Descargar póster desde URL' en el admin.")