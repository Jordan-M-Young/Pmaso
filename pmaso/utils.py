import csv

def load_csv(filename: str) -> list[list]:
    with open(filename, 'r') as csvf:
        reader = csv.reader(csvf, delimiter=",")
        return [row for row in reader]


def load_tickers(data: list[list]) -> list[str]:
    return [row[0] for row in data]