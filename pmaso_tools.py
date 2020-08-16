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

def gen_report(tickers,opt_params,fname):
    
    """Called by a ResultsWindow class method,
    this function generates an excel file report
    of the portfolios generated during the optimization.
    Information on the 'Best Portfolios' the efficient frontier
    and individual assets is included
    """
    
    if '.xlsx' not in fname or '.xls' not in fname:
            fname = fname + '.xlsx'
    
    
    op = opt_params
    
    sheets = ['Best Portfolios','Efficient Frontier','Asset']
    
    #Sheet One: Best Parameters
    s1_v = op['Best_Portfolios']
    sh1 = [[s1_v[k][key] for key in s1_v[k].keys()] for k in s1_v.keys()]

    for i in range(len(sh1)):
        for j in reversed(range(len(sh1[i][3]))):
            sh1[i].insert(4,sh1[i][3][j])
        del(sh1[i][3])
        
    
    cl = [key for key in s1_v['0'].keys() if key != 'Weights']
    for i in reversed(range(len(tickers))):
        cl.insert(3,tickers[i])
    sh1 = pd.DataFrame(sh1,columns=cl)
    
    
    #Sheet Two: Frontier Parameters
    s2_v = op['Frontier Portfolios']
    sh2 = [[s2_v[k][key] for key in s2_v[k].keys()] for k in s2_v.keys()]

    for i in range(len(sh2)):
        for j in reversed(range(len(sh2[i][3]))):
            sh2[i].insert(4,sh2[i][3][j])
        del(sh2[i][3])
        
    
    cl = [key for key in s2_v['0'].keys() if key != 'Weights']
    for i in reversed(range(len(tickers))):
        cl.insert(3,tickers[i])
    sh2 = pd.DataFrame(sh2,columns=cl)
    
    
    #Sheet Three: Assest Parameters
    rw = tickers
    cl = [key for key in op.keys() if 'Asset' in key]
    sh3 = [[op[cl[j]][rw[i]] for i in range(len(rw))] for j in range(len(cl))]
    sh3 = pd.DataFrame(sh3,index=cl,columns=rw).T
    
    
    #Writes pandas dataframe to .xlsx file
    with pd.ExcelWriter(fname) as writer:
        sh1.to_excel(writer,'Best_Portfolios')
        sh2.to_excel(writer,'Frontier_Portfolios')
        sh3.to_excel(writer,'Assets')
