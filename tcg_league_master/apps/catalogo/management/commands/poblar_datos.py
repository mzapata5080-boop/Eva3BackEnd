from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from apps.catalogo.models import FranquiciaTCG, TorneoTCG


class Command(BaseCommand):
    help = "Pobla la base de datos con franquicias TCG, torneos iniciales y usuarios de prueba."

    def handle(self, *args, **kwargs):
        # 1. Crear usuarios de prueba (Admin y Estándar)
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@tcgleague.cl", "admin")
            self.stdout.write(self.style.SUCCESS("✓ Superusuario 'admin' creado (Clave: admin)."))

        if not User.objects.filter(username="jugador1").exists():
            User.objects.create_user("jugador1", "jugador1@tcgleague.cl", "jugador123", first_name="Pedro", last_name="Soto")
            self.stdout.write(self.style.SUCCESS("✓ Usuario estándar 'jugador1' creado."))

        # 2. Crear Franquicias de Contexto
        franquicias_data = [
            ("Magic: The Gathering", "Wizards of the Coast", "Juego de estrategia coleccionable pionero."),
            ("Pokémon TCG", "The Pokémon Company", "Torneos oficiales de cartas Pokémon."),
            ("Dragon Ball Super Card Game", "Bandai", "Batallas de ritmo rápido con guerreros Z."),
            ("Yu-Gi-Oh! TCG", "Konami", "Duelos de monstruos, magia y trampas."),
        ]

        franq_map = {}
        for nombre, ed, desc in franquicias_data:
            f, _ = FranquiciaTCG.objects.get_or_create(nombre=nombre, defaults={'editorial': ed, 'descripcion': desc})
            franq_map[nombre] = f

        # 3. Crear Torneos Principales
        ahora = timezone.now()
        torneos_data = [
            ("MTG-CMD-01", "Torneo Commander FNM", franq_map["Magic: The Gathering"], "Commander / EDH", ahora + timedelta(days=2), 5000, 32, 28, True),
            ("PKM-STD-01", "League Cup Pokémon Standard", franq_map["Pokémon TCG"], "Standard", ahora + timedelta(days=5), 8000, 24, 12, True),
            ("DBS-ADV-01", "Dragon Ball Championship Qualifier", franq_map["Dragon Ball Super Card Game"], "Constructed Advanced", ahora + timedelta(days=7), 10000, 16, 16, False),
            ("YGO-ADV-02", "Locals Yu-Gi-Oh! Dual Sunday", franq_map["Yu-Gi-Oh! TCG"], "Advanced Format", ahora + timedelta(days=9), 4000, 20, 15, False),
        ]

        for cod, nom, franq, form, fecha, prec, max_c, disp_c, dest in torneos_data:
            TorneoTCG.objects.get_or_create(codigo=cod, defaults={
                'nombre': nom, 'franquicia': franq, 'formato': form, 
                'fecha_evento': fecha, 'precio_inscripcion': prec, 
                'cupos_maximos': max_c, 'cupos_disponibles': disp_c, 
                'destacado': dest, 'estado': 'programado', 'activo': True
            })

        self.stdout.write(self.style.SUCCESS("✓ Datos iniciales de TCG League Master cargados correctamente."))