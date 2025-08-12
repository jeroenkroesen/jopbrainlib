"""Support functions to deal with time
"""
import pendulum
from typing import List



def get_days_in_month(year: int, month: int) -> List[pendulum.DateTime]:
    """Get all days in a month

    Parameters
    ----------
    year : int
        The year as an integer (2025, NOT 25, unless you mean the 
        actual year 0025)
    month : int
        The month as an integer (1 - 12)

    Returns
    -------
    list[pendulum.DateTime]
        A list where each item is a DateTime representing a day in the 
        specified year-month period.

    Raises
    ------
        TypeError: If year or month are not integers.
        ValueError: If year or month are outside their valid ranges.
    """
    # Input Validation
    if not isinstance(year, int) or not isinstance(month, int):
        raise TypeError("Year and month must be integers.")
    if not (1 <= month <= 12):
        raise ValueError("Month must be between 1 and 12.")
    if not (1 <= year <= 9999):  # Basic sanity check for year
        raise ValueError("Year must be between 1 and 9999")
 
    start_date = pendulum.datetime(year, month, 1)
    end_date = start_date.end_of('month')
    days = []
    current_date = start_date
    
    while current_date <= end_date:
        days.append(current_date)
        current_date = current_date.add(days=1)
        
    return days
