import re


def fill_str_date(date: str, year_start: bool = False, year_end: bool = False) -> str:
    """ Fill a date string with the missing month and day if needed, useful for Odoo domains"""
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date):
        return date

    elif re.match(r'^\d{4}$', date):
        assert not (year_start and year_end), "You can't set both year_start and year_end to True"
        if year_start:
            return f"{date}-01-01"
        elif year_end:
            return f"{date}-12-31"
        raise ValueError("You must set either year_start or year_end to True")

    raise ValueError("Invalid date format: %s" % date)
