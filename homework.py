import datetime as dt
from typing import Optional

DATE_FORMAT = '%d.%m.%Y'


class Calculator:
    def __init__(self, limit: float) -> None:
        self.limit = limit
        self.records = []

    def add_record(self, record: 'Record') -> None:
        """Сохраняет новую запись о расходах/приемах пищи."""
        self.records.append(record)

    def get_today_stats(self):
        """Суммирует деньги/ккал за сегодняшний день."""
        today_date = dt.date.today()
        return sum(record.amount for record in self.records
                   if record.date == today_date)

    def get_week_stats(self) -> int:
        """Суммирует деньги/ккал за прошедшие 7 дней."""
        today_date = dt.date.today()
        week_period = dt.timedelta(days=7)
        week_ago = today_date - week_period
        return sum(record.amount for record in self.records
                   if today_date >= record.date > week_ago)

    def get_remainder(self) -> int:
        """Высчитывает остаток на сегодня."""
        return self.limit - self.get_today_stats()


class Record:
    def __init__(self, amount: float, comment: str,
                 date: Optional[str] = None) -> None:
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, DATE_FORMAT).date()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self) -> str:
        """Определяет, сколько ещё калорий можно/нужно получить сегодня."""
        calories_remained = self.get_remainder()
        if calories_remained > 0:
            return('Сегодня можно съесть что-нибудь ещё, '
                   'но с общей калорийностью не '
                   f'более {calories_remained} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    RUB_RATE = 1.0
    USD_RATE = 74.25
    EURO_RATE = 87.72

    def get_today_cash_remained(self, currency: float) -> str:
        """Определяет, сколько ещё денег можно потратить сегодня в рублях,
        долларах или евро."""
        currency_r = {
            'rub': ('руб', self.RUB_RATE),
            'usd': ('USD', self.USD_RATE),
            'eur': ('Euro', self.EURO_RATE)
        }
        if currency not in currency_r.values:
            raise ValueError('Такой валюты нет')
        cash_remained = self.get_remainder()
        if cash_remained == 0:
            return 'Денег нет, держись'
        currency_name, currency_rate = currency_r[currency]
        rate_all = abs(round(cash_remained / currency_rate, 2))
        if cash_remained > 0:
            return('На сегодня осталось '
                   f'{rate_all} {currency_name}')
        return('Денег нет, держись: твой долг '
               f'- {rate_all} {currency_name}')
