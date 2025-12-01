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
    
def iter_months(start_year, start_month, end_year, end_month):
    for year in range(start_year, end_year+1):
        for month in range(1, 12+1):
            
            # skip months before or after our defined time range
            if (year,month) < (start_year,start_month):
                continue
            if (year,month) > (end_year,end_month):
                continue

            # yield iter
            yield year, month
