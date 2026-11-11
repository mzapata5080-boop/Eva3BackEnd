from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('catalogo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='torneotcg',
            name='afiche',
        ),
    ]
