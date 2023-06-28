def get_weekday_from_absdate(absdate):
  return absdate % 7

def leap_gregorian(year):
  if ((year % 4) == 0) and \
     ((year % 400) != 100) and \
     ((year % 400) != 200) and \
     ((year % 400) != 300):
    return True
  else:
    return False

def last_day_of_gregorian_month(month, year):
  if leap_gregorian(year) == True and month == 2:
    return 29
  else:
    lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return lengths[month-1]

def hebrew_leap(year):
  if ((((year*7)+1) % 19) < 7):
    return True
  else:
    return False

def hebrew_year_months(year):
  if hebrew_leap(year):
    return 13
  else:
    return 12

def _hebrew_calendar_elapsed_days(year):
  value = 235 * ((year-1) // 19)
  monthsElapsed = value

  value = 12 * ((year-1) % 19)
  monthsElapsed += value

  value = ((((year-1) % 19) * 7) + 1) // 19
  monthsElapsed += value;

  partsElapsed = (((monthsElapsed % 1080) * 793) + 204)
  hoursElapsed = (5 +
                   (monthsElapsed * 12) + \
                   ((monthsElapsed // 1080) * 793) + \
                   (partsElapsed // 1080));

  day = 1 + (29 * monthsElapsed) + (hoursElapsed//24)

  parts = ((hoursElapsed % 24) * 1080) + \
           (partsElapsed % 1080)

  if ((parts >= 19440) or \
      (((day % 7) == 2) and \
       (parts >= 9924)  and \
       (not hebrew_leap(year))) or \
      (((day % 7) == 1) and \
       (parts >= 16789) and \
       (hebrew_leap(year-1)))):
    alternativeDay = day+1
  else:
    alternativeDay = day

  if (((alternativeDay % 7) == 0) or \
      ((alternativeDay % 7) == 3) or \
      ((alternativeDay % 7) == 5)):
    alternativeDay += 1

  return alternativeDay

def days_in_hebrew_year(year):
  return (_hebrew_calendar_elapsed_days(year+1) - \
          _hebrew_calendar_elapsed_days(year))

def _long_heshvan(year):
  if ((days_in_hebrew_year(year) % 10) == 5):
    return True
  else:
    return False

def _short_kislev(year):
  if ((days_in_hebrew_year(year) % 10) == 3):
    return True
  else:
    return False

def hebrew_month_days(year, month):
  if ((month == 2) or \
      (month == 4) or \
      (month == 6) or \
      (month == 10) or \
      (month == 13)):
    return 29
  if ((month == 12) and (not hebrew_leap(year))):
    return 29
  if ((month == 8) and (not _long_heshvan(year))):
    return 29
  if ((month == 9) and (_short_kislev(year))):
    return 29
  return 30

def hebrew_to_absdate(year, month, day):
  value = day
  returnValue = value

  if month < 7:
    for m in range(7,hebrew_year_months(year)+1):
      value = hebrew_month_days(year, m)
      returnValue += value
    for m in range(1,month):
      value = hebrew_month_days(year, m)
      returnValue += value
  else:
    for m in range(7,month):
      value = hebrew_month_days(year, m)
      returnValue += value

  value = _hebrew_calendar_elapsed_days(year)
  returnValue += value

  value = 1373429
  returnValue -= value

  return returnValue

def absdate_to_hebrew(absdate): # year, month, day
  approx = (absdate+1373429) // 366

  y = approx
  while 1:
    temp = hebrew_to_absdate(y+1, 7, 1)
    if absdate < temp:
      break
    y += 1
  year = y

  temp = hebrew_to_absdate(year, 1, 1)
  if absdate < temp:
    start = 7
  else:
    start = 1

  m = start
  while 1:
    temp = hebrew_to_absdate(year, m, hebrew_month_days(year, m))
    if absdate <= temp:
      break
    m += 1
  month = m

  temp = hebrew_to_absdate(year, month, 1)
  day = absdate-temp+1

  return (year, month, day)

def gregorian_to_absdate(year, month, day):
  value = day
  returnValue = value

  for m in range(1,month):
    value = last_day_of_gregorian_month(m, year)
    returnValue += value

  value = (365 * (year-1))
  returnValue += value

  value = ((year-1) // 4)
  returnValue += value

  value = ((year-1) // 100)
  returnValue -= value

  value = ((year-1) // 400)
  returnValue += value

  return returnValue

def absdate_to_gregorian(absdate):
  approx = absdate // 366

  y = approx
  while 1:
    temp = gregorian_to_absdate(y+1, 1, 1)
    if (absdate < temp):
      break
    y += 1
  year = y

  m = 1
  while 1:
    temp = gregorian_to_absdate(year, m, last_day_of_gregorian_month(m, year))
    if (absdate <= temp):
      break
    m += 1
  month = m

  temp = gregorian_to_absdate(year, month, 1)
  day = absdate-temp+1;

  return (year, month, day)
