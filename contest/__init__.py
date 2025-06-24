from otree.api import (
    BaseConstants,
    BaseGroup,
    BasePlayer,
    BaseSubsession,
    Page,
)
from otree.views import WaitPage

doc = """
A splash-screen welcome page for the experiment
"""


class C(BaseConstants):
    NAME_IN_URL = "contest"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class SetupRound(WaitPage):
    pass


class Intro(Page):
    pass


class Decision(Page):
    pass


class DecisionWaitPage(WaitPage):
    pass


class Results(Page):
    pass


class EndBlock(Page):
    pass


page_sequence = [
    #SetupRound,
    Intro,
    Decision,
    #DecisionWaitPage,
    Results,
    EndBlock,
]
