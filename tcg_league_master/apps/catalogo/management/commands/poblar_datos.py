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
            self.stdout.write(self.style.SUCCESS("OK: Superusuario 'admin' creado (Clave: admin)."))

        if not User.objects.filter(username="jugador1").exists():
            User.objects.create_user("jugador1", "jugador1@tcgleague.cl", "jugador123", first_name="Pedro", last_name="Soto")
            self.stdout.write(self.style.SUCCESS("OK: Usuario estándar 'jugador1' creado."))

        # 2. Crear Franquicias de Contexto
        franquicias_data = [
            ("Pokémon TCG", "The Pokémon Company", "Torneos oficiales de cartas Pokémon."),
            ("One Piece Card Game", "Bandai", "Torneos oficiales del juego de cartas de One Piece."),
            ("Magic: The Gathering", "Wizards of the Coast", "Juego de estrategia coleccionable pionero."),
            ("Dragon Ball Super Card Game", "Bandai", "Batallas de ritmo rápido con guerreros Z."),
            ("Yu-Gi-Oh! TCG", "Konami", "Duelos de monstruos, magia y trampas."),
        ]

        franq_map = {}
        for nombre, ed, desc in franquicias_data:
            f, _ = FranquiciaTCG.objects.get_or_create(nombre=nombre, defaults={'editorial': ed, 'descripcion': desc})
            franq_map[nombre] = f

        # 3. Crear Torneos Principales en Chillán (La Ira, Suna Senso, Rey Mago)
        ahora = timezone.now()
        torneos_data = [
            ("PKM-CHI-01", "League Cup Pokémon Standard", franq_map["Pokémon TCG"], "Standard", ahora + timedelta(days=2), "La Ira (Chillán)", 6000, 32, 28, True),
            ("OPC-CHI-01", "Store Tournament One Piece", franq_map["One Piece Card Game"], "Standard", ahora + timedelta(days=3), "Suna Senso (Chillán)", 5000, 24, 20, True),
            ("MTG-CHI-01", "Torneo Commander FNM", franq_map["Magic: The Gathering"], "Commander / EDH", ahora + timedelta(days=5), "Rey Mago (Chillán)", 5000, 32, 26, True),
            ("PKM-CHI-02", "Liga Pokémon Gym Battle", franq_map["Pokémon TCG"], "Expanded", ahora + timedelta(days=6), "Suna Senso (Chillán)", 4000, 20, 16, False),
            ("YGO-CHI-01", "Locals Yu-Gi-Oh! Chillán", franq_map["Yu-Gi-Oh! TCG"], "Advanced Format", ahora + timedelta(days=8), "La Ira (Chillán)", 4500, 24, 18, False),
            ("OPC-CHI-02", "Flagship Qualifier One Piece", franq_map["One Piece Card Game"], "Standard", ahora + timedelta(days=10), "Rey Mago (Chillán)", 7000, 32, 30, False),
        ]

        for cod, nom, franq, form, fecha, lug, prec, max_c, disp_c, dest in torneos_data:
            TorneoTCG.objects.update_or_create(codigo=cod, defaults={
                'nombre': nom, 'franquicia': franq, 'formato': form, 
                'fecha_evento': fecha, 'lugar': lug, 'precio_inscripcion': prec, 
                'cupos_maximos': max_c, 'cupos_disponibles': disp_c, 
                'destacado': dest, 'estado': 'programado', 'activo': True
            })

        self.stdout.write(self.style.SUCCESS("OK: Datos iniciales de TCG League Master cargados correctamente."))
