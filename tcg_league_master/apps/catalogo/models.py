from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify

# Create your models here.

class FranquiciaTCG(models.Model):
    """Entidad de Contexto / Agrupación: Marca de juego de cartas (Magic, Pokémon, etc.)"""
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Juego / Marca TCG")
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    editorial = models.CharField(max_length=100, verbose_name="Editorial / Creador (Ej: Wizards of the Coast, Nintendo)")
    descripcion = models.TextField(blank=True, verbose_name="Reglamento General o Descripción")
    activo = models.BooleanField(default=True, verbose_name="¿Franquicia Activa?")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Franquicia TCG"
        verbose_name_plural = "Franquicias TCG"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    @property
    def logo_static_path(self):
        """Ruta del logo oficial usado en los torneos de esta franquicia."""
        logos = {
            'pokemon-tcg': 'images/pkmn.png',
            'one-piece-card-game': 'images/onePiece.png',
            'magic-the-gathering': 'images/magic.png',
            'dragon-ball-super-card-game': 'images/dbtcg.png',
            'yu-gi-oh-tcg': 'images/yuGiOh.png',
        }
        return logos.get(self.slug, 'images/dbtcg.png')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class TorneoTCG(models.Model):
    """Entidad Principal Gestionable: Torneo o Evento TCG"""
    ESTADOS_OPERATIVOS = [
        ('programado', 'Inscripciones Abiertas'),
        ('en_curso', 'En Curso / Rondas Activas'),
        ('finalizado', 'Finalizado'),
        ('suspendido', 'Suspendido'),
    ]

    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código del Torneo (Ej: MTG-CMD-01)")
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Evento / Torneo")
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    franquicia = models.ForeignKey(
        FranquiciaTCG, 
        on_delete=models.PROTECT, 
        related_name="torneos", 
        verbose_name="Juego TCG"
    )
    formato = models.CharField(max_length=100, verbose_name="Formato de Juego (Ej: Commander, Standard, Modern, Advanced)")
    fecha_evento = models.DateTimeField(verbose_name="Fecha y Hora de Inicio")
    lugar = models.CharField(max_length=200, default="Tienda La Ira - Chillán", verbose_name="Sede / Ubicación")
    
    precio_inscripcion = models.DecimalField(
        max_digits=10, 
        decimal_places=0, 
        validators=[MinValueValidator(0)], 
        verbose_name="Tarifa Inscripción (CLP)"
    )
    cupos_maximos = models.PositiveIntegerField(
        default=16, 
        validators=[MinValueValidator(4)], 
        verbose_name="Cupos Máximos (Aforo)"
    )
    cupos_disponibles = models.PositiveIntegerField(verbose_name="Cupos Disponibles")
    
    estado = models.CharField(max_length=20, choices=ESTADOS_OPERATIVOS, default='programado', verbose_name="Estado Operativo")
    destacado = models.BooleanField(default=False, verbose_name="¿Evento Destacado / Major?")
    activo = models.BooleanField(default=True, verbose_name="¿Publicado / Visible?")
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Torneo TCG"
        verbose_name_plural = "Torneos TCG"
        ordering = ['fecha_evento']

    def __str__(self):
        return f"[{self.codigo}] {self.nombre} ({self.franquicia.nombre})"

    @property
    def hay_cupos(self):
        return self.cupos_disponibles > 0 and self.estado == 'programado'

    @property
    def precio_formateado(self):
        return f"${self.precio_inscripcion:,.0f}".replace(",", ".")

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.codigo}-{self.nombre}")
            slug = base_slug
            contador = 1
            while TorneoTCG.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{contador}"
                contador += 1
            self.slug = slug
        super().save(*args, **kwargs)
