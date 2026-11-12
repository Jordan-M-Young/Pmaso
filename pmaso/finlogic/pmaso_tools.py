import csv

def parse_tickers(tickers):
    
    """accepts tickers string input i.e. 'GOOG,AAPL,MSFT'
    and outputs tickers list ['GOOG','AAPL','MSFT']"""
    
    
    num_commas = tickers.find(',')
    tickers = tickers.rsplit(',',num_commas+1)
    
    return tickers


def write_portfolio(portfolio,tickers,file_path):
    
    """accepts a portfolio name, list of tickers, and a
    filepath as arguments and saves the info to a .csv file"""
    
    if '.csv' not in file_path:
        file_path = file_path + '.csv'
    

    port = {'Portfolio':portfolio,'Tickers':tickers}
    
    #writes dict to .csv file
    with open(file_path,'w', newline='') as csvfile:
        fieldnames = ['Portfolio','Tickers']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerow(port)
        
def load_portfolio(file_path):
    """Loads saved portfolio .csv files"""
    
    with open(file_path,newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            portfolio = row['Portfolio']
            tickers = row['Tickers']
            
    
    return portfolio,tickers

def get_perms(num_assets,bounds):
    
    """Generates a set of asset weight permutations based on a number
    of assets argument and boundary conditions.This function is used
    specifically for the results window worker thread
    """
    
    low_bound, up_bound = bounds
    x = range(low_bound,up_bound)
    perms = itertools.product(x,repeat=num_assets)
    
    return perms

def gen_report(tickers,opt_params,fname,selection):
    
    if '.xlsx' not in fname or '.xls' not in fname:
            fname = fname + '.xlsx'
    
    
    op = opt_params
    
    sheets = ['Selected Portfolios','All Portfolios','Asset']
    
    #Sheet One: Best Parameters
    
        
    
    cl = ['Std Deviation','Expected Returns','Sharpe Ratio','ALpha','Beta']
    for i in reversed(range(len(tickers))):
        cl.insert(5,tickers[i])
    sh1 = pd.DataFrame(selection,columns=cl)
    
    
    #Sheet Two: All Portfolios
    alphas = op['Alphas']
    betas = op['Betas']
    sharpes = op['Portfolio_Sharpe_Ratios']
    rets = op['Portfolio_Space_Returns']
    stds = op['Portfolio_Space_Stds']
    weights = op['Weights']
    
    
    cl = ['Std Deviation','Expected Returns','Sharpe Ratio','ALpha','Beta']
    for i in reversed(range(len(tickers))):
        cl.insert(5,tickers[i])
        
        
        
    ports = [[float(stds[i]),
              float(rets[i]),
              float(sharpes[i]),
              float(alphas[i]),
              float(betas[i])] for i in range(len(alphas))]
        
        #Packs all values into a list of lists
    num = len(ports[0]) 
    for j in range(len(ports)):
        for i in reversed(range(len(weights[0]))):
            ports[j].insert(num,float(weights[j][i]))
                
                
                
    sh2 = pd.DataFrame(ports,columns=cl)
    
    
    #Sheet Three: Assest Parameters
    rw = tickers
    cl = [key for key in op.keys() if 'Asset' in key]
    sh3 = [[op[cl[j]][rw[i]] for i in range(len(rw))] for j in range(len(cl))]
    sh3 = pd.DataFrame(sh3,index=cl,columns=rw).T
    
    
    
    with pd.ExcelWriter(fname) as writer:
        sh1.to_excel(writer,'Selected Portfolios')
        sh2.to_excel(writer,'All Portfolios')
        sh3.to_excel(writer,'Assets')
