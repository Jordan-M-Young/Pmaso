import numpy as np

def simple_moving_avg(data,period=3):
    sma = []
    interval = np.array(range(period-1,len(data)))
    
    for i in range(len(data)):
        if i >= period-1:
            select = data[(i-period+1):(i+1)]
            avg = np.mean(select)
            sma.append(avg)
    sma = np.array(sma).reshape(len(sma),1)
    
    return sma, interval



def weighted_moving_avg(data,period=3):
    wma = []
    interval = np.array(range(period-1,len(data)))
    
    for i in range(len(data)):
        if i >= period-1:
            select = data[(i-period+1):(i+1)]
            select = select.reshape(len(select),)
            k = 0
            weights = np.array(range(1,len(select)+1))

            wavg = (select.dot(weights)) / np.sum(weights)
            wma.append(wavg)
    
    wma = np.array(wma).reshape(len(wma),1)
    
    return wma, interval

def exponential_moving_avg(data,period=3,alpha=None):
    
    
    if alpha == None:
        alpha = 2 / (len(data) + 1)
        
    ema = []
    interval = np.array(range(period-1,len(data)))
    
    for i in range(len(data)):
        if i >= period-1:
            select = data[(i-period+1):(i+1)]
            avg = []
            print(len(select))
            for j in range(len(select)):
                k = 9 - j
                
                pt = select[j]
                Yt = alpha*((1-alpha)**k)
                avg.append(pt*Yt)
                
            avg = np.array(avg).sum()
            ema.append(avg)
    
    ema = np.array(ema).reshape(len(ema),1)
    
    return ema, interval
