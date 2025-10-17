import re

YEAR = 'YEAR'
MONTH = 'MONTH'
WEEK = 'WEEK'
DAY = 'DAY'

def detect_period_type(s):
    # TODO: more robust parsing of period types and maybe even using external library
    s = str(s).strip()
    if re.fullmatch(r"\d{4}$", s):
        return YEAR
    elif re.fullmatch(r"\d{6}$", s) or re.fullmatch(r"\d{4}-\d{2}$", s):
        return MONTH
    elif re.fullmatch(r"\d{4}-W\d{2}$", s):
        return WEEK
    elif re.fullmatch(r"\d{8}$", s) or re.fullmatch(r"\d{4}-\d{2}-\d{2}$", s):
        return DAY
    else:
        return None
    