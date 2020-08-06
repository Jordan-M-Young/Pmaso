import itertools
import numpy as np
import matplotlib.pyplot as plt
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
    
    count = num_portfolios

    
    for perm in perms:
        if np.sum(np.array(list(perm))/100) == 1:
            total.append(list(np.array(perm)/100))
            count = count - 1
            print(count)
        
        if count == 0:
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
        
    return frontier_rets, frontier_stds

def gen_portfolio_space(weights,exp_rets,ann_rets,vnces,
                     tickers,stds,rf_asset_return=None,plot=None):
    
    port_stds = []
    port_exp_rets = []
    
    for k in range(len(weights)):
        w2 = np.array(weights[k])**2
        term1 = vnces.dot(np.array(w2))
        term2 = []
        for i in range(len(tickers)):
            for j in range(len(tickers)):
                if j > i:
                    corr = cov(ann_rets[i],ann_rets[j])
                    term = 2*weights[k][i] * weights[k][j] * corr * stds[i] * stds[j]
                    term2.append(term)
                    
        term2 = np.sum(term2)
        
        port_var = term1 + term2
        
        port_std = math.sqrt(port_var)
        port_exp_ret = exp_rets.dot(np.array(weights[k]))
        port_stds.append(port_std)
        port_exp_rets.append(port_exp_ret)


    if plot:
        plt.scatter(np.array(port_stds)*100,np.array(port_exp_rets)*100)
        

        
        

        
    
    
    return port_exp_rets, port_stds


def gen_CAL(port_exp_ret,port_std,Rf_rate,plot=None):
    weights = [[1.0,0.0],[0.5,0.5],[0.0,1.0],[-0.5,1.5]]
    cal_rets = []
    cal_stds = []
    for weight in weights:
        cal_ret = weight[0]*Rf_rate + weight[1]*port_exp_ret*100
        cal_std = weight[1]*port_std*100
        cal_rets.append(cal_ret)
        cal_stds.append(cal_std)
    
    
    sharpe_ratio = (cal_rets[1] - cal_rets[0]) / (cal_stds[1] - cal_stds[0] ) 

    
    if plot:
        plt.plot(np.array(cal_stds),np.array(cal_rets))
        
        
    return cal_rets, cal_stds, sharpe_ratio
           


def gen_frontier_slope(frontier_ret,coefs,poly_order):
    
    if poly_order == 3:
        slope = 3*coefs[0]*(frontier_ret**2) + 2*coefs[1]*frontier_ret + coefs[2]
    elif poly_order == 4:
        slope = 4*coefs[0]*(frontier_ret**3) + 3*coefs[1]*(frontier_ret**2) 
        + 2*coefs[2]*frontier_ret + coefs[3]
        
    else:
        slope = 2*coefs[0]*(frontier_ret) + coefs[1]
    
    return slope
    
    
def gen_sharp_ratios(frontier_rets,frontier_stds,Rf_rate,p_order=3):
    coefs = np.polyfit(frontier_rets,frontier_stds,p_order)

    inverse_sharpes = []
    frontier_slopes = []
    sharpe_ratios = []
    for i in range(len(frontier_rets)):
        yprime = gen_frontier_slope(frontier_rets[i],coefs,poly_order=p_order)
        frontier_slopes.append(yprime)
        cal_rets, cal_stds, sharpe_ratio = gen_CAL(frontier_rets[i],frontier_stds[i],Rf_rate)
        inverse_sharpes.append(1/sharpe_ratio)
        sharpe_ratios.append(sharpe_ratio)
    
    return sharpe_ratios, inverse_sharpes, frontier_slopes


def slope_comparison(inverse_sharpes,frontier_slopes,tolerance):
    inds = []
    slope_ration = np.array(inverse_sharpes) / np.array(frontier_slopes)
    for i in range(len(slope_ration)):
        if slope_ration[i] > tolerance:
            inds.append(i)
            
    return inds

def find_best_weights(inds,frontier_rets,frontier_stds,sharpe_ratios,
                      port_exp_rets,port_stds,weights):
    
    best_rets = []
    best_stds = []
    best_sharpe_ratios = []
    for i in inds:
        best_rets.append(frontier_rets[i])
        best_stds.append(frontier_stds[i])
        best_sharpe_ratios.append(sharpe_ratios[i])
        
    best_weights_indices = []
    for i in range(len(best_rets)):
        
        ret_index = port_exp_rets.index(best_rets[i]/100)
        std_index = port_stds.index(best_stds[i]/100)
        
        if ret_index == std_index:
            best_weights_indices.append(ret_index)
        
        
    
    best_weights = []
    for ind in best_weights_indices:
        best_weights.append(weights[ind])

    
    return best_weights, best_rets, best_stds, best_sharpe_ratios


def get_portfolio_dic(best_rets,best_stds,best_sharpe_ratios,best_weights):
    
    
    best_portfolios = {}
    for i in range(len(best_weights)):
        port_results = {}
        port_results['Expected_Returns'] = best_rets[i]
        port_results['Standard_Deviation'] = best_stds[i]
        port_results['Sharpe_Ratio'] = best_sharpe_ratios[i]
        port_results['Weights'] = best_weights[i]
        
        best_portfolios[str(i)] = port_results
    
    return best_portfolios


def get_best_portfolios(weights,port_exp_rets,port_stds,frontier_rets,
                        frontier_stds,tolerance,Rf_rate):
    
    
    
    sharpe_ratios, s_ratios, frontier_slopes = gen_sharp_ratios(frontier_rets, 
                                                                frontier_stds, 
                                                                Rf_rate,
                                                                p_order=3)
    


    inds = slope_comparison(s_ratios, frontier_slopes,tolerance)
            
    
    
    best_params = find_best_weights(inds, 
                                    frontier_rets, 
                                    frontier_stds, 
                                    sharpe_ratios, 
                                    port_exp_rets, 
                                    port_stds, 
                                    weights)
    
    
    best_weights, best_rets, best_stds, best_sharpe_ratios = best_params
    
    
    best_portfolios = get_portfolio_dic(best_rets, 
                                        best_stds, 
                                        best_sharpe_ratios, 
                                        best_weights)
    
    return best_portfolios


def optimize_portfolio_weights(params,tickers,weights,Rf_rate,tolerance=0.3):
    
    optimization_params = {'Asset_Expected_Returns':{},
                           'Asset_Std':{},
                           'Asset_Variance':{}}
    
    
    
    
    ann_rets = []
    exp_rets = []
    stds = []
    vnces = []
    
    for ticker in tickers:
        
        ann_ret = params['Annualized_Returns'][ticker]
        # print(ann_ret)
        ann_rets.append(ann_ret)
        exp_ret = np.mean(ann_ret)
        ann_std = np.std(ann_ret)
        var = ann_std**2
        exp_rets.append(exp_ret)
        stds.append(ann_std)
        vnces.append(var)
        optimization_params['Asset_Expected_Returns'][ticker] = exp_ret*100
        optimization_params['Asset_Std'][ticker] = ann_std*100
        optimization_params['Asset_Variance'][ticker] = var*100
    
    
    exp_rets = np.array(exp_rets)
    stds = np.array(stds)
    vnces = np.array(vnces)
    
    
    
    
    
    port_exp_rets, port_stds = gen_portfolio_space(weights,
                                                   exp_rets,
                                                   ann_rets,
                                                   vnces,
                                                   tickers,
                                                   stds,
                                                   Rf_rate
                                                   )
    
    
    
    
    frontier_rets, frontier_stds = gen_eff_frontier(port_exp_rets,port_stds,200)
    frontier_rets = np.array(frontier_rets)*100
    frontier_stds = np.array(frontier_stds)*100
    
    
    
    
    best_portfolios = get_best_portfolios(weights, 
                                          port_exp_rets, 
                                          port_stds, 
                                          frontier_rets, 
                                          frontier_stds,
                                          tolerance,
                                          Rf_rate)
    
    
    

    optimization_params['Best_Portfolios'] = best_portfolios
    optimization_params['Frontier_Returns'] = frontier_rets
    optimization_params['Frontier_Stds'] = frontier_stds
    optimization_params['Portfolio_Space_Returns'] = port_exp_rets
    optimization_params['Portfolio_Space_Stds'] = port_stds
    optimization_params['Weights'] = weights
    
    
    
    return optimization_params
    
    
