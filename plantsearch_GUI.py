import tkinter as tk
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
import time

window = tk.Tk()
window.title('Plant search')
window.geometry('500x700')   
window.configure(background='white')


def calculate_plant_name_value():
    t1 =time.time()
    global df
    df = pd.read_csv('crawler_complete.csv')
   
    stemscore_list = []
    for stem in df['莖']:
        if stem_entry.get() is "":
            stemscore = 0
        else:
            stemscore = [fuzz.partial_ratio(str(stem_entry.get()),str(stem))]# partial_ratio 非完全匹配
        stemscore_list += [stemscore]
    stemscore_list = np.array(stemscore_list)
    
    leafscore_list = []
    for leaf in df['葉']:
        if leaf_entry.get() is "":
            leafscore = 0
        else:
            leafscore = [fuzz.partial_ratio(str(leaf_entry.get()),str(leaf))]# partial_ratio 非完全匹配
        leafscore_list += [leafscore]
    leafscore_list = np.array(leafscore_list)
    
    flowerscore_list = []
    for flower in df['花']:
        if flower_entry.get() is "":
            flowerscore = 0
        else:
            flowerscore = [fuzz.partial_ratio(str(flower_entry.get()),str(flower))]# partial_ratio 非完全匹配
        flowerscore_list += [flowerscore]
    flowerscore_list = np.array(flowerscore_list)
    
    fruitscore_list = []
    for fruit in df['果實']:
        if fruit_entry.get() is "":
            fruitscore = 0
        else:
            fruitscore = [fuzz.partial_ratio(str(fruit_entry.get()),str(fruit))]# partial_ratio 非完全匹配
        fruitscore_list += [fruitscore]
    fruitscore_list = np.array(fruitscore_list)
    
    whole_entry = characteristic_entry.get() +'，'+ fruit_entry.get() +'，'+ flower_entry.get() +'，'+ leaf_entry.get() +'，'+ stem_entry.get()
    
    wholescore_list = []
    for whole in df['全部特徵']:
        wholescore = [fuzz.partial_ratio(str(whole_entry),str(whole))]
        wholescore_list += [wholescore]
    wholescore_list = np.array(wholescore_list)
    
    df['stemscore'] = (stemscore_list/stemscore_list.sum())*100
    df['leafscore'] = (leafscore_list/leafscore_list.sum())*100
    df['flowerscore'] = (flowerscore_list/flowerscore_list.sum())*100
    df['fruitscore'] = (fruitscore_list/fruitscore_list.sum())*100
    df['wholescore'] = (wholescore_list/wholescore_list.sum())*100
    df = df.fillna ( 0 )
    df['重要值'] = (df['stemscore'] + df['leafscore'] + df['flowerscore'] + df['fruitscore'] + df['wholescore'])
    ranking = df['重要值']
    df['排名'] = ranking.rank(ascending=False,method='min')
    print(df['重要值'].sum())
    
    head = df.sort_values(['排名'],ascending = True).iloc[:21,[2,15,16]]
    head_form = pd.DataFrame(head)
    global name
    name = df['植物名']
    
    result_name.configure(text=head_form)
    
    name_rank_text = '{}'.format(name_rank())
    result_rank.configure(text = name_rank_text)
    
    t2 =time.time()
    speedtime = '耗時：%s' % (t2 - t1) +'  秒'
    result_time.configure(text = speedtime)
    #print('-'*20)
    #print('總共耗時：%s' % (t2 - t1))    

def name_rank():
    if name_entry.get() is "":
        return'本次並沒有進行複查排名'
    elif name_entry.get() not in list(name):
        return'查無此植物'
    else:
        search = list(name).index(name_entry.get())
        plant_name_rank = str(df.iloc[search,16])
        return'本次複查植物  '+name_entry.get()+'  排名:'+plant_name_rank


header_label = tk.Label(window, text='植物特徵電子檢索')
header_label.pack()

# 以下為 stem_frame 群組
stem_frame = tk.Frame(window)
# 向上對齊父元件
stem_frame.pack(side=tk.TOP)
stem_label = tk.Label(stem_frame, text='請輸入主幹或莖的描述：')
stem_label.pack(side=tk.LEFT)
stem_entry = tk.Entry(stem_frame)
stem_entry.pack(side=tk.LEFT)

# 以下為 leaf_frame 群組
leaf_frame = tk.Frame(window)
leaf_frame.pack(side=tk.TOP)
leaf_label = tk.Label(leaf_frame, text='請輸入葉的描述：')
leaf_label.pack(side=tk.LEFT)
leaf_entry = tk.Entry(leaf_frame)
leaf_entry.pack(side=tk.LEFT)

# 以下為 flower_frame 群組
flower_frame = tk.Frame(window)
flower_frame.pack(side=tk.TOP)
flower_label = tk.Label(flower_frame, text='請輸入花的描述：')
flower_label.pack(side=tk.LEFT)
flower_entry = tk.Entry(flower_frame)
flower_entry.pack(side=tk.LEFT)

# 以下為 fruit_frame 群組
fruit_frame = tk.Frame(window)
fruit_frame.pack(side=tk.TOP)
fruit_label = tk.Label(fruit_frame, text='請輸入果實描述：')
fruit_label.pack(side=tk.LEFT)
fruit_entry = tk.Entry(fruit_frame)
fruit_entry.pack(side=tk.LEFT)

# 以下為 characteristic_frame 群組
characteristic_frame = tk.Frame(window)
characteristic_frame.pack(side=tk.TOP)
characteristic_label = tk.Label(characteristic_frame, text='請輸入其他特徵：')
characteristic_label.pack(side=tk.LEFT)
characteristic_entry = tk.Entry(characteristic_frame)
characteristic_entry.pack(side=tk.LEFT)

name_frame = tk.Frame(window)
name_frame.pack(side=tk.TOP)
name_label = tk.Label(name_frame, text='請輸入植物名複查排名：')
name_label.pack(side=tk.LEFT)
name_entry = tk.Entry(name_frame)
name_entry.pack(side=tk.LEFT)

spilt_label = tk.Label(window, text='-'*60)
spilt_label.pack()

result_rank = tk.Label(window)
result_rank.pack()

spilt1_label = tk.Label(window, text='-'*40)
spilt1_label.pack()

result_name = tk.Label(window)
result_name.pack()

spilt2_label = tk.Label(window, text='-'*40)
spilt2_label.pack()

result_time = tk.Label(window)
result_time.pack()


calculate_ = tk.Button(window, text='確認', command = calculate_plant_name_value)
calculate_.pack()


#calculate_rank = tk.Button(window, text='確認', command = name_rank)
#calculate_rank.pack()


window.mainloop()
