from django.contrib import admin
from django.contrib import messages
from .models import Genre, Person, Movie, Rating


class RatingInline(admin.TabularInline):
    model = Rating
    extra = 1
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'birth_date', 'created_at', 'updated_at')
    search_fields = ('first_name', 'last_name')
    list_filter = ('birth_date',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'duration', 'director', 'has_poster', 'created_at')
    list_filter = ('genres', 'release_year')
    search_fields = ('title', 'synopsis', 'director__first_name', 'director__last_name')
    filter_horizontal = ('genres', 'actors')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [RatingInline]
    actions = ['fetch_posters']

    fieldsets = (
        ('Información básica', {
            'fields': ('title', 'synopsis', 'release_year', 'duration')
        }),
        ('Relaciones', {
            'fields': ('genres', 'director', 'actors')
        }),
        ('Imagen', {
            'fields': ('poster_url', 'poster'),
            'description': 'Introduce una URL en "poster_url" y usa la acción "Descargar póster desde URL" para guardarla.'
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def has_poster(self, obj):
        return bool(obj.poster)
    has_poster.boolean = True
    has_poster.short_description = 'Póster'

    @admin.action(description='Descargar póster desde URL')
    def fetch_posters(self, request, queryset):
        count = 0
        for movie in queryset:
            if movie.fetch_poster_from_url():
                count += 1
        self.message_user(request, f'Se descargaron {count} pósters correctamente.', messages.SUCCESS)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'score', 'created_at')
    list_filter = ('score', 'created_at')
    search_fields = ('movie__title', 'user__username', 'comment')
    readonly_fields = ('created_at', 'updated_at')