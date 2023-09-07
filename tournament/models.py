from django.db import models


class Tournament(models.Model):
    name = models.CharField(
        max_length=32,
        blank=False,
    )
    tournament_start = models.DateTimeField(
        blank=False,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self) -> str:
        return f"({self.pk}) {self.name}"


class Pool(models.Model):
    """" A pool is a grouping of participants that compete with each other in a tournament. """
    tournament = models.ForeignKey(
        "Tournament",
        related_name="pools",
        on_delete=models.CASCADE,
    )

    class PoolType:
        Solo: str = "S"
        Pair: str = "P"
        Team: str = "T"
        Para: str = "X"
    POOL_TYPES = [
        (PoolType.Solo, "Solo"),
        (PoolType.Pair, "Pair"),
        (PoolType.Team, "Team"),
    ]
    pool_type = models.CharField(
        max_length=1,
        choices=POOL_TYPES,
        blank=False,
    )


class Team(models.Model):
    """" A tournament signup, linked to one or more participants. """
    tournament = models.ForeignKey(
        "Tournament",
        related_name="teams",
        on_delete=models.CASCADE,
    )
    pool = models.ForeignKey(
        "Pool",
        related_name="teams",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        if self.participants.count() > 0:
            return f"({self.pk}) {' & '.join([str(p) for p in self.participants.all()])}"
        else:
            return f"({self.pk}) Empty team"


class Participant(models.Model):
    team = models.ForeignKey(
        "Team",
        related_name="participants",
        on_delete=models.CASCADE,
    )

    class BeltGrades:
        White: str = "WH"
        White_yellow: str = "WY"
        Yellow: str = "YE"
        Yellow_green: str = "YG"
        Green: str = "GR"
        Green_blue: str = "GB"
        Blue: str = "BL"
        Blue_red: str = "BR"
        Red: str = "RE"
        Red_black: str = "RB"
        Dan_1: str = "1D"
        Dan_2: str = "2D"
        Dan_3: str = "3D"
        Dan_4: str = "4D"
        Dan_5: str = "5D"
    BELT_GRADES = [
        (BeltGrades.White, "White"),
        (BeltGrades.White_yellow, "White-yellow"),
        (BeltGrades.Yellow, "Yellow"),
        (BeltGrades.Yellow_green, "Yellow-green"),
        (BeltGrades.Green, "Green"),
        (BeltGrades.Green_blue, "Green-blue"),
        (BeltGrades.Blue, "Blue"),
        (BeltGrades.Blue_red, "Blue-red"),
        (BeltGrades.Red, "Red"),
        (BeltGrades.Red_black, "Red-black"),
        (BeltGrades.Dan_1, "1st Dan"),
        (BeltGrades.Dan_2, "2nd Dan"),
        (BeltGrades.Dan_3, "3rd Dan"),
        (BeltGrades.Dan_4, "4th Dan"),
        (BeltGrades.Dan_5, "5th Dan"),
    ]
    name = models.CharField(
        max_length=128,
        blank=False,
    )
    belt_grade = models.CharField(
        max_length=2,
        choices=BELT_GRADES,
        blank=False,
    )

    class Sexes:
        Female: str = "F"
        Male: str = "M"
    SEXES = [
        (Sexes.Female, "Female"),
        (Sexes.Male, "Male"),
    ]
    sex = models.CharField(
        max_length=1,
        choices=SEXES,
        blank=False,
    )
    birthdate = models.DateField(
        blank=False,
    )

    def __str__(self) -> str:
        return f"{self.name} ({self.sex[0]})"


class Round(models.Model):
    """" A round contains a schedule for all participants that made it to the round. """
    pool = models.ForeignKey(
        "Pool",
        related_name="rounds",
        on_delete=models.CASCADE,
    )
    round_number = models.PositiveSmallIntegerField(
        blank=False,
    )

    def __str__(self) -> str:
        return f"Pool {self.pool.pk} - round {self.round_number}"


class Turn(models.Model):
    """ A turn of a participant: multiple forms (and scores) per turn. """
    round = models.ForeignKey(
        "Round",
        related_name="turns",
        on_delete=models.CASCADE,
    )
    turn_order = models.PositiveIntegerField(
        blank=False,
    )
    team = models.ForeignKey(
        "Team",
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['round', 'turn_order'], name='unique_migration_host_combination'
            )
        ]

    def __str__(self) -> str:
        return f"({self.pk}) {self.round} - turn {self.turn_order}"


class Form(models.Model):
    turn = models.ForeignKey(
        "Turn",
        related_name="forms",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.turn} - form {self.pk}"


class Score(models.Model):
    form = models.ForeignKey(
        "Form",
        related_name="scores",
        on_delete=models.CASCADE,
    )
    technique_score = models.PositiveIntegerField(
        blank=False,
    )
    presentation_score = models.PositiveIntegerField(
        blank=False,
    )
