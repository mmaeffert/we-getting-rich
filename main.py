from position import Position
import csv

positions = []
invested = 0
lev = 10

def read_csv(file_path="data.csv"):
    with open(file_path, 'r', newline=None, encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            average_price = (float(row[1].strip('"')) + float(row[4].strip('"'))) / 2
            add_position(average_price)

def add_position(price_now):
    global invested
    invest_amount = 50
    invested += invest_amount * 2
    position = Position(price_now, lev, invest_amount)
    # Pass the soft_liquidation_percentage here (10% for +10% soft liquidation)
    position.soft_liquidation_percentage = 0.10
    positions.append(position)
    for position in positions:
        position.evaluate_position(price_now)

def count_closed_positions():
    return sum(1 for position in positions if position.is_closed)

def count_positions_with_profit():
    return sum(1 for position in positions if position.is_closed and position.current_balance > position.investment * 2)

def count_positions_with_loss():
    return sum(1 for position in positions if position.is_closed and position.current_balance <= position.investment * 2)

def get_total_balance():
    return sum(position.current_balance for position in positions)

def count_still_open_positions():
    return sum(1 for position in positions if not position.is_closed)

def get_balance_from_closed_positions():
    return sum(position.current_balance for position in positions if position.is_closed)

# Run the simulation
read_csv()

# Calculate and display statistics
total_positions = len(positions)
closed_positions = count_closed_positions()
positions_with_profit = count_positions_with_profit()
positions_with_loss = count_positions_with_loss()
balance = round(get_total_balance(), 2)
still_open = count_still_open_positions()
profit_from_sold = round(get_balance_from_closed_positions() - invested, 2)

# Output results
print(f"Number of Entries: {total_positions}")
print(f"Closed Positions: {closed_positions}")
print(f"Positions with Profit: {positions_with_profit}")
print(f"Positions with Loss: {positions_with_loss}")
print(f"Positions Still Open: {still_open}")
print(f"Leverage: {lev}")
print(f"Entry Amount per Position: $50")
print(f"Invested Total: ${invested}")
print(f"Total Balance: ${balance}")
print(f"Profit from Closed Positions: ${profit_from_sold}")
print(f"Overall Profit Percentage: {profit_from_sold / invested * 100:.2f} %")
