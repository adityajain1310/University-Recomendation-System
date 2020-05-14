#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 19:53:07 2020

@author: aditya
"""
# Used to store the dictionary lacally
import pickle
import numpy as np
# Importing necessary libraries
import pandas as pd
# for making default dict
from collections import defaultdict
# Used to load html page by requesting using url
import requests
# used to scrap data from the html page
from bs4 import BeautifulSoup
# Used to handle categorical varible
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
# Used to split the dataset into training data and test data
from sklearn.model_selection import train_test_split
# Used to normalize the dataset to handle outliers and scaling problem
from sklearn.preprocessing import StandardScaler

# converting the categorical data into numerical data...removing unnecessary spaces and symbols
def categorical_var(data,feature):
    feature_list = data[feature].astype(str).tolist()
    student_id_for_feature = defaultdict(list)
    for i in range(len(feature_list)):
        feature_list[i] = str(feature_list[i])
        feature_list[i] = feature_list[i].strip()
        feature_list[i] = feature_list[i].replace('-', '')
        feature_list[i] = feature_list[i].replace('.', '')
        feature_list[i] = feature_list[i].partition('/')[0]
        feature_list[i] = feature_list[i].partition('(')[0]
        feature_list[i] = feature_list[i].replace(' ','')
        feature_list[i] = feature_list[i].lower()
    
    max_len = 0
    max_feature_name = ""
    unique_feature = []
    for i in range(len(feature_list)):
        for j in range(i+1,len(feature_list)):
            if (feature_list[i] in feature_list[j]):
                if (max_len < len(feature_list[j])):
                    max_len = len(feature_list[j])
                    max_feature_name = feature_list[j]
        if max_len == 0:
            unique_feature.append(feature_list[i])
            student_id_for_feature[feature_list[i]].append(i)
        elif max_len > 0:
            student_id_for_feature[max_feature_name].append(i)
        max_len = 0

    for i in range(len(unique_feature)):
        student_list_for_cur_feature = [0] * len(data)
        for j in student_id_for_feature[unique_feature[i]]:
            student_list_for_cur_feature[j] = 1
        data[unique_feature[i]] = student_list_for_cur_feature
        pass

    return data

# Scraping the conversion table if GRE from Old format to New Fromat
def scraping_table(): 
    # requesting at the following link for scraping the conversion table
    page = requests.get('https://gre.graduateshotline.com/gre_score_scale.html')
    # Scraping the data using Beautiful Soup
    soup = BeautifulSoup(page.content, 'html.parser')
    # finding all tds in the page content
    allTDs = soup.table.find_all('td')
    oldformat = []
    verbal = []
    quant = []
    # Storing all the content in a list
    for i in range(len(allTDs)):
        rem = i%3
        if(rem == 0):
            oldformat.append((allTDs[i].string or "").strip())
        if(rem == 1):
            verbal.append((allTDs[i].string or "").strip())
        if(rem == 2):
            quant.append((allTDs[i].string or "").strip())
        
    for i in range(len((oldformat))):
        if(i==0):
            continue
        else:
            row = []
            row.append(oldformat[i])
            row.append(verbal[i].strip().split(" ")[0])
            row.append(quant[i].strip().split(" ")[0])
            scr_conver.append(row)

# Score Conversion dict stored
with open('../univdata/scoreconversion.p', 'wb') as fp:
    pickle.dump(scr_conver, fp, protocol=pickle.HIGHEST_PROTOCOL)

# Use to Normalize the cgpa according to there cgpa Scale
def normalizecgpa(cgpa, ttlcgpa):
    cgpa = cgpa.tolist()
    ttlcgpa = ttlcgpa.tolist()
    for i in range(len(cgpa)):
        if(ttlcgpa[i] != 0):
            cgpa[i] = cgpa[i] / ttlcgpa[i]
        else:
            cgpa[i] = 0
    return cgpa
    
# converting old GRE quantative score to New format
def convert_quant_score(quant_score):
    quant_list = []
    quant_score = quant_score.tolist()
    # if score is less than 170 than it is in new format
    for old_quant in quant_score:
        if old_quant <= 170:
            quant_list.append(int(old_quant))
            continue
        
        flag=0
        new_quant=0
        for l in range(len(scr_conver)):
            score = scr_conver[l]
            oldformat = int(score[0]) 
            verbal = int(score[1])
            quant = int(score[2])
            if oldformat==old_quant:
                new_quant=quant
                flag+=1
            if flag==2:
                break
        quant_list.append(new_quant)
    return quant_list    
    

# converting old GRE verbal score to New format
def convert_verbal_score(verbal_score):
    verbal_list = []
    verbal_score = verbal_score.tolist()
    for old_verbal in verbal_score:
        if old_verbal <= 170:
            verbal_list.append(int(old_verbal))
            continue
        flag=0
        new_verbal=0
        for l in range(len(scr_conver)):
            score = scr_conver[l]
            oldformat = int(score[0]) 
            verbal = int(score[1])
            quant = int(score[2])
            if oldformat==old_verbal:
                new_verbal=verbal
                flag+=1
            if flag==2:
                break
        verbal_list.append(new_verbal)
    return verbal_list


# Reading University data for preprocessing
dataset = pd.read_csv('../univdata/finaldata.csv')

# droping unnecessary columns and the columns which have most of missing values
dataset = dataset.drop('specialization', 1)
dataset = dataset.drop('toeflScore', 1)
dataset = dataset.drop('toeflEssay', 1)
dataset = dataset.drop('program', 1)
dataset = dataset.drop('department', 1)
dataset = dataset.drop('userProfileLink', 1)
dataset = dataset.drop('journalPubs', 1)
dataset = dataset.drop('topperCgpa', 1)
dataset = dataset.drop('termAndYear', 1)
dataset = dataset.drop('confPubs', 1)
dataset = dataset.drop('gmatA', 1)
dataset = dataset.drop('gmatQ', 1)
dataset = dataset.drop('gmatV', 1)

# removing rejected students
dataset = dataset[dataset['admit'] > 0]

# droping admit columns after removing the rejected students
dataset = dataset.drop('admit', 1)

# droping missing values
dataset = dataset.dropna()

# screaping the conversion table from graduateshortline
scr_conver = []
scraping_table()

# converting GRE score from old format to new for both quantative and  verbal
dataset['greQ'] = convert_quant_score(dataset['greQ'])
dataset['greV'] = convert_verbal_score(dataset['greV'])

# normalizing the cgpa by using cgpa scale
dataset['cgpa'] = normalizecgpa(dataset['cgpa'], dataset['cgpaScale'])
dataset = dataset.drop('cgpaScale', 1)

# categorical data
dataset = categorical_var(dataset,'major')
dataset = dataset.drop('major' ,1)
dataset = categorical_var(dataset,'ugCollege')
dataset = dataset.drop('ugCollege' ,1)

dataset.to_csv("../univdata/processeddata.csv")

# dependent variable or output values
y = dataset.iloc[:, 8].values

dataset = dataset.drop('univName', 1) 

# Independent Variable
x = dataset.iloc[:,1:].values

# Encoding categorical data
labelencoder_y=LabelEncoder()
y=labelencoder_y.fit_transform(y)

# Splitting the data into training and test data 
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
data_tr, data_ts = train_test_split(dataset, test_size = 0.2, random_state = 0) 

# storing locally all the test dat and train data
pd.DataFrame(x).to_csv("../univdata/inputdata.csv")
pd.DataFrame(y).to_csv("../univdata/outputdata.csv")
data_tr.to_csv("../univdata/train_data.csv")
data_ts.to_csv("../univdata/test_data.csv")

# Feature Scaling
from sklearn.preprocessing import StandardScaler
# Used to normalize the data for better result
sc_x=StandardScaler()
x_train=sc_x.fit_transform(x_train)
x_test=sc_x.transform(x_test)
y = y.reshape(-1 ,1)
y_train = y_train.reshape(-1 ,1)
y_test = y_test.reshape(-1 ,1)


pd.DataFrame(x_train).to_csv("../univdata/input_train_data.csv")
pd.DataFrame(x_test).to_csv("../univdata/input_test_data.csv")
pd.DataFrame(y_train).to_csv("../univdata/output_train_data.csv")
pd.DataFrame(y_test).to_csv("../univdata/output_test_data.csv")


# K-Nearest Neighbour
def knn(query_x,X,Y,k=20):
    rec = []
    vals=[]
    pairs = []
    m=X.shape[0]
    # finding euclidean distance between the input vector and training data
    for i in range(m):
        dist = np.sqrt(sum((query_x-X[i])**2))
        vals.append((dist,Y[i]))
    
    # pick first k values after sorting the result    
    vals=sorted(vals)
    vals=vals[:k]
    vals=np.array(vals)
    
    # pick all the unique values and counting the count    
    new_vals = np.unique(vals[:,1],return_counts=True)
    
    for i in range(len(new_vals[0])):
        pairs.append((new_vals[1][i], int(new_vals[0][i]) ))
    pairs.sort( key = lambda x : x[0], reverse = True )
    for i in range(len(pairs)):
        rec.append(pairs[i][1])
    recomendation.append(rec)
    
size=int(x_test.shape[0])
anslist = []
recomendation = []
count = 0

# calling knn function for each query of test 
for i in range(size):
    query_x=x_test[i]
    knn(query_x, x_train, y_train)
    count+=1
    print(count)
    pred = int(recomendation[i][0])
    anslist.append(pred)

    
dict={"Outcome" : anslist}
y_knn = pd.DataFrame(dict)

y_knn.to_csv("../univdata/predictedUniv.csv")

result = labelencoder_y.inverse_transform(y_knn)
result = result.tolist()
usrName = data_ts['userName'].tolist()
univrec = {}
count = 0
for i in range(len(x_test)):
    dict = {"univ" : recomendation[i]}
    result = labelencoder_y.inverse_transform(pd.DataFrame(dict)).tolist()
    univrec[usrName[i]] = result
    if y_test[i] in recomendation[i]:
        count+=1

with open('../univdata/univRecmnd.p', 'wb') as fp:
    pickle.dump(univrec, fp, protocol=pickle.HIGHEST_PROTOCOL)
    
'''with open('../univdata/univRecmnd.p', 'rb') as fp:
    univRecmnd = pickle.load(fp)'''
    
acc = count*100/len(x_test)


