import random
import datetime
from string import ascii_lowercase


class IntColumnDataGenerator:
    """
    Class for generating integer value between lower and upper bound
    """
    def __init__(self, lower_bound_: int, upper_bound_: int):
        self._lower_bound = lower_bound_
        self._upper_bound = upper_bound_

    def dump_int_value(self) -> int:
        """
        Return randomly generated integer value
        """
        res = random.randint(self._lower_bound, self._upper_bound)
        return res


class StringColumnDataGenerator:
    """
    Class for generating string value of a length between min and max values
    """
    def __init__(self, min_len_: int, max_len_: int):
        self._min_len = min_len_
        self._max_len = max_len_

    def dump_str_value(self) -> str:
        """
        Return randomly generated string value
        """
        res = ''.join(
            random.choice(ascii_lowercase)
            for _ in range(random.randint(self._min_len, self._max_len))
        )
        return res


class JobColumnDataGenerator:
    """
    Class for generating random IT job name
    """
    LEVEL_CHOICES = ['Trainee', 'Junior', 'Middle', 'Senior', 'Lead']
    LANGUAGE_CHOICES = ['Python', 'Java', 'Go', 'Ruby', 'C#', 'C++', 'C']

    def dump_job_value(self) -> str:
        """
        Return randomly generated job name
        """
        level = random.choice(self.LEVEL_CHOICES)
        language = random.choice(self.LANGUAGE_CHOICES)
        return f'{level} {language} developer'


class PhoneColumnDataGenerator:
    """
    Class for generating phone with a +380 at the begging
    """
    @staticmethod
    def dump_phone_value() -> str:
        """
        Return randomly generated phone as a string value
        """
        phone = '+380'
        for _ in range(9):
            phone += str(random.randint(0, 9))
        return phone


class DateColumnDataGenerator:
    """
    Class for generating random date
    """
    @staticmethod
    def dump_date_value() -> datetime.datetime:
        """
        Return randomly generated date
        """
        nowadays = datetime.datetime.now()
        res_dt = nowadays - datetime.timedelta(days=random.randint(0, 365*10))
        return res_dt
