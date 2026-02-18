import datetime

x = datetime.date.today()
print(x - datetime.timedelta(days=5))

x = datetime.date.today()
y = datetime.date(*list(map(int, input("Input \"year month day\": ").split())))
print(f"Days between today and {y}: {x-y}")

x = datetime.datetime.now().replace(microsecond=0)
print(x)

x = datetime.date.today()
print(f"Yesterday: {x - datetime.timedelta(days=1)}\nToday: {x}\nTomorrow: {x + datetime.timedelta(days=1)}")