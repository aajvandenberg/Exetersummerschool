import random
import string
import time

from otree.api import *
from otree.models import player

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'encryption'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3
    TIME_FOR_TASK = 300
    LOOKUP_TABLES = [
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "ABCDEFGHIJKLMNOPQRSTUVWXZY",
        "ABCDEFGHIJKLMNOPQRSTUVWZYX",
    ]


class Subsession(BaseSubsession):
    random_seed = models.IntegerField()
    payment_per_correct = models.CurrencyField()
    lookup_table = models.StringField()
    time_for_task = models.FloatField()
    word = models.StringField()

    def setup_round(self):
        if self.round_number == 1:
            self.random_seed = self.session.config.get("random_seed", 12345678)
            random.seed(self.random_seed)
        self.payment_per_correct = Currency(0.10)
        self.time_for_task = C.TIME_FOR_TASK
        self.lookup_table = C.LOOKUP_TABLES[(self.round_number - 1) % 3]
        self.word = "".join(random.choices(string.ascii_uppercase, k=5))

    @property
    def lookup_dict(self):
        lookup = {}
        for letter in string.ascii_uppercase:
            lookup[letter] = self.lookup_table.index(letter)
        return lookup

    @property
    def correct_response(self):
        return [self.lookup_dict[letter] for letter in self.word]

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    started_task_at = models.FloatField()
    response_1 = models.IntegerField()
    response_2 = models.IntegerField()
    response_3 = models.IntegerField()
    response_4 = models.IntegerField()
    response_5 = models.IntegerField()
    is_correct = models.BooleanField()

    @property
    def response(self):
        return[self.response_1, self.response_2, self.response_3,
               self.response_4, self.response_5]

    @property
    def response_fields(self): #HELP
        return["response_1", "response_2", "response_3","response_4","response_5"]

    def check_response(self):
        self.is_correct = self.response == self.subsession.correct_response
        if self.is_correct:
            self.payoff = self.subsession.payment_per_correct

    def start_task(self):
        self.started_task_at = time.time()

    def get_time_elapsed(self):
        return time.time() - self.in_round(1).started_task_at

    def get_time_remaining(self):
        return self.subsession.in_round(1).time_for_task - self.get_time_elapsed()

def creating_session(subsession):
    subsession.setup_round()


# PAGES
class Intro(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.start_task()

class Decision(Page):
    form_model = "player"

    @staticmethod
    def get_timeout_seconds(player):
        return player.get_time_remaining()

    @staticmethod
    def get_form_fields(self):
        return self.response_fields


    @staticmethod
    def before_next_page(player, timeout_happened):
        player.check_response()


class Results(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS



page_sequence = [Intro,
                 Decision,
                 Results]
