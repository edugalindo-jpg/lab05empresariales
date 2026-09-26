import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont
from movies.models import Movie
from io import BytesIO

# Colores para cada película (tema cinematográfico)
movie_colors = {
    'Inception': ('#1a1a2e', '#e94560'),
    'The Dark Knight': ('#000000', '#ffd700'),
    'Interstellar': ('#0c0c0c', '#ffd700'),
    'Pulp Fiction': ('#8b0000', '#ffffff'),
    'Django Unchained': ('#2f4f4f', '#ffd700'),
    'Forrest Gump': ('#228b22', '#ffffff'),
    'Saving Private Ryan': ('#8b4513', '#ffffff'),
    'Goodfellas': ('#1a1a1a', '#ff6347'),
    'The Departed': ('#2c2c2c', '#ffffff'),
    'The Matrix': ('#006400', '#00ff00'),
}

def create_placeholder_image(title, bg_color, accent_color):
    """Crear imagen placeholder con PIL."""
    width, height = 300, 450
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Gradiente sutil
    for y in range(height):
        alpha = y / height
        r = int(int(bg_color[1:3], 16) * (1 - alpha * 0.3))
        g = int(int(bg_color[3:5], 16) * (1 - alpha * 0.3))
        b = int(int(bg_color[5:7], 16) * (1 - alpha * 0.3))
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Texto del título
    try:
        font = ImageFont.truetype("arial.ttf", 24)
        font_small = ImageFont.truetype("arial.ttf", 14)
    except:
        font = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Dibujar título (envuelto)
    words = title.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] > width - 40:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
        else:
            current_line.append(word)
    if current_line:
        lines.append(' '.join(current_line))
    
    total_height = len(lines) * 35
    start_y = (height - total_height) // 2
    
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = start_y + i * 35
        # Sombra
        draw.text((x+2, y+2), line, font=font, fill='#000000')
        # Texto principal
        draw.text((x, y), line, font=font, fill=accent_color)
    
    # Icono de cámara
    icon_y = start_y + total_height + 30
    draw.ellipse([width//2 - 30, icon_y - 30, width//2 + 30, icon_y + 30], outline=accent_color, width=2)
    draw.ellipse([width//2 - 15, icon_y - 15, width//2 + 15, icon_y + 15], outline=accent_color, width=2)
    draw.ellipse([width//2 - 8, icon_y - 8, width//2 + 8, icon_y + 8], fill=accent_color)
    draw.polygon([(width//2 - 10, icon_y + 5), (width//2, icon_y - 5), (width//2 + 10, icon_y + 5)], fill=accent_color)
    
    # Texto "POSTER"
    bbox = draw.textbbox((0, 0), "POSTER", font=font_small)
    text_w = bbox[2] - bbox[0]
    draw.text((width//2 - text_w//2, icon_y + 40), "POSTER", font=font_small, fill=accent_color)
    
    return img

for movie in Movie.objects.all():
    if not movie.poster:
        colors = movie_colors.get(movie.title, ('#1a1a2e', '#e94560'))
        img = create_placeholder_image(movie.title, colors[0], colors[1])
        
        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=85)
        buffer.seek(0)
        
        filename = f"{movie.title.lower().replace(' ', '_')}_poster.jpg"
        movie.poster.save(filename, ContentFile(buffer.read()), save=True)
        print(f"[OK] Creado póster local para: {movie.title}")
    else:
        print(f"[SKIP] {movie.title} ya tiene póster")

print("\n[DONE] Todos los pósters generados localmente")