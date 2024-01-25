from position import Position
from strategy import Strategy
import argparse
import csv
import concurrent.futures
import threading
from multiprocessing.dummy import Pool as ThreadPool



def read_csv(file_path = "data.csv"):
    with open("data.csv", 'r', newline=None, encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        stock_data = list(csv_reader)
        return stock_data

def parse_stock_data_to_float_list(stock_data):
    float_list = []
    for entry in stock_data:
        float_list.append(float(entry[1].strip('"')) + float(entry[4].strip('"')) / 2 )
    return float_list

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Process file path.")
    
    parser.add_argument("-p", "--path", type=str, help="Path to the file.")
    parser.add_argument("-s", "--strategy", action="store_true", help="Get the best strategy")
    
    # Parse the arguments
    args = parser.parse_args()

    # print_file_path(args.path)

    stock_data = read_csv(args.path)

    calculate_all_strats(parse_stock_data_to_float_list(stock_data))

counter = 0
no_strats = 0

def evaluate_strategy(strategy):
    global counter
    counter += 1
    global no_strats
    if counter % 200 == 0:
        print(f"{counter} / {no_strats} - {round(counter / no_strats * 100, 2)} %")
    strategy.evaluate_strategy()

def calculate_all_strats(stock_data, invest=50, lower_leverage=2, higher_leverage=90, lower_stop_loss=0.1, higher_stop_loss=1, higher_sell_limit=1):
    strategies = {}
    global no_strats
    no_strats = (higher_leverage - lower_leverage) * (higher_stop_loss - lower_stop_loss) * 20 * (higher_sell_limit - lower_stop_loss) * 50
    counter = 0

    for lev in range(lower_leverage, higher_leverage):
        current_stop_l = lower_stop_loss
        while current_stop_l <= higher_stop_loss:
            current_sell_l = current_stop_l
            while current_sell_l <= higher_sell_limit:
                key = (lev, current_stop_l, current_sell_l)
                strategies[key] = Strategy(stock_data, current_stop_l, lev, current_sell_l, "temp", invest)
                current_sell_l += 0.03
                counter += 1
                
            current_stop_l += 0.05

    # Make the Pool of workers
    pool = ThreadPool(12)

    # Open the URLs in their own threads
    # and return the results
    result = pool.map(evaluate_strategy, strategies.values())

    # Close the pool and wait for the work to finish
    pool.close()
    pool.join()

    # for strat in strategies.values():
    #     print(strat)

    print(find_best_strat(strategies.values()))

def find_best_strat(strategies):
    current_best = list(strategies)[0]
    for strat in strategies:
        if strat.balance >= current_best.balance:
            current_best = strat
    return current_best

def print_file_path(path):
    if path:
        print("File path:", path)
    else:
        print("No file path provided.")

if __name__ == "__main__":
    main()