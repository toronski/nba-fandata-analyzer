from datetime import datetime

def get_current_season():
    current_year = datetime.now().year
    previous_year = current_year - 1

    current_season = f"{previous_year}-{split_year(current_year)}"

    return current_season

def split_year(year):
    year = str(year)
    year_split = year.split('0', 1)
    year_ready = year_split[1]

    return year_ready
