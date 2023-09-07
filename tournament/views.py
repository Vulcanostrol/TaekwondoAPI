from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import tournament.models as models
import tournament.serializers as serializers
from tournament.rules import belt_grade_to_class, D_CLASS, make_tournament_pools, tournament_pools_walker


class MakePoolsEndpoint(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk: int):
        tournament = models.Tournament.objects.get(id=pk)
        pools = make_tournament_pools(tournament)
        for pool in tournament_pools_walker(pools):
            pool.save()

        teams = models.Team.objects.filter(tournament=tournament)
        team: models.Team
        for team in teams:
            team_class = D_CLASS  # Default
            participant: models.Participant
            for participant in team.participants.all():
                belt_grade = participant.belt_grade
                participant_class = belt_grade_to_class(belt_grade)
                if participant_class.level > team_class.level:
                    team_class = participant_class
            if team.participants.count() == 1:
                team.pool = pools[team_class][models.Pool.PoolType.Solo][team.participants.first().sex]
            elif team.participants.count() == 2:
                team.pool = pools[team_class][models.Pool.PoolType.Pair][models.Participant.Sexes.Female]
            elif team.participants.count() > 2:
                team.pool = pools[team_class][models.Pool.PoolType.Team][team.participants.first().sex]
            else:
                raise ValueError(f"Team {team} has no participants.")
            team.save(update_fields=["pool"])
        for pool in tournament.pools.all():
            if pool.teams.count() == 0:
                pool.delete()

        return Response(serializers.TournamentSerializer(tournament).data)


class TournamentList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = models.Tournament.objects.all()
    serializer_class = serializers.TournamentSerializer


class TournamentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = models.Tournament.objects.all()
    serializer_class = serializers.TournamentSerializer


class PoolList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = models.Pool.objects.all()
    serializer_class = serializers.PoolSerializer


class PoolDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = models.Pool.objects.all()
    serializer_class = serializers.PoolSerializer


class TeamList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer


class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer


class ParticipantList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = models.Participant.objects.all()
    serializer_class = serializers.ParticipantSerializer


class ParticipantDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = models.Participant.objects.all()
    serializer_class = serializers.ParticipantSerializer


class RoundList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = models.Round.objects.all()
    serializer_class = serializers.RoundSerializer


class RoundDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = models.Round.objects.all()
    serializer_class = serializers.RoundSerializer


class TurnList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = models.Turn.objects.all()
    serializer_class = serializers.TurnSerializer


class TurnDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = models.Turn.objects.all()
    serializer_class = serializers.TurnSerializer


class FormList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = models.Form.objects.all()
    serializer_class = serializers.FormSerializer


class FormDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = models.Form.objects.all()
    serializer_class = serializers.FormSerializer


class ScoreList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = models.Score.objects.all()
    serializer_class = serializers.ScoreSerializer


class ScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = models.Score.objects.all()
    serializer_class = serializers.ScoreSerializer
