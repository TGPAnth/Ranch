from src.core.economics.rules import EconomyCropRules


class Crop:
    def __init__(self, **kwargs):
        self.economy_rules = self.set_economy_rules(**kwargs['economics'])

    def set_economy_rules(self, **kwargs):
        return EconomyCropRules(**kwargs)
