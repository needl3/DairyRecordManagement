import datetime
today = datetime.date.today()
first = today.replace(day=1)
lastMonth = first - datetime.timedelta(days=1)
print(lastMonth.strftime("%Y/%m"))