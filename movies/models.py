from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe


class Genre(models.Model):
    name = models.CharField("Nombre", max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Género"
        verbose_name_plural = "Géneros"

    def __str__(self):
        return self.name


class Person(models.Model):
    ROLE_CHOICES = [
        ("director", "Director"),
        ("actor", "Actor"),
        ("writer", "Guionista"),
        ("producer", "Productor"),
    ]
    name = models.CharField("Nombre", max_length=200)
    role = models.CharField("Rol", max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Persona"
        verbose_name_plural = "Personas"

    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"


class Movie(models.Model):
    title = models.CharField("Título", max_length=200)
    year = models.PositiveIntegerField("Año")
    image = models.ImageField("Carátula", upload_to="movies/covers/", blank=True, null=True)
    genres = models.ManyToManyField(Genre, related_name="movies", blank=True, verbose_name="Géneros")
    people = models.ManyToManyField(Person, related_name="movies", blank=True, verbose_name="Personas")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-year", "title"]
        verbose_name = "Película"
        verbose_name_plural = "Películas"

    def __str__(self):
        return f"{self.title} ({self.year})"

    def has_image(self):
        return bool(self.image and hasattr(self.image, 'url'))

    def image_url(self):
        if self.has_image():
            try:
                return self.image.url
            except (ValueError, AttributeError):
                return None
        return None

    def image_tag_admin_list(self):
        url = self.image_url()
        if url:
            return mark_safe(
                f'<img src="{url}" width="60" height="90" '
                f'style="object-fit:cover;border-radius:4px;border:1px solid #ddd;" loading="lazy" />'
            )
        return mark_safe('<span style="color:#999;font-size:0.8rem;">Sin carátula</span>')
    image_tag_admin_list.short_description = "Carátula"

    def image_tag_admin_form(self):
        url = self.image_url()
        if url:
            return mark_safe(
                f'<img src="{url}" width="200" height="300" '
                f'style="object-fit:cover;border-radius:8px;border:1px solid #ccc;box-shadow:0 2px 8px rgba(0,0,0,0.1);" loading="lazy" />'
            )
        return mark_safe(
            '<div style="width:200px;height:300px;background:#f5f5f5;border:2px dashed #ddd;'
            'border-radius:8px;display:flex;align-items:center;justify-content:center;color:#999;font-size:0.85rem;">'
            'Sin carátula</div>'
        )
    image_tag_admin_form.short_description = "Vista previa"


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="ratings", verbose_name="Película")
    score = models.PositiveSmallIntegerField("Puntuación", help_text="1-10")
    comment = models.TextField("Comentario", blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ratings")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Valoración"
        verbose_name_plural = "Valoraciones"
        unique_together = ["movie", "user"]

    def __str__(self):
        return f"{self.movie.title} - {self.user.username}: {self.score}/10"