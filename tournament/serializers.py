from rest_framework import serializers

import tournament.models as models


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tournament
        fields = ["id", "name", "tournament_start", "created", "pools", "teams"]


class PoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pool
        fields = ["id", "tournament", "rounds", "teams"]


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = ["id", "tournament", "pool", "participants"]


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Participant
        fields = ["id", "team", "name", "belt_grade", "sex", "birthdate"]


class RoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Round
        fields = ["id", "pool", "round_number", "turns"]


class TurnSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Turn
        fields = ["id", "round", "turn_order", "team"]


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Form
        fields = ["id", "turn"]


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Score
        fields = ["id", "form", "technique_score", "presentation_score"]
