#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 12:55:35 2020

@author: aditya
"""

import requests
from bs4 import BeautifulSoup

def yearsToMonth(durstr):
    year, mon = durstr.split(',')
    year = year.strip()
    mon  = mon.strip()
    if ' ' in year:
        year, text1 = year.split(' ')
    else:
        year = 0
    if ' ' in mon:
        mon, text2 = mon.split(' ')
    else:
        mon = 0
    total = (int(year) * 12) + int(mon)
    return total

def getuserinfofromUrl(userProfileUrl):
    userobject = {}
    userobject['userprofilelink'] = userProfileUrl
    page = requests.get(userProfileUrl)
        soup = BeautifulSoup(page.content, 'html.parser')
        allTDs = soup.table.find_all('td')
    usrattr = ["Program", "Major", "Specialization", "Term and Year", "University/College", 
               "Department", "Grade", "Topper's Grade", "Grade Scale", "Journal Publications", "Conference Publications", 
               "Industrial Experience", "Research Experience", "Internship Experience"]
    keys = ["program", "major", "specialization", "termAndyear","ugcollege", 
               "department", "cgpa", "topperCgpa", "cgpaScale", "journalPubs", "confPubs", 
               "industryExp", "researchExp", "internExp"]
    
    j = 0 
    for i in range(len(allTDs)):
        text = (allTDs[i].string or "").strip()
        print(text)
        if(text == usrattr[j]):
            if(text.find("Experience") == 1):
                val = (allTDs[i+1].string or "").strip()
                userobject[keys[j]] = yearsToMonth(val)
            else:
                userobject[keys[j]] = (allTDs[i+1].string or "").strip()
            i+=2
            j+=1
        if(text == "GRE"):
            userobject['greQ'] = (allTDs[i+2].string or "").strip()
            userobject['greV'] = (allTDs[i+4].string or "").strip()
            userobject['greA'] = (allTDs[i+6].string or "").strip()
            i+=6
        if(text == "GMAT"):
            userobject['gmatQ'] = (allTDs[i+2].string or "").strip()
            userobject['gmatV'] = (allTDs[i+4].string or "").strip()
            userobject['gmatA'] = (allTDs[i+6].string or "").strip()
            i+=6
        if(text == "TOEFL"):
            userobject['toeflscore'] = (allTDs[i+2].string or "").strip()
            userobject['toeflessay'] = (allTDs[i+4].string or "").strip()
            i+=4
        
        
        # Checking for missing props and filling default values
        for k in range(len(keys)):
            if keys[k] not in userobject:
                if keys[k] == "program":
                    userobject[keys[k]] = "MS"
                    
                if keys[k] == "termAndyear" or keys[k] == "major" or keys[k] == "specialization":
                    userobject[keys[k]] = ""
                    
                else:
                    userobject[keys[k]] = "0"
            
        if "greQ" not in userobject:
            userobject['greQ'] = "0"
        if "greV" not in userobject:
            userobject['greV'] = "0"
        if "greA" not in userobject:
            userobject['greA'] = "0"

        if "gmatQ" not in userobject:
            userobject['gmatQ'] = "0"
        if "gmatV" not in userobject:
            userobject['gmatV'] = "0"
        if "gmatA" not in userobject:
            userobject['gmatA'] = "0"
            
        if "toeflscore" not in userobject:
            userobject['toeflscore'] = "0"
        if "toeflessay" not in userobject:
            userobject['toeflessay'] = "0"
        
    return userobject

Attlist = ["userName", "major", "researchExp", "industryExp", "specialization", "toeflscore", "program", "department", 
        "toeflEssay", "internExp", "greV", "greQ", "userprofilelink", "journalPubs", "greA", "topperCgpa", "termAndYear",
        "confPubs", "ugcollege", "gmatA", "cgpa", "gmatQ", "cgpaScale", "gmatV"]


UserInfoJSON = open("../univdata/" + "allUsersdata.csv", "w")
count = 0
UserInfoJSON.write(','.join(Attlist) + "\n")
for userInfo in open("../univdata/uniqueUsers_1.txt"):
    userName, userLink = userInfo.split(",")
    vals = []
    userInfoObj = getuserinfofromUrl(userLink)
    for key in userInfoObj:
        vals.append(userInfoObj[key])
    print(vals)
    
    UserInfoJSON.write(userName + "," + userInfoObj["major"].replace(",", " ") + "," + str(userInfoObj["researchExp"]) + "," 
           + str(userInfoObj["industryExp"]) + "," + userInfoObj["specialization"].replace(",", " ") + "," 
           + str(userInfoObj["toeflscore"]) + "," + userInfoObj["program"] + "," + userInfoObj["department"] + ","
           + str(userInfoObj["toeflessay"]) + "," + str(userInfoObj["internExp"]) + "," + str(userInfoObj["greV"]) + "," 
           + str(userInfoObj["greQ"]) + "," + userInfoObj["userprofilelink"].strip() + "," + str(userInfoObj["journalPubs"]) 
           + "," + str(userInfoObj["greA"]) + "," + str(userInfoObj["topperCgpa"]) + "," + userInfoObj["termAndyear"] + "," 
           + str(userInfoObj["confPubs"]) + "," + userInfoObj["ugcollege"].replace(",", " ") + "," + str(userInfoObj["gmatA"]) 
           + "," + str(userInfoObj["cgpa"]) + "," + str(userInfoObj["gmatQ"]) + "," + str(userInfoObj["cgpaScale"]) + "," 
           + str(userInfoObj["gmatV"]))
    count+=1
print(count)