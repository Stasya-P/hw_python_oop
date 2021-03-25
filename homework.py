import datetime as dt

date_format = '%d.%m.%Y'


class Calculator:
    def __init__(self, limit) -> None:
        self.limit = limit
        self.records = []

# Сохраняем новую запись о расходах/приемах пищи
    def add_record(self, record):
        self.records.append(record)

    # Суммируем деньги/ккал за сегодняшний день
    def get_today_stats(self):
        day_sum: int = 0
        for record in self.records:
            if record.date == dt.datetime.now().date():
                day_sum += record.amount
        return day_sum

# Суммируем деньги/ккал за прошедшие 7 дней
    def get_week_stats(self):
        week_sum: int = 0
        self.week_period = dt.timedelta(days=7)
        self.week_ago = dt.date.today() - self.week_period
        for record in self.records:
            if dt.date.today() >= record.date >= self.week_ago:
                week_sum += record.amount
        return(week_sum)


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        if self.get_today_stats() < self.limit:
            calories_remained = self.limit - self.get_today_stats()
            return('Сегодня можно съесть что-нибудь ещё, '
                   'но с общей калорийностью не '
                   f'более {calories_remained} кКал')
        else:
            return('Хватит есть!')


class Record:
    def __init__(self, amount, date=None, comment=''):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, ('%d.%m.%Y')).date()


class CashCalculator(Calculator):
    RUB_RATE = 1.0
    USD_RATE = 74.25
    EURO_RATE = 87.72
    CURRENCY_R = {
        'rub': [RUB_RATE, 'руб'],
        'usd': [USD_RATE, 'USD'],
        'eur': [EURO_RATE, 'Euro']}

    def get_today_cash_remained(self, currency):
        self.CURRENCY_R = {
            'rub': ['руб', self.RUB_RATE],
            'usd': ['USD', self.USD_RATE],
            'eur': ['Euro', self.EURO_RATE]
        }
        cash_remained = self.limit - self.get_today_stats()
        currency_rate = self.CURRENCY_R[currency][1]
        currency_name = self.CURRENCY_R[currency][0]
        rate_all = round(cash_remained / currency_rate, 2)
        if self.get_today_stats() < self.limit:
            return('На сегодня осталось '
                   f'{rate_all} {currency_name}')
        elif self.get_today_stats() == self.limit:
            return ('Денег нет, держись')
        else:
            return('Денег нет, держись: твой долг '
                   f'- {abs(rate_all)} {currency_name}')
