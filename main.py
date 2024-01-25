from position import Position
import csv

positions = []
invested = 0

def read_csv(file_path = "ms.csv"):
    data = []
    with open(file_path, 'r', newline=None, encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            # Strip double quotes from each element and append to the data list
            opened = float(row[1].strip('"'))
            closed = float(row[4].strip('"'))
            add_position((opened + closed) / 2)
    return data

def add_position(price_now):
    invest = 50
    global invested
    invested = invested + invest * 2
    positions.append(Position(price_now, 0.2, 100, invest))
    for position in positions:
        position.eval(price_now)

def count_liquidated(mode):
    count = 0
    for position in positions:
        if mode == "short" and position.short_liquidated:
            count = count + 1
        if mode == "long" and position.long_liquidated:
            count = count + 1
    return count

def count_lost():
    count = 0
    for position in positions:
        if position.short_liquidated and position.long_liquidated:
            count = count + 1
    return count

def count_win():
    count = 0
    for position in positions:
        if position.long_liquidated == False and position.short_liquidated == True and position.closed:
            count = count + 1
        if position.long_liquidated == True and position.short_liquidated == False and position.closed:
            count = count + 1
    return count

def get_balance():
    balance = 0
    for position in positions:
        balance = balance + position.current_balance
    return balance

def get_balance_from_sold():
    balance = 0
    for position in positions:
        if position.closed:
            balance = balance + position.balance
    return balance

def count_still_open():
    count = 0
    for position in positions:
        if position.closed == False:
            count = count + 1
    return count



read_csv()
short_liquidated = count_liquidated("short")
long_liquidated = count_liquidated("long")
absolute_lost_count = count_lost()
absolute_win_count = count_win()
balance = round(get_balance(), 2)
still_open = count_still_open()
profit_from_sold = round(balance - invested, 2)
money_lost = absolute_lost_count * 100

for position in positions:
    print(position)

print(f"Number of Entries: {len(positions)}")
# print(f"Short liquidated: {short_liquidated}")
# print(f"Long liquidated: {long_liquidated}")
print(f"Successful sold for profit: {absolute_win_count}")
print(f"Both liquidated: {absolute_lost_count}")
print(f"Still open: {still_open}\n")

print(f"leverage: {positions[0].leverage}")
print(f"Sell at 20%\n")

print(f"Entry amount per position: 50 $")
print(f"Invested: {invested} $")
print(f"Money lost: {money_lost}")
print(f"Current balance {balance} $")
print(f"Profit from sold positions: {profit_from_sold} $")
print(f"Overal profit: {profit_from_sold / invested * 100} %")

