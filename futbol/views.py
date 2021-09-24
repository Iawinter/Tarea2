from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import Ligas, Equipo, Jugador
from . serializers import LigasSerializer, EquiposSerializer, JugadoresSerializer
from base64 import b64encode
# Create your views here.


class LigasList(APIView):
    def get(self, request):
        ligas = Ligas.objects.all()
        serializer = LigasSerializer(ligas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        info = request.data
        if "name" not in info.keys() or "sport" not in info.keys():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if type(info['name']) != str or type(info['sport']) != str:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        id = b64encode(info['name'].encode()).decode('utf-8')
        if len(id) > 22:
            id = id[0:22]
        liga = Ligas.objects.all().filter(id=id)
        if liga:
            serializer = LigasSerializer(liga, many=True)
            return Response(serializer.data[0], status=status.HTTP_409_CONFLICT)
        teams = "https://iawinter-tarea2.herokuapp.com/leagues/"+id+"/teams"
        players = "https://iawinter-tarea2.herokuapp.com/leagues/"+id+"/players"
        yo = "https://iawinter-tarea2.herokuapp.com/leagues/"+id
        sport = info['sport']
        nueva_liga = Ligas.objects.create(id=id, name=info['name'], sport=sport, teams=teams, players=players)
        nueva_liga.self = yo
        nueva_liga.save()
        serializer = LigasSerializer(nueva_liga)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EquiposList(APIView):
    def get(self, request):
        equipos = Equipo.objects.all()
        serializer = EquiposSerializer(equipos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class JugadoresList(APIView):
    def get(self, request):
        jugadores = Jugador.objects.all()
        serializer = JugadoresSerializer(jugadores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LigasUnico(APIView):
    def get(self, request, id):
        liga = Ligas.objects.all().filter(id=id)
        if liga:
            serializer = LigasSerializer(liga, many=True)
            return Response(serializer.data[0], status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        liga = Ligas.objects.all().filter(id=id)
        if liga:
            Ligas.objects.get(id=id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class EquiposUnico(APIView):
    def get(self, request, id):
        equipo = Equipo.objects.all().filter(id=id)
        if equipo:
            serializer = EquiposSerializer(equipo, many=True)
            return Response(serializer.data[0], status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        equipo = Equipo.objects.all().filter(id=id)
        if equipo:
            Equipo.objects.get(id=id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class JugadoresUnico(APIView):
    def get(self, request, id):
        jugador = Jugador.objects.all().filter(id=id)
        if jugador:
            serializer = JugadoresSerializer(jugador, many=True)
            return Response(serializer.data[0], status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        jugador = Jugador.objects.all().filter(id=id)
        if jugador:
            Jugador.objects.get(id=id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class EquiposLiga(APIView):
    def get(self, request, id):
        liga = Ligas.objects.all().filter(id=id)
        if not liga:
            return Response(status=status.HTTP_404_NOT_FOUND)
        equipos = Equipo.objects.all().filter(league_id=id)
        serializer = EquiposSerializer(equipos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id):
        info = request.data
        if "name" not in info.keys() or "city" not in info.keys():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if type(info['name']) != str or type(info['city']) != str:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        liga = Ligas.objects.all().filter(id=id)
        if not liga:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        id1 = info['name']+":"+id
        id1 = b64encode(id1.encode()).decode('utf-8')
        if len(id1) > 22:
            id1 = id1[0:22]
        equipo = Equipo.objects.all().filter(id=id1)
        if equipo:
            serializer = EquiposSerializer(equipo, many=True)
            return Response(serializer.data[0], status=status.HTTP_409_CONFLICT)
        liga = Ligas.objects.get(id=id)
        league = "https://iawinter-tarea2.herokuapp.com/league/"+id
        players = "https://iawinter-tarea2.herokuapp.com/teams/"+id1+"/players"
        yo = "https://iawinter-tarea2.herokuapp.com/teams/"+id1
        nuevo_equipo = Equipo.objects.create(id=id1, league_id=id, name=info['name'], city=info['city'], league=league, players=players, padre=liga)
        nuevo_equipo.self = yo
        nuevo_equipo.save()
        serializer = EquiposSerializer(nuevo_equipo)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JugadoresLiga(APIView):
    def get(self, request, id):
        liga = Ligas.objects.all().filter(id=id)
        if not liga:
            return Response(status=status.HTTP_404_NOT_FOUND)
        equipo = Equipo.objects.all().filter(league_id=id)
        serializer = EquiposSerializer(equipo, many=True)
        lista = []
        for equipo in serializer.data:
            jugadores = Jugador.objects.all().filter(team_id=equipo['id'])
            serializer1 = JugadoresSerializer(jugadores, many=True)
            for jugador in serializer1.data:
                lista.append(jugador)
        return Response(lista, status=status.HTTP_200_OK)


class JugadoresEquipo(APIView):
    def get(self, request, id):
        equipo = Equipo.objects.all().filter(id=id)
        if not equipo:
            return Response(status=status.HTTP_404_NOT_FOUND)
        jugadores = Jugador.objects.all().filter(team_id=id)
        serializer = JugadoresSerializer(jugadores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id):
        equipo = Equipo.objects.all().filter(id=id)
        if not equipo:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        info = request.data
        if "name" not in info.keys() or "age" not in info.keys() or "position" not in info.keys():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if type(info['name']) != str or type(info['age']) != int or type(info['position']) != str:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        id1 = info['name']+":"+id
        id1 = b64encode(id1.encode()).decode('utf-8')
        if len(id1) > 22:
            id1 = id1[0:22]
        jugador = Jugador.objects.all().filter(id=id1)
        if jugador:
            serializer = JugadoresSerializer(jugador, many=True)
            return Response(serializer.data[0], status=status.HTTP_409_CONFLICT)
        equipo = Equipo.objects.get(id=id)
        id_liga = Equipo.objects.get(id=id)
        id_liga = id_liga.league_id
        liga= "https://iawinter-tarea2.herokuapp.com/league/"+id_liga
        team= "https://iawinter-tarea2.herokuapp.com/teams/"+id
        yo = "https://iawinter-tarea2.herokuapp.com/players/"+id1
        nuevo_jugador = Jugador.objects.create(id=id1, team_id=id, name=info['name'], position=info['position'], times_trained=0, league=liga , team=team, padre=equipo)
        nuevo_jugador.self = yo
        nuevo_jugador.save()
        serializer = JugadoresSerializer(nuevo_jugador)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JugadorTrain(APIView):
    def put(self, request, id):
        jugador = Jugador.objects.all().filter(id=id)
        if not jugador:
            return Response(status=status.HTTP_404_NOT_FOUND)
        jugador = Jugador.objects.get(id=id)
        jugador.times_trained += 1
        jugador.save()
        return Response(status=status.HTTP_200_OK)


class EquipoTrain(APIView):
    def put(self, request, id):
        equipo = Equipo.objects.all().filter(id=id)
        if not equipo:
            return Response(status=status.HTTP_404_NOT_FOUND)
        jugadores = Jugador.objects.all().filter(team_id=id)
        for jugador in jugadores:
            jugador.times_trained += 1
            jugador.save()
        return Response(status=status.HTTP_200_OK)


class LigaTrain(APIView):
    def put(self, request, id):
        liga = Ligas.objects.all().filter(id=id)
        if not liga:
            return Response(status=status.HTTP_404_NOT_FOUND)
        equipos = Equipo.objects.all().filter(league_id=id)
        for eq in equipos:
            jugadores = Jugador.objects.all().filter(team_id=eq.id)
            for jugador in jugadores:
                jugador.times_trained += 1
                jugador.save()
        return Response(status=status.HTTP_200_OK)