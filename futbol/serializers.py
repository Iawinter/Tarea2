from rest_framework import serializers
from . models import Ligas, Equipo, Jugador

class LigasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ligas
        fields = '__all__'

class EquiposSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = ('id', 'league_id', 'name', 'city', 'league', 'players', 'self')

class JugadoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jugador
        fields = ('id', 'team_id', 'name', 'age', 'position', 'times_trained', 'league', 'team', 'self')