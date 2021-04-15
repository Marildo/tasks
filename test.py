from datetime import datetime

hoje = datetime.today()

fom = f"day-{datetime.strftime(datetime.today(), '%d-%m-%Y')}.csv"

print(fom)
 
