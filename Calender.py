import time
from datetime import datetime
import pytz
from enum import Enum


class Term_modes(Enum):
    FARD = 0
    ZOJ = 1
    TABESTAN = 2


class Calander:
    months = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']

    def __init__(self):
        d = time.localtime()
        t = datetime.now(pytz.timezone('Asia/Tehran'))
        [self.year, self.month, self.day] = self.gregorian_to_jalali(d.tm_year, d.tm_mon, d.tm_mday)
        [self.hour, self.minute, self.second] = [t.hour, t.minute, t.second]

        if (7 <= self.month < 11) or (self.month == 11 and self.day < 10):
            self.term_month = Calander.months[6:11]
            self.term_mode = Term_modes.FARD
        elif self.month >= 11 or self.month <= 3 or (self.month == 4 and self.day <= 15):
            self.term_month = (Calander.months[10:])
            self.term_month.extend(Calander.months[0:4])
            self.term_mode = Term_modes.ZOJ
        else:
            self.term_month = Calander.months[3:6]
            self.term_mode = Term_modes.TABESTAN
        print(self.term_month)

    def update_time(self):
        self.__init__()

    def academic_year(self):
        if self.term_mode == Term_modes.FARD or self.term_mode == Term_modes.TABESTAN:
            return [self.year, self.year + 1]
        elif self.term_mode == Term_modes.ZOJ and self.month >= 11:
            return [self.year, self.year + 1]
        else:
            return [self.year - 1, self.year]

    def month_to_end_of_term(self):
        if self.term_mode == Term_modes.FARD:
            return self.term_month[self.month - 7:]
        elif self.term_mode == Term_modes.ZOJ:
            return self.term_month[self.month - 11 if self.month >= 11 else self.month + 1:]
        else:
            return self.term_month[self.month - 4:]

    @staticmethod
    def gregorian_to_jalali(gy, gm, gd):
        g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
        if gm > 2:
            gy2 = gy + 1
        else:
            gy2 = gy
        days = 355666 + (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99) // 100) + ((gy2 + 399) // 400) + gd + g_d_m[
            gm - 1]
        jy = -1595 + (33 * (days // 12053))
        days %= 12053
        jy += 4 * (days // 1461)
        days %= 1461
        if days > 365:
            jy += (days - 1) // 365
            days = (days - 1) % 365
        if days < 186:
            jm = 1 + (days // 31)
            jd = 1 + (days % 31)
        else:
            jm = 7 + ((days - 186) // 30)
            jd = 1 + ((days - 186) % 30)
        return [jy, jm, jd]

    @staticmethod
    def jalali_to_gregorian(jy, jm, jd):
        jy += 1595
        days = -355668 + (365 * jy) + ((jy // 33) * 8) + (((jy % 33) + 3) // 4) + jd
        if jm < 7:
            days += (jm - 1) * 31
        else:
            days += ((jm - 7) * 30) + 186
        gy = 400 * (days // 146097)
        days %= 146097
        if days > 36524:
            days -= 1
            gy += 100 * (days // 36524)
            days %= 36524
            if days >= 365:
                days += 1
        gy += 4 * (days // 1461)
        days %= 1461
        if days > 365:
            gy += ((days - 1) // 365)
            days = (days - 1) % 365
        gd = days + 1
        if (gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0):
            kab = 29
        else:
            kab = 28
        sal_a = [0, 31, kab, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        gm = 0
        while gm < 13 and gd > sal_a[gm]:
            gd -= sal_a[gm]
            gm += 1
        return [gy, gm, gd]
