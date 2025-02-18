# Generated by Django 5.1.5 on 2025-02-18 10:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Movie', '0001_initial'),
        ('Theatre', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='C_ShowType',
            fields=[
                ('showTypeId', models.IntegerField(choices=[(1, 'Morning Show'), (2, 'Matinee Show'), (3, 'First Show'), (4, 'Second Show')], default=1, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='ShowDirectory',
            fields=[
                ('showId', models.AutoField(primary_key=True, serialize=False)),
                ('startTime', models.TimeField()),
                ('endTime', models.TimeField()),
                ('dateTime', models.DateTimeField()),
                ('houseFullFlag', models.BooleanField(default=False)),
                ('movieId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Movie.moviedirectory')),
                ('screenId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Theatre.screendirectory')),
                ('showTypeId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Booking.c_showtype')),
                ('theatreId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Theatre.theatredirectory')),
            ],
        ),
        migrations.CreateModel(
            name='BookingDirectory',
            fields=[
                ('bookingId', models.AutoField(primary_key=True, serialize=False)),
                ('seatID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Theatre.seatmaster')),
                ('showId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Booking.showdirectory')),
            ],
        ),
        migrations.AddConstraint(
            model_name='showdirectory',
            constraint=models.UniqueConstraint(fields=('screenId', 'dateTime', 'showTypeId'), name='unique_show_per_screen_per_date'),
        ),
    ]
