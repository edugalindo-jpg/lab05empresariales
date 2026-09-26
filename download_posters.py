import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()

from movies.models import Movie

for movie in Movie.objects.all():
    if movie.poster_url and not movie.poster:
        result = movie.fetch_poster_from_url()
        status = "OK" if result else "FAIL"
        print(f"{movie.title}: {status} - {movie.poster}")

print("Descarga completada")