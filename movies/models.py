from django.db import models
from django.conf import settings


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Movie(models.Model):
    title = models.CharField(max_length=200)
    synopsis = models.TextField(blank=True)
    release_year = models.PositiveIntegerField()
    duration = models.PositiveIntegerField(help_text="Duración en minutos")
    genres = models.ManyToManyField(Genre, related_name='movies', blank=True)
    director = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True, related_name='directed_movies')
    actors = models.ManyToManyField(Person, related_name='acted_movies', blank=True)
    poster = models.ImageField(upload_to='movies/posters/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-release_year', 'title']

    def __str__(self):
        return f"{self.title} ({self.release_year})"


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings')
    score = models.PositiveSmallIntegerField(help_text="Puntuación del 1 al 10")
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['movie', 'user']

    def __str__(self):
        return f"{self.movie.title} - {self.user.username}: {self.score}/10"