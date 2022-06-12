# Generated by Django 3.2.5 on 2022-06-12 21:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mainapp', '0003_product'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now=True, verbose_name='Создан')),
                ('updated', models.DateTimeField(auto_now_add=True, verbose_name='Обновлён')),
                ('paid', models.DateTimeField(verbose_name='Оплачен')),
                ('status', models.CharField(choices=[('FM', 'Формирутеся'), ('STP', 'Обрабатывается'), ('PD', 'Оплачен'), ('PRD', 'Обрабатывается'), ('RDY', 'Готов к выдаче'), ('CNC', 'Отменён')], default='FM', max_length=3, verbose_name='Статус')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='Количество')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderitems', to='ordersapp.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.product', verbose_name='Товары')),
            ],
        ),
    ]
