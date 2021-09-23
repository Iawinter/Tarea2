from django.db import models

# Create your models here.


class Ligas(models.Model):
    id = models.CharField(primary_key=True, max_length=22)
    name = models.CharField(max_length=100)
    sport = models.CharField(max_length=100)
    teams = models.CharField(max_length=200)
    players = models.CharField(max_length=200)
    self = models.CharField(max_length=200)


class Equipo(models.Model):
    id = models.CharField(primary_key=True, max_length=22)
    league_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    league = models.CharField(max_length=200)
    players = models.CharField(max_length=200)
    self = models.CharField(max_length=200)
    padre = models.ForeignKey(Ligas, on_delete=models.CASCADE)


class Jugador(models.Model):
    id = models.CharField(primary_key=True, max_length=22)
    team_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    position = models.CharField(max_length=200)
    times_trained = models.IntegerField()
    league = models.CharField(max_length=200)
    team = models.CharField(max_length=200)
    self = models.CharField(max_length=200)
    padre = models.ForeignKey(Equipo, on_delete=models.CASCADE)