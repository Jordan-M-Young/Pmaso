import itertools
import numpy as np
import math
import random as rand

def cov(ret1,ret2):
    mean1 = np.mean(ret1)
    mean2 = np.mean(ret2)
    
    if len(ret1) > len(ret2):
        min_size = len(ret2)
        r1 = len(ret1) - min_size
        r2 = 0
        
    elif len(ret1) < len(ret2):
        min_size = len(ret1)
        r1 = 0
        r2 = len(ret2) - min_size
        
    else:
        min_size = len(ret1)
        r1 = 0
        r2 = 0
        
    els = []
    
    for i in range(min_size):
        els.append((ret1[i+r1] - mean1) * (ret2[i+r2] - mean2))
    
    el_sum = np.sum(np.array(els))
    Cov = el_sum / min_size
    return Cov

def gen_weights(num_assets,num_portfolios,bounds):
    
    low_bound, up_bound = bounds
    total = []
    
    
    
    x = range(low_bound,up_bound)
    perms = itertools.product(x,repeat=num_assets)
    
    counter = num_portfolios
    
    
    
    try:
        
        global count
        step = 100 / counter
        
        for perm in perms:
            if np.sum(np.array(list(perm))/100) == 1:
                total.append(list(np.array(perm)/100))
                counter = counter - 1
                count = count + step
                print(count)
            if counter == 0:
                break
            
    except NameError:
        
        for perm in perms:
            if np.sum(np.array(list(perm))/100) == 1:
                total.append(list(np.array(perm)/100))
                counter = counter - 1
            if counter == 0:
                break
        
    
    
    for i in range(len(total)):
        if i % 2:
            total[i].reverse()
        
        elif i % 3 or i % 7:
            r1 = rand.randint(0,(int(num_assets/2))-1)
            r2 = rand.randint(int(num_assets/2),num_assets-1)
            e1 = total[i][r1]
            e2 = total[i][r2]
            
            total[i][r1] = e2
            total[i][r2] = e1

        elif i % 5:
            total[i].reverse()
            
    return total

def gen_eff_frontier(port_exp_rets,port_stds,num_points):
    
    p_exp_rets = port_exp_rets.copy()
    p_stds = port_stds.copy()
    
    

    frontier_stds = []
    frontier_rets = []
    
    pmindex = p_stds.index(np.min(p_stds))
    min_ret, min_std = (p_exp_rets[pmindex],p_stds[pmindex])
    
    frontier_stds.append(min_std)
    frontier_rets.append(min_ret)
    
    pmaxdex = p_exp_rets.index(np.max(p_exp_rets))
    max_ret, max_std = (p_exp_rets[pmaxdex],p_stds[pmaxdex])
    
    frontier_stds.append(max_std)
    frontier_rets.append(max_ret)
    
    
    for i in reversed(range(len(p_exp_rets))):
        if p_exp_rets[i] < min_ret:
            del(p_exp_rets[i])
            del(p_stds[i])
    
    
    
    std_range = max_std - min_std
    step_size = std_range / (num_points-1)
    
    new_max_std = max_std
    for j in range(num_points-2):
        
        new_max_std = new_max_std - step_size
        for i in reversed(range(len(p_exp_rets))):
            if p_stds[i] > new_max_std:
                del(p_exp_rets[i])
                del(p_stds[i])
                
              
        pmaxdex = p_exp_rets.index(np.max(p_exp_rets))
        max_ret, max_std = (p_exp_rets[pmaxdex],p_stds[pmaxdex])
        
        frontier_stds.append(max_std)
        frontier_rets.append(max_ret)
        
    frontier_rets.sort()
    frontier_stds.sort()
        
    return frontier_rets, frontier_stds

def gen_portfolio_space(weights,exp_rets,ann_rets,vnces,
                     tickers,stds):
    
    port_stds = []
    port_exp_rets = []
    
    for k in range(len(weights)):
        w2 = np.array(weights[k])**2
        term1 = vnces.dot(np.array(w2))
        term2 = []
        for i in range(len(tickers)):
            for j in range(len(tickers)):
                if j > i:
                    covar = cov(ann_rets[i],ann_rets[j])
                    term = 2*weights[k][i] * weights[k][j] * covar * stds[i] * stds[j]
                    term2.append(term)
                    
        term2 = np.sum(term2)
        
        port_var = term1 + term2
        
        port_std = math.sqrt(port_var)
        port_exp_ret = exp_rets.dot(np.array(weights[k]))
        port_stds.append(round(port_std,10)*100)
        port_exp_rets.append(round(port_exp_ret,10)*100)        

        
        

        
    
    
    return port_exp_rets, port_stds


def gen_CAL(port_exp_ret,port_std,rf_rate):
    weights = [[1.0,0.0],[0.5,0.5],[0.0,1.0],[-0.5,1.5]]
    cal_rets = []
    cal_stds = []
    for weight in weights:
        cal_ret = weight[0]*rf_rate + weight[1]*port_exp_ret
        cal_std = weight[1]*port_std
        cal_rets.append(cal_ret)
        cal_stds.append(cal_std)
   
    sharpe_ratio = (cal_rets[2] - cal_rets[0]) / (cal_stds[2] - cal_stds[0] ) 
    
        
        
    return cal_rets, cal_stds, sharpe_ratio
           
    
    
def gen_sharp_ratios(frontier_rets,frontier_stds,rf_rate):
    

    inverse_sharpes = []
    frontier_slopes = []
    sharpe_ratios = []
    for i in range(len(frontier_rets)):
        cal_rets, cal_stds, sharpe_ratio = gen_CAL(frontier_rets[i],frontier_stds[i],rf_rate)
        sharpe_ratios.append(sharpe_ratio)
    
    
    return sharpe_ratios, inverse_sharpes, frontier_slopes


def gen_betas(asset_betas,weights):
    asset_betas = np.array(asset_betas)
    port_betas = []
    for i in range(len(weights)):
        weight = np.array(weights[i])
        beta = np.dot(asset_betas,weight)
        port_betas.append(beta)


    return port_betas


def gen_alphas(port_exp_rets,port_betas,Rf_rate,mkt_ret):
    
    alphas = []
    for i in range(len(port_exp_rets)):
        
        
        alpha = port_exp_rets[i] - (Rf_rate + (port_betas[i]*(mkt_ret-Rf_rate)))
        alphas.append(alpha)
    
    return alphas

def optimize_portfolio_weights(params,tickers,weights,rf_rate,tolerance=0.2):
    
    optimization_params = {'Asset_Expected_Returns':{},
                           'Asset_Std':{},
                           'Asset_Variance':{},
                           'Asset_Covariance':{},
                           'Asset_Beta':{}}
    
    
    
    ann_rets = []
    exp_rets = []
    stds = []
    vnces = []
    mkt_ret = np.mean(params['Annualized_Market_Returns'])*100
    ann_mkt_rets = params['Annualized_Market_Returns']
    mkt_var = params['Annualized_Market_Returns_std']**2
    asset_betas = []
    for ticker in tickers:
        
        ann_ret = params['Annualized_Returns'][ticker]
        
        ann_rets.append(ann_ret)
        exp_ret = np.mean(ann_ret)
        ann_std = np.std(ann_ret)
        var = ann_std**2
        exp_rets.append(exp_ret)
        stds.append(ann_std)
        vnces.append(var)
        covariance = cov(ann_ret,ann_mkt_rets)
        Beta = covariance / mkt_var
        asset_betas.append(Beta)
        
        optimization_params['Asset_Expected_Returns'][ticker] = exp_ret*100
        optimization_params['Asset_Std'][ticker] = ann_std*100
        optimization_params['Asset_Variance'][ticker] = var
        optimization_params['Asset_Covariance'][ticker] = covariance
        optimization_params['Asset_Beta'][ticker] = Beta
        
        
        
    exp_rets = np.array(exp_rets)
    stds = np.array(stds)
    vnces = np.array(vnces)
    
    
    
    
    port_exp_rets, port_stds = gen_portfolio_space(weights,
                                                   exp_rets,
                                                   ann_rets,
                                                   vnces,
                                                   tickers,
                                                   stds
                                                  )
                                                   
    
    
    
 
    num_points = 50
    
    frontier_rets, frontier_stds = gen_eff_frontier(port_exp_rets,port_stds,num_points)
    
    
    frontier_rets = np.array(frontier_rets)
    frontier_stds = np.array(frontier_stds)
    
    
    
    
    sharpe_ratios, s, slopes = gen_sharp_ratios(port_exp_rets,
                                                        port_stds,
                                                        rf_rate,
                                                        )
   
    port_betas = gen_betas(asset_betas,weights)
    port_alphas = gen_alphas(port_exp_rets,port_betas,rf_rate,mkt_ret)
    
    
    
    optimization_params['Frontier_Returns'] = frontier_rets
    optimization_params['Frontier_Stds'] = frontier_stds
    optimization_params['Frontier_Vals'] = np.array([list(frontier_stds),list(frontier_rets)])
    optimization_params['Portfolio_Space_Returns'] = port_exp_rets
    optimization_params['Portfolio_Space_Stds'] = port_stds
    optimization_params['Portfolio_Sharpe_Ratios'] = sharpe_ratios
    optimization_params['Portfolio_Space'] = np.array([port_stds,port_exp_rets])
    optimization_params['Weights'] = weights
    optimization_params['Betas'] = port_betas
    optimization_params['Alphas'] = port_alphas
    
    
    return optimization_params


