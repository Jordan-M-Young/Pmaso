import csv

def tick_parse(tickers):
    t = tickers.find(',')
    tt = tickers.rsplit(',',t+1)
    
    return tt


def write_port(portfolio,tickers,file_path):
    
    if '.csv' not in file_path:
        file_path = file_path + '.csv'
    

    p1 = {'Portfolio':portfolio,'Tickers':tickers}
    
    with open(file_path,'w', newline='') as csvfile:
        fieldnames = ['Portfolio','Tickers']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerow(p1)
        
def load_port(file_path):
    
    with open(file_path,newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            portfolio = row['Portfolio']
            tickers = row['Tickers']
            
    
    return portfolio,tickers
