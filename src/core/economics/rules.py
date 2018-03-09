from typing import List


class EconomyCropRulesException(Exception):
    pass


class EconomyCropRules:
    def __init__(self, increase: float, decrease: float, min_value: int, max_value: int):
        self._increase = increase
        self._decrease = decrease
        self._min_value = min_value
        self._max_value = max_value

    # @staticmethod
    # def check_params(**kwargs) -> None:
    #     for key, value in kwargs.items():
    #         k_min, k_max = [getattr(eco_const, key.upper() + '_' + i) for i in ('MIN', 'MAX')]
    #         if k_min < value < k_max:
    #             continue
    #         raise EconomyCropRulesException('Cannot set {key}: {value} not in range ({k_min}, {k_max})'.format(
    #             key=key,
    #             value=value,
    #             k_min=k_min,
    #             k_max=k_max,
    #         ))

    def set_values_diff(self, increase: float, decrease: float) -> None:
        # self.check_params(increase=increase, decrease=decrease)
        self._increase = increase
        self._decrease = decrease

    def get_values_diff(self) -> List[float]:
        return self._increase, self._decrease

    def set_value_range(self, min_value: int, max_value: int) -> None:
        # self.check_params(min_value=min_value, max_value=max_value)
        if min_value > max_value:
            raise EconomyCropRulesException('Cannot set min_value/max_value: min_value > max_value')
        self._min_value = min_value
        self._max_value = max_value

    def get_value_range(self) -> List[float]:
        return self._min_value, self._max_value
