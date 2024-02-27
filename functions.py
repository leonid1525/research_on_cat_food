import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

# Функция для получения квантиля от набора данных
def percentile(n):
    
    def percentile_(x):
        
        return x.quantile(n)
    percentile_.__name__ = 'percentile_{:02.0f}'.format(n*100)
    return percentile_

# Функция для визуализации количественных данных, с исключением компании на выбор
def boxplot_ing_except_comp(data, column:str, y_label:str, filter_column:list, except_company:str, step=0, minx=0, quan=0, filter=1_000_000_000_000):
    
    # data - датафрейм
    # column - визуализируемые количественные данные
    # y_label - подпись оси y, должна по смыслу совпадать с column
    # filter_column - набор качественных данных, разбивающих column на группы, которые будут визуализироваться
    # except_company - исключаемая компания из датафрейма
    # step - шаг оси y, может сам рассчитываться
    # minx - минимум на графике, может сам рассчитываться
    # quan - максимум данных column который, нужно визуализировать
    # filter - фильтр для column, нужен чтобы убирать большие выбросы в данных

    # отфильтруем данные, так чтобы они были больше 0
    data = data[data[column]>0]

    # соберем все данные из датафрейма в список, далее из списка списков превратим его в простой список
    value_column_list = [data[(data[x]==1) & (data['company']!=except_company)][column].values.tolist() for x in filter_column]
    flist = []
    for ulist in value_column_list:
        flist = flist + ulist
    
    # если quan не задан, то определим его как максимум из всех наших данных собранных в список выше
    if quan == 0:
        quan = max(flist)
    
    # создадим универсальный список для перебора удобных значений
    zlist = [x for x in range(0, 100, 5)] + [x for x in range(100, 1000, 50)] + [x for x in range(1000, 10000, 500)] + [x for x in range(10000, 100000, 5000)] + [x for x in range(100000, 1000000, 50000)] + [x for x in range(1000000, 1000000000, 5000000)]
    
    # подберем удобный максимум значений оси y из универсального списка выше 
    maxx = min([x for x in zlist if x-quan>=0])
        
    # если minx не задан, подберем удобный минимум значений оси y из универсального списка выше 
    if minx == 0:
        minx = max([x for x in zlist if min(flist)-x>=0])
            
    # если step не задан, по выбранным максимуму и минимуму определим оптимальный шаг значений оси y
    if step==0:
        step = min([x for x in [x for x in zlist if x>0] if (maxx-minx)/x>10 and (maxx-minx)/x<=31])
    
    # скорректируем максимум и минимум через шаг
    maxx = maxx+step
    if minx-step>0:
        minx = minx-step
    else:
        minx = 0

    plt.figure(1, figsize=(16, 11))
    boxplot = []
    xticks = []
    
    # пройдем циклом внутри цикла по всем качественным столбцам деля корма по типу
    for number, col in enumerate(filter_column, 1):
        for wet in ["влажный", "сухой"]:

            # отфильтруем данные по столбцу
            df = data[data[col]==1]

            # если корм сухой и если данные есть после применения фильтров, то добавим в списки отфильтрованные данные и подписи к данным
            if wet == "сухой":
                if df[(df['wet']==0) & (df[column]<filter) & (df['company']!=except_company)][column].dropna().shape[0]>0:
                    boxplot = boxplot + [df[(df['wet']==0) & (df[column]<filter) & (df['company']!=except_company)][column].dropna()]
                    xticks = xticks + [f"сухой\n {df[(df['wet']==0) & (df[column]<filter) & (df['company']!=except_company)][column].dropna().shape[0]} единиц\n {col}"]
            
            # если корм влажный и если данные есть после применения фильтров, то добавим в списки отфильтрованные данные и подписи к данным
            elif wet == "влажный":
                if df[(df['wet']!=0) & (df[column]<filter) & (df['company']!=except_company)][column].dropna().shape[0]>0:
                    boxplot = boxplot + [df[(df['wet']!=0) & (df[column]<filter) & (df['company']!=except_company)][column].dropna()]
                    xticks = xticks + [f"влажный\n {df[(df['wet']!=0) & (df[column]<filter) & (df['company']!=except_company)][column].dropna().shape[0]} единиц\n {col}"]

    # передадим в функции списки с наборами данных, подписи к ним и подпись к оси y
    plt.boxplot(boxplot, meanline=True, showmeans=True)
    plt.xticks([x for x in range(1, len(boxplot)+1, 1)], xticks)
    plt.ylabel(y_label)
    
    # если шаг больше 1 (если шаг неопределен, то меньше единицы он не будет), то просто передаем данные, однако если
    # шаг определен заранее и менее 1, то минимум, максимум и шаг умножаются на 10, чтобы range работал, после все элементы
    # последовательности делятся на 10
    if step>1: 
        plt.yticks(range(minx, maxx, step))
    else:
        minx_=int(minx*10)
        maxx_=int(maxx*10)
        step_=int(step*10)
        plt.yticks([x/10 for x in range(minx_, maxx_, step_)])

    plt.show()

# Функция для визуализации количественных данных, с выбором компании
def boxplot_ing_only_comp(data, column:str, y_label:str, filter_column:list, only_company:str, step=0, minx=0, quan=0, filter=1_000_000_000_000):

    # data - датафрейм
    # column - визуализируемые количественные данные
    # y_label - подпись оси y, должна по смыслу совпадать с column
    # filter_column - набор качественных данных, разбивающих column на группы, которые будут визуализироваться
    # only_company - компания, данные которой будут визуализированы
    # step - шаг оси y, может сам рассчитываться
    # minx - минимум на графике, может сам рассчитываться
    # quan - максимум данных column который, нужно визуализировать
    # filter - фильтр для column, нужен чтобы убирать большие выбросы в данных
    
    # отфильтруем данные, так чтобы они были больше 0
    data = data[data[column]>0]

    # соберем все данные из датафрейма в список, далее из списка списков превратим его в простой список
    value_column_list = [data[(data[x]==1) & (data['company']==only_company)][column].values.tolist() for x in filter_column]
    flist = []
    for ulist in value_column_list:
        flist = flist + ulist
    
    # если quan не задан, то определим его как максимум из всех наших данных собранных в список выше
    if quan == 0:
        quan = max(flist)
    
    # создадим универсальный список для перебора удобных значений
    zlist = [x for x in range(0, 100, 5)] + [x for x in range(100, 1000, 50)] + [x for x in range(1000, 10000, 500)] + [x for x in range(10000, 100000, 5000)] + [x for x in range(100000, 1000000, 50000)] + [x for x in range(1000000, 1000000000, 5000000)]
    
    # подберем удобный максимум значений оси y из универсального списка выше 
    maxx = min([x for x in zlist if x-quan>=0])
    
    # если minx не задан, подберем удобный минимум значений оси y из универсального списка выше 
    if minx == 0:
        minx = max([x for x in zlist if min(flist)-x>=0])

    # если step не задан, по выбранным максимуму и минимуму определим оптимальный шаг значений оси y
    if step==0:
        step = min([x for x in [x for x in zlist if x>0] if (maxx-minx)/x>5 and (maxx-minx)/x<=31])

    # скорректируем максимум и минимум через шаг
    maxx = maxx+step
    if minx-step>0:
        minx = minx-step
    else:
        minx = 0
    
    plt.figure(1, figsize=(16, 11))
    boxplot = []
    xticks = []
    
    # пройдем циклом внутри цикла по всем качественным столбцам деля корма по типу
    for number, col in enumerate(filter_column, 1):
        for wet in ["влажный", "сухой"]:

            # отфильтруем данные по столбцу
            df = data[data[col]==1]

            # если корм сухой и если данные есть после применения фильтров, то добавим в списки отфильтрованные данные и подписи к данным
            if wet == "сухой":
                if df[(df['wet']==0) & (df[column]<filter) & (df['company']==only_company)][column].dropna().shape[0]>0:
                    boxplot = boxplot + [df[(df['wet']==0) & (df[column]<filter) & (df['company']==only_company)][column].dropna()]
                    xticks = xticks + [f"сухой\n {df[(df['wet']==0) & (df[column]<filter) & (df['company']==only_company)][column].dropna().shape[0]} единиц\n {col}"]

            # если корм влажный и если данные есть после применения фильтров, то добавим в списки отфильтрованные данные и подписи к данным     
            elif wet == "влажный":
                if df[(df['wet']!=0) & (df[column]<filter) & (df['company']==only_company)][column].dropna().shape[0]>0:
                    boxplot = boxplot + [df[(df['wet']!=0) & (df[column]<filter) & (df['company']==only_company)][column].dropna()]
                    xticks = xticks + [f"влажный\n {df[(df['wet']!=0) & (df[column]<filter) & (df['company']==only_company)][column].dropna().shape[0]} единиц\n {col}"]

    # передадим в функции списки с наборами данных, подписи к ним и подпись к оси y
    plt.boxplot(boxplot, meanline=True, showmeans=True)
    plt.xticks([x for x in range(1, len(boxplot)+1, 1)], xticks)
    plt.ylabel(y_label)
    
    # если шаг больше 1 (если шаг неопределен, то меньше единицы он не будет), то просто передаем данные, однако если
    # шаг определен заранее и менее 1, то минимум, максимум и шаг умножаются на 10, чтобы range работал, после все элементы
    # последовательности делятся на 10
    if step>1: 
        plt.yticks(range(minx, maxx, step))
    else:
        minx_=int(minx*10)
        maxx_=int(maxx*10)
        step_=int(step*10)
        plt.yticks([x/10 for x in range(minx_, maxx_, step_)])
    
    plt.show()
    
# Функция для визуализации количественных данных    
def boxplot_ing(data, column:str, y_label:str, filter_column:list, step=0, minx=0, quan=0, filter=1_000_000_000_000):
    
    # data - датафрейм
    # column - визуализируемые количественные данные
    # y_label - подпись оси y, должна по смыслу совпадать с column
    # filter_column - набор качественных данных, разбивающих column на группы, которые будут визуализироваться
    # step - шаг оси y, может сам рассчитываться
    # minx - минимум на графике, может сам рассчитываться
    # quan - максимум данных column который, нужно визуализировать
    # filter - фильтр для column, нужен чтобы убирать большие выбросы в данных

    # отфильтруем данные, так чтобы они были больше 0
    data = data[data[column]>1].dropna()
    
    # соберем все данные из датафрейма в список, далее из списка списков превратим его в простой список
    value_column_list = [data[data[x]==1][column].values.tolist() for x in filter_column]
    flist = []
    for ulist in value_column_list:
        flist = flist + ulist
    
    # если quan не задан, то определим его как максимум из всех наших данных собранных в список выше
    if quan == 0:
        quan = max(flist)
    
    # создадим универсальный список для перебора удобных значений
    zlist = [x for x in range(0, 100, 5)] + [x for x in range(100, 1000, 50)] + [x for x in range(1000, 10000, 500)] + [x for x in range(10000, 100000, 5000)] + [x for x in range(100000, 1000000, 50000)] + [x for x in range(1000000, 1000000000, 5000000)]

    # подберем удобный максимум значений оси y из универсального списка выше 
    maxx = min([x for x in zlist if x-quan>=0])

    # если minx не задан, подберем удобный минимум значений оси y из универсального списка выше 
    if minx == 0:
        minx = max([x for x in zlist if min(flist)-x>=0])

    # если step не задан, по выбранным максимуму и минимуму определим оптимальный шаг значений оси y
    if step==0:
        step = min([x for x in [x for x in zlist if x>0] if (maxx-minx)/x>10 and (maxx-minx)/x<=31])

    # скорректируем максимум и минимум через шаг
    maxx = maxx+step*2
    if minx-step>0:
        minx = minx-step
    else:
        minx = 0
        
    plt.figure(figsize=(16, 11))
    boxplot = []
    xticks = []

    # пройдем циклом внутри цикла по всем качественным столбцам деля корма по типу
    for number, col in enumerate(filter_column, 1):
        for wet in ["влажный", "сухой"]:

            # отфильтруем данные по столбцу
            df = data[data[col]==1]

            # если корм сухой и если данные есть после применения фильтров, то добавим в списки отфильтрованные данные и подписи к данным
            if wet == "сухой":
                if df[(df['wet']==0) & (df[column]<filter)][column].dropna().shape[0]>0:
                    boxplot = boxplot + [df[(df['wet']==0) & (df[column]<filter)][column].dropna()]
                    xticks = xticks + [f"сухой\n {df[(df['wet']==0) & (df[column]<filter)][column].dropna().shape[0]} единиц\n {col}"]

            # если корм влажный и если данные есть после применения фильтров, то добавим в списки отфильтрованные данные и подписи к данным
            elif wet == "влажный":
                if df[(df['wet']!=0) & (df[column]<filter)][column].dropna().shape[0]>0:
                    boxplot = boxplot + [df[(df['wet']!=0) & (df[column]<filter)][column].dropna()]
                    xticks = xticks + [f"влажный\n {df[(df['wet']!=0) & (df[column]<filter)][column].dropna().shape[0]} единиц\n {col}"]

    # передадим в функции списки с наборами данных, подписи к ним и подпись к оси y
    plt.boxplot(boxplot, meanline=True, showmeans=True)
    plt.xticks([x for x in range(1, len(boxplot)+1, 1)], xticks)
    plt.ylabel(y_label)

    # если шаг больше 1 (если шаг неопределен, то меньше единицы он не будет), то просто передаем данные, однако если
    # шаг определен заранее и менее 1, то минимум, максимум и шаг умножаются на 10, чтобы range работал, после все элементы
    # последовательности делятся на 10    
    if step>1: 
        plt.yticks(range(minx, maxx, step))
    else:
        minx_=int(minx*10)
        maxx_=int(maxx*10)
        step_=int(step*10)
        plt.yticks([x/10 for x in range(minx_, maxx_, step_)])

    plt.show()