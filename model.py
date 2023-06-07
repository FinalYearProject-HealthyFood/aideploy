import requests
import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
from pulp import *
import numpy as np

def build_nutritional_values(calories):
    protein_calories = round(calories*30)/100
    carb_calories = round(calories*35)/100
    fat_calories = round(calories*35)/100
    res = {'Protein Calories':protein_calories,'Carbohydrates Calories':carb_calories,'Fat Calories':fat_calories}
    return res

def extract_gram(table):
    protein_grams = round(table['Protein Calories']/4.)
    carbs_grams = round(table['Carbohydrates Calories']/4.)
    fat_grams = round(table['Fat Calories']/9.)
    res = {'Protein Grams':protein_grams, 'Carbohydrates Grams':carbs_grams,'Fat Grams':fat_grams}
    return res

def DietModel(days_data,calories, data_ingredients):
    G = extract_gram(build_nutritional_values(calories))
    E = G['Carbohydrates Grams']
    F = G['Fat Grams']
    P = G['Protein Grams']
    day_data = days_data
    food = day_data.name.tolist()
    c  = day_data.iloc[:,4].tolist()
    x  = pulp.LpVariable.dicts( "x", indices = food, lowBound=0.0, upBound=1.5, cat='Continuous')
    food_chosen = pulp.LpVariable.dicts("Chosen",indices = food,lowBound = 0,upBound = 1,cat='Integer')
    e = day_data.iloc[:,6].tolist()
    f = day_data.iloc[:,7].tolist()
    p = day_data.iloc[:,5].tolist()
    sat_f = day_data.iloc[:,8].tolist()
    cholesterol = day_data.iloc[:,12].tolist()
    trans_f = day_data.iloc[:,9].tolist()
    fiber = day_data.iloc[:,10].tolist()
    sugar = day_data.iloc[:,11].tolist()
    sodium = day_data.iloc[:,13].tolist()
    calium = day_data.iloc[:,14].tolist()
    fe = day_data.iloc[:,15].tolist()
    zn = day_data.iloc[:,16].tolist()
    # v_a = day_data.vitamin_c.tolist()
    # v_b = day_data.vitamin_a_rae.tolist()
    # v_c = day_data.calcium.tolist()
    # v_d = day_data.irom.tolist()
    prob  = pulp.LpProblem( "Diet", LpMinimize )
    prob += pulp.lpSum( [x[food[i]]*c[i] for i in range(len(x))]  )<= (calories + 200)
    prob += pulp.lpSum( [x[food[i]]*c[i] for i in range(len(x))]  )>= (calories - 200)
    prob += pulp.lpSum( [x[food[i]]*e[i] for i in range(len(x)) ] )>= E # = 250 gram carb
    prob += pulp.lpSum( [x[food[i]]*f[i] for i in range(len(x)) ] )>= F  # = 80 gram fat
    prob += pulp.lpSum( [x[food[i]]*p[i] for i in range(len(x)) ] )>= P # = 70 gram protein
    prob += pulp.lpSum( [x[food[i]]*sat_f[i] for i in range(len(x)) ] )>=(13.0*35)/100
    prob += pulp.lpSum( [x[food[i]]*cholesterol[i] for i in range(len(x)) ] )>=10.0
    prob += pulp.lpSum( [x[food[i]]*cholesterol[i] for i in range(len(x)) ] )<=100.0
    # prob += pulp.lpSum( [x[food[i]]*trans_f[i] for i in range(len(x)) ] )>= 1.0
    prob += pulp.lpSum( [x[food[i]]*trans_f[i] for i in range(len(x)) ] )<= 2.2
    # prob += pulp.lpSum( [x[food[i]]*fiber[i] for i in range(len(x)) ] )>=(900.0*35)/100
    prob += pulp.lpSum( [x[food[i]]*sugar[i] for i in range(len(x)) ] )<= 10.0
    prob += pulp.lpSum( [x[food[i]]*sodium[i] for i in range(len(x)) ] )<=round((2300.0*35)/100)
    prob += pulp.lpSum( [x[food[i]]*calium[i] for i in range(len(x)) ] )>=round((1300.0*35)/100)
    prob += pulp.lpSum( [x[food[i]]*fe[i] for i in range(len(x)) ] )>=round((8.7*35)/100)
    prob += pulp.lpSum( [x[food[i]]*zn[i] for i in range(len(x)) ] )>=round((8*35)/100)

    for f in food:
      prob += x[f]>= food_chosen[f]*0.1
      prob += x[f]<= food_chosen[f]*1e5
    # prob += food_chosen['gạo lứt'] >=1
    # prob += x['gạo lứt'] >=1.0
    # food_choices = ['gạo trắng']
    prob += lpSum([food_chosen[p] for p in data_ingredients['name']]) >= len(data_ingredients)
    prob.solve()

    optimal_values = [round(x[food[i]].varValue,2) for i in range(len(food))]

    day_data['OptimalValue'] = optimal_values
    
    # if (prob.status != 1):
    #    return []

    return day_data[day_data["OptimalValue"] > 0]