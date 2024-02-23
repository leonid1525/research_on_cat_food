import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

def percentile(n):
    
    def percentile_(x):
        
        return x.quantile(n)
    percentile_.__name__ = 'percentile_{:02.0f}'.format(n*100)
    return percentile_

def boxplot_ing_except_comp(data, column:str, y_label:str, filter_column:list, except_company:str, step=0, minx=0, quan=0, filter=1_000_000_000_000):
    
    data = data[data[column]>0]

    value_column_list = [data[(data[x]==1) & (data['company']!=except_company)][column].values.tolist() for x in filter_column]
    flist = []
    for ulist in value_column_list:
        flist = flist + ulist
    
    if quan == 0:
        quan = max(flist)
    
    zlist = [x for x in range(0, 100, 5)] + [x for x in range(100, 1000, 50)] + [x for x in range(1000, 10000, 500)] + [x for x in range(10000, 100000, 5000)] + [x for x in range(100000, 1000000, 50000)] + [x for x in range(1000000, 1000000000, 5000000)]
    
    maxx = min([x for x in zlist if x-quan>=0])
        
    if minx == 0:
        minx = max([x for x in zlist if min(flist)-x>=0])
            
    if step==0:
        step = min([x for x in [x for x in zlist if x>0] if (maxx-minx)/x>10 and (maxx-minx)/x<=31])
        
    maxx = maxx+step
    if minx-step>0:
        minx = minx-step
    else:
        minx = 0

    plt.figure(1, figsize=(16, 11))
    boxplot = []
    xticks = []
    
    for number, col in enumerate(filter_column, 1):
        for wet in ["влажный", "сухой"]:
            df = data[data[col]==1]
            if wet == "сухой":
                if df[(df['wet']==0) & (df[column]<filter) & (df['company']!=except_company)][column].dropna().shape[0]>0:
                    boxplot = boxplot + [df[(df['wet']==0) & (df[column]<filter) & (df['company']!=except_company)][column].dropna()]
                    xticks = xticks + [f"сухой\n {df[(df['wet']==0) & (df[column]<filter) & (df['company']!=except_company)][column].dropna().shape[0]} единиц\n {col}"]
                    
            elif wet == "влажный":
                if df[(df['wet']!=0) & (df[column]<filter) & (df['company']!=except_company)][column].dropna().shape[0]>0:
                    boxplot = boxplot + [df[(df['wet']!=0) & (df[column]<filter) & (df['company']!=except_company)][column].dropna()]
                    xticks = xticks + [f"влажный\n {df[(df['wet']!=0) & (df[column]<filter) & (df['company']!=except_company)][column].dropna().shape[0]} единиц\n {col}"]
                    
    plt.boxplot(boxplot, meanline=True, showmeans=True)
    plt.xticks([x for x in range(1, len(boxplot)+1, 1)], xticks)
    plt.ylabel(y_label)
    
    if step>1: 
        plt.yticks(range(minx, maxx, step))
    else:
        minx_=int(minx*10)
        maxx_=int(maxx*10)
        step_=int(step*10)
        plt.yticks([x/10 for x in range(minx_, maxx_, step_)])
    plt.show()
    
def boxplot_ing_only_comp(data, column:str, y_label:str, filter_column:list, only_company:str, step=0, minx=0, quan=0, filter=1_000_000_000_000):
    
    data = data[data[column]>0]

    value_column_list = [data[(data[x]==1) & (data['company']==only_company)][column].values.tolist() for x in filter_column]
    flist = []
    for ulist in value_column_list:
        flist = flist + ulist
    
    if quan == 0:
        quan = max(flist)
    
    zlist = [x for x in range(0, 100, 5)] + [x for x in range(100, 1000, 50)] + [x for x in range(1000, 10000, 500)] + [x for x in range(10000, 100000, 5000)] + [x for x in range(100000, 1000000, 50000)] + [x for x in range(1000000, 1000000000, 5000000)]
    
    maxx = min([x for x in zlist if x-quan>=0])
        
    if minx == 0:
        minx = max([x for x in zlist if min(flist)-x>=0])
            
    if step==0:
        step = min([x for x in [x for x in zlist if x>0] if (maxx-minx)/x>5 and (maxx-minx)/x<=31])

    maxx = maxx+step
    if minx-step>0:
        minx = minx-step
    else:
        minx = 0
        
    plt.figure(1, figsize=(16, 11))
    boxplot = []
    xticks = []
    
    for number, col in enumerate(filter_column, 1):
        for wet in ["влажный", "сухой"]:
            df = data[data[col]==1]
            if wet == "сухой":
                if df[(df['wet']==0) & (df[column]<filter) & (df['company']==only_company)][column].dropna().shape[0]>0:
                    boxplot = boxplot + [df[(df['wet']==0) & (df[column]<filter) & (df['company']==only_company)][column].dropna()]
                    xticks = xticks + [f"сухой\n {df[(df['wet']==0) & (df[column]<filter) & (df['company']==only_company)][column].dropna().shape[0]} единиц\n {col}"]
                    
            elif wet == "влажный":
                if df[(df['wet']!=0) & (df[column]<filter) & (df['company']==only_company)][column].dropna().shape[0]>0:
                    boxplot = boxplot + [df[(df['wet']!=0) & (df[column]<filter) & (df['company']==only_company)][column].dropna()]
                    xticks = xticks + [f"влажный\n {df[(df['wet']!=0) & (df[column]<filter) & (df['company']==only_company)][column].dropna().shape[0]} единиц\n {col}"]
                    
    plt.boxplot(boxplot, meanline=True, showmeans=True)
    plt.xticks([x for x in range(1, len(boxplot)+1, 1)], xticks)
    plt.ylabel(y_label)
    
    if step>1: 
        plt.yticks(range(minx, maxx, step))
    else:
        minx_=int(minx*10)
        maxx_=int(maxx*10)
        step_=int(step*10)
        plt.yticks([x/10 for x in range(minx_, maxx_, step_)])
    plt.show()
    
    
def boxplot_ing(data, column:str, y_label:str, filter_column:list, step=0, minx=0, quan=0, filter=1_000_000_000_000):
    
    data = data[data[column]>1].dropna()
        
    value_column_list = [data[data[x]==1][column].values.tolist() for x in filter_column]
    flist = []
    for ulist in value_column_list:
        flist = flist + ulist
        
    if quan == 0:
        quan = max(flist)
        
    zlist = [x for x in range(0, 100, 5)] + [x for x in range(100, 1000, 50)] + [x for x in range(1000, 10000, 500)] + [x for x in range(10000, 100000, 5000)] + [x for x in range(100000, 1000000, 50000)] + [x for x in range(1000000, 1000000000, 5000000)]
    maxx = min([x for x in zlist if x-quan>=0])
        
    if minx == 0:
        minx = max([x for x in zlist if min(flist)-x>=0])
            
    if step==0:
        step = min([x for x in [x for x in zlist if x>0] if (maxx-minx)/x>10 and (maxx-minx)/x<=31])
        
    maxx = maxx+step*2
    if minx-step>0:
        minx = minx-step
    else:
        minx = 0
        
    plt.figure(figsize=(16, 11))
    boxplot = []
    xticks = []
    
    for number, col in enumerate(filter_column, 1):
        for wet in ["влажный", "сухой"]:
            df = data[data[col]==1]

            if wet == "сухой":
                if df[(df['wet']==0) & (df[column]<filter)][column].dropna().shape[0]>0:
                    boxplot = boxplot + [df[(df['wet']==0) & (df[column]<filter)][column].dropna()]
                    xticks = xticks + [f"сухой\n {df[(df['wet']==0) & (df[column]<filter)][column].dropna().shape[0]} единиц\n {col}"]
                    
            elif wet == "влажный":
                if df[(df['wet']!=0) & (df[column]<filter)][column].dropna().shape[0]>0:
                    boxplot = boxplot + [df[(df['wet']!=0) & (df[column]<filter)][column].dropna()]
                    xticks = xticks + [f"влажный\n {df[(df['wet']!=0) & (df[column]<filter)][column].dropna().shape[0]} единиц\n {col}"]

    plt.boxplot(boxplot, meanline=True, showmeans=True)
    plt.xticks([x for x in range(1, len(boxplot)+1, 1)], xticks)
    plt.ylabel(y_label)
    
    if step>1: 
        plt.yticks(range(minx, maxx, step))
    else:
        minx_=int(minx*10)
        maxx_=int(maxx*10)
        step_=int(step*10)
        plt.yticks([x/10 for x in range(minx_, maxx_, step_)])
    plt.show()