from otree.api import *

doc = """
A splash-screen welcome page for the experiment
"""


class C(BaseConstants):
    NAME_IN_URL = "contest"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 2
    ENDOWMENT = Currency(10)
    COST_PER_TICKET = Currency(5)
    PRICE = Currency(8)


class Subsession(BaseSubsession): #This is where I define variables on the subsession (i.e. rounds) level
    is_paid = models.BooleanField()

    def setup_round(self):
        self.is_paid = True
        for group in self.get_groups():
            group.setup_round()


class Group(BaseGroup): #This is where I define variables on the group level
    prize = models.CurrencyField() #Stores the value of the prize of the lottery

    def setup_round(self):
        self.prize = C.PRICE
        for player in self.get_players():
            player.setup_round()


class Player(BasePlayer): #This is where I define variables on the player (i.e. individual) level
    endowment = models.CurrencyField()
    cost_per_ticket = models.CurrencyField()
    tickets_purchased = models.IntegerField() #The reason why I use models.IntegerField() and not tickets_purchased: int is because it links the input to the data or something like that.

    def setup_round(self):
        self.endowment = C.ENDOWMENT
        self.cost_per_ticket = C.COST_PER_TICKET




# def creating_session(subsession): #this function is called at the start of every round (and at the moment of creating the session) and is an alternative to making a waitpage as in SetupRound
#     subsession.setup_round()


class SetupRound(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession): #this function gets called once all players arrived at the waitpage
        subsession.setup_round()


class Intro(Page):
    pass


class Decision(Page):
    form_model = "player"
    form_fields = ["tickets_purchased"]


class DecisionWaitPage(WaitPage):
    pass


class Results(Page):
    pass


class EndBlock(Page):
    pass


page_sequence = [
    SetupRound,
    Intro,
    Decision,
    DecisionWaitPage,
    Results,
    EndBlock,
]
