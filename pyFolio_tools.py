import csv

def parse_tickers(tickers):
    num_commas = tickers.find(',')
    tickers = tickers.rsplit(',',num_commas+1)
    
    return tickers


def write_portfolio(portfolio,tickers,file_path):
    
    if '.csv' not in file_path:
        file_path = file_path + '.csv'
    

    port = {'Portfolio':portfolio,'Tickers':tickers}
    
    with open(file_path,'w', newline='') as csvfile:
        fieldnames = ['Portfolio','Tickers']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerow(port)
        
def load_port(file_path):
    
    with open(file_path,newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            portfolio = row['Portfolio']
            tickers = row['Tickers']
            
    
    return portfolio,tickers
