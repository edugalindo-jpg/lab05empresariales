from django.contrib import admin
from .models import Movie, Genre, Person, Rating


class RatingInline(admin.TabularInline):
    model = Rating
    extra = 1
    readonly_fields = ("created_at", "updated_at")
    fields = ("user", "score", "comment", "created_at", "updated_at")
    verbose_name = "Valoración"
    verbose_name_plural = "Valoraciones"


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "created_at", "updated_at")
    list_filter = ("role",)
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("image_tag_admin_list", "title", "year", "get_genres", "created_at")
    list_display_links = ("title",)
    list_filter = ("genres", "year")
    search_fields = ("title", "people__name")
    filter_horizontal = ("genres", "people")
    readonly_fields = ("created_at", "updated_at", "image_tag_admin_form")
    inlines = [RatingInline]

    fieldsets = (
        ("Información básica", {"fields": ("title", "year")}),
        ("Carátula", {
            "fields": ("image", "image_tag_admin_form"),
            "description": "Sube una imagen (JPG/PNG/WebP). Se muestra vista previa abajo."
        }),
        ("Relaciones", {"fields": ("genres", "people")}),
        ("Auditoría", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def get_genres(self, obj):
        return ", ".join([g.name for g in obj.genres.all()])
    get_genres.short_description = "Géneros"

    def image_tag_admin_list(self, obj):
        return obj.image_tag_admin_list()
    image_tag_admin_list.short_description = "Carátula"

    def image_tag_admin_form(self, obj):
        return obj.image_tag_admin_form()
    image_tag_admin_form.short_description = "Vista previa"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("movie", "user", "score", "created_at")
    list_filter = ("score", "created_at")
    search_fields = ("movie__title", "user__username", "comment")
    readonly_fields = ("created_at", "updated_at")