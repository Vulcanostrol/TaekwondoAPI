from datetime import datetime

from django.contrib.auth.models import User

from tournament import models
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TournamentObjectTest(APITestCase):
    def setUp(self) -> None:
        superuser = User.objects.create_superuser("admin", "email@example.com", "admin")
        superuser.save()
        self.client.login(username="admin", password="admin")

    def test_get_tournament_list(self):
        url = reverse('tournament-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_tournament(self):
        url = reverse('tournament-list')
        data = {
            "name": "Testing Tournament!",
            "tournament_start": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "pools": [],
            "teams": [],
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Tournament.objects.count(), 1)
        self.assertEqual(models.Tournament.objects.get().name, 'Testing Tournament!')


class EndToEndTest(APITestCase):
    def setUp(self) -> None:
        superuser = User.objects.create_superuser("admin", "email@example.com", "admin")
        superuser.save()
        self.client.login(username="admin", password="admin")

    def create(self, url: str, data: dict) -> dict:
        response = self.client.post(
            reverse(url),
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.json()

    def test_signup_for_tournament(self):
        tournament = self.create(
            "tournament-list",
            {
                "name": "Testing Tournament!",
                "tournament_start": datetime.now(),
                "pools": [],
                "teams": [],
            },
        )

        team = self.create(
            "team-list",
            {
                "tournament": tournament["id"],
                "participants": [],
            },
        )

        self.create(
            "participant-list",
            {
                "team": team["id"],
                "name": "Test Participant",
                "belt_grade": models.Participant.BELT_GRADES[0][0],
                "sex": models.Participant.SEXES[0][0],
                "birthdate": datetime.today().strftime("%Y-%m-%d"),
            },
        )

        tournament_teams = models.Tournament.objects.get(id=tournament["id"]).teams
        self.assertEqual(tournament_teams.count(), 1)
        self.assertEqual(tournament_teams.first().participants.count(), 1)

        self.create(
            "participant-list",
            {
                "team": team["id"],
                "name": "Test Participant",
                "belt_grade": models.Participant.BELT_GRADES[0][0],
                "sex": models.Participant.SEXES[-1][0],
                "birthdate": datetime.today().strftime("%Y-%m-%d"),
            },
        )

        self.assertEqual(tournament_teams.first().participants.count(), 2)


class TestPoolCreation(APITestCase):
    def setUp(self) -> None:
        superuser = User.objects.create_superuser("admin", "email@example.com", "admin")
        superuser.save()
        self.client.login(username="admin", password="admin")

    def create(self, url: str, data: dict) -> dict:
        response = self.client.post(
            reverse(url),
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.json())
        return response.json()

    def make_tournament(self) -> dict:
        return self.create(
            "tournament-list",
            {
                "name": "Testing Tournament!",
                "tournament_start": datetime.now(),
                "pools": [],
                "teams": [],
            },
        )

    def make_team(self, tournament_id: int) -> dict:
        return self.create(
            "team-list",
            {
                "tournament": tournament_id,
                "participants": [],
            },
        )

    def make_participant(
            self,
            team_id: int,
            name: str,
            belt_grade: str = models.Participant.BeltGrades.White,
            sex: str = models.Participant.Sexes.Female,
            birthdate: str = datetime.today().strftime("%Y-%m-%d"),
    ) -> dict:
        return self.create(
            "participant-list",
            {
                "team": team_id,
                "name": name,
                "belt_grade":  belt_grade,
                "sex": sex,
                "birthdate": birthdate,
            },
        )

    def assert_tournament_pools(
            self,
            tournament_id: int,
            pool_amount: int,
            teams_per_pool: int,
            participants_per_team: int,
    ):
        tournament_obj = models.Tournament.objects.get(id=tournament_id)
        self.assertEqual(tournament_obj.pools.count(), pool_amount)
        for pool in tournament_obj.pools.all():
            self.assertEqual(pool.teams.count(), teams_per_pool)
            for team in pool.teams.all():
                self.assertEqual(team.participants.count(), participants_per_team)

    def test_with_one_team(self):
        tournament = self.make_tournament()
        self.make_participant(self.make_team(tournament["id"])["id"], "Alice")
        url = reverse('make-pools', args=[tournament["id"]])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_tournament_pools(tournament["id"], pool_amount=1, teams_per_pool=1, participants_per_team=1)

    def test_solo_sex_pools(self):
        tournament = self.make_tournament()
        self.make_participant(self.make_team(tournament["id"])["id"], "Alice", sex=models.Participant.Sexes.Female)
        self.make_participant(self.make_team(tournament["id"])["id"], "Bob", sex=models.Participant.Sexes.Male)
        self.make_participant(self.make_team(tournament["id"])["id"], "Christine", sex=models.Participant.Sexes.Female)
        self.make_participant(self.make_team(tournament["id"])["id"], "Dennis", sex=models.Participant.Sexes.Male)
        self.make_participant(self.make_team(tournament["id"])["id"], "Eva", sex=models.Participant.Sexes.Female)
        self.make_participant(self.make_team(tournament["id"])["id"], "Frank", sex=models.Participant.Sexes.Male)
        url = reverse('make-pools', args=[tournament["id"]])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_tournament_pools(tournament["id"], pool_amount=2, teams_per_pool=3, participants_per_team=1)

    def test_solo_belt_grade_pools(self):
        tournament = self.make_tournament()
        self.make_participant(self.make_team(tournament["id"])["id"], "Alice", sex=models.Participant.Sexes.Female,
                              belt_grade=models.Participant.BeltGrades.White)
        self.make_participant(self.make_team(tournament["id"])["id"], "Bob", sex=models.Participant.Sexes.Male,
                              belt_grade=models.Participant.BeltGrades.White)
        self.make_participant(self.make_team(tournament["id"])["id"], "Christine", sex=models.Participant.Sexes.Female,
                              belt_grade=models.Participant.BeltGrades.Yellow)
        self.make_participant(self.make_team(tournament["id"])["id"], "Dennis", sex=models.Participant.Sexes.Male,
                              belt_grade=models.Participant.BeltGrades.Yellow)
        self.make_participant(self.make_team(tournament["id"])["id"], "Eva", sex=models.Participant.Sexes.Female,
                              belt_grade=models.Participant.BeltGrades.Red)
        self.make_participant(self.make_team(tournament["id"])["id"], "Frank", sex=models.Participant.Sexes.Male,
                              belt_grade=models.Participant.BeltGrades.Red)
        url = reverse('make-pools', args=[tournament["id"]])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_tournament_pools(tournament["id"], pool_amount=6, teams_per_pool=1, participants_per_team=1)

    def test_belt_grade_groupings(self):
        # A class
        tournament = self.make_tournament()
        self.make_participant(self.make_team(tournament["id"])["id"], "A",
                              belt_grade=models.Participant.BeltGrades.White)
        self.make_participant(self.make_team(tournament["id"])["id"], "B",
                              belt_grade=models.Participant.BeltGrades.White_yellow)
        url = reverse('make-pools', args=[tournament["id"]])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_tournament_pools(tournament["id"], pool_amount=1, teams_per_pool=2, participants_per_team=1)

        # B class
        tournament = self.make_tournament()
        self.make_participant(self.make_team(tournament["id"])["id"], "A",
                              belt_grade=models.Participant.BeltGrades.Yellow)
        self.make_participant(self.make_team(tournament["id"])["id"], "B",
                              belt_grade=models.Participant.BeltGrades.Yellow_green)
        self.make_participant(self.make_team(tournament["id"])["id"], "C",
                              belt_grade=models.Participant.BeltGrades.Green)
        self.make_participant(self.make_team(tournament["id"])["id"], "D",
                              belt_grade=models.Participant.BeltGrades.Green_blue)
        url = reverse('make-pools', args=[tournament["id"]])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_tournament_pools(tournament["id"], pool_amount=1, teams_per_pool=4, participants_per_team=1)

        # C class
        tournament = self.make_tournament()
        self.make_participant(self.make_team(tournament["id"])["id"], "A",
                              belt_grade=models.Participant.BeltGrades.Blue)
        self.make_participant(self.make_team(tournament["id"])["id"], "B",
                              belt_grade=models.Participant.BeltGrades.Blue_red)
        self.make_participant(self.make_team(tournament["id"])["id"], "C",
                              belt_grade=models.Participant.BeltGrades.Red)
        self.make_participant(self.make_team(tournament["id"])["id"], "D",
                              belt_grade=models.Participant.BeltGrades.Red_black)
        url = reverse('make-pools', args=[tournament["id"]])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_tournament_pools(tournament["id"], pool_amount=1, teams_per_pool=4, participants_per_team=1)

        # D class
        tournament = self.make_tournament()
        self.make_participant(self.make_team(tournament["id"])["id"], "A",
                              belt_grade=models.Participant.BeltGrades.Dan_1)
        self.make_participant(self.make_team(tournament["id"])["id"], "B",
                              belt_grade=models.Participant.BeltGrades.Dan_2)
        self.make_participant(self.make_team(tournament["id"])["id"], "C",
                              belt_grade=models.Participant.BeltGrades.Dan_3)
        self.make_participant(self.make_team(tournament["id"])["id"], "D",
                              belt_grade=models.Participant.BeltGrades.Dan_4)
        self.make_participant(self.make_team(tournament["id"])["id"], "E",
                              belt_grade=models.Participant.BeltGrades.Dan_5)
        url = reverse('make-pools', args=[tournament["id"]])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_tournament_pools(tournament["id"], pool_amount=1, teams_per_pool=5, participants_per_team=1)
