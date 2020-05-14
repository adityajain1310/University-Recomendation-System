#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 21:54:43 2020

@author: aditya
"""

univIdList = ['432', '1370', '1852', '1911', '1876', '1780', '920', '918', '917', '153', '812', '583', '582',
              '1410', '1366', '419', '1319', '1222', '1220', '1127', '1024', '658', '145', '144', '142', '139',
              '138', '136', '136', '980', '880', '1613', '1586', '1585', '133', '1471', '252', '1464', '647',
              '1202', '408', '570', '1559', '1463', '397', '1301', '390', '206', '1819', '1510', '1507', '1678',
              '716', '48', '969']

univList = ['Worcester Polytechnic Institute', 'Wayne State University', 'Virginia Polytechnic Institute and State University',
            'University of Wisconsin Madison', 'University of Washington', 'University of Utah', 'University of Texas Dallas',
            'University of Texas Austin', 'University of Texas Arlington', 'University of Southern California',
            'University of Pennsylvania', 'University of North Carolina Charlotte', 'University of North Carolina Chapel Hill',
            'University of Minnesota Twin Cities', 'University of Michigan Ann Arbor', 'University of Massachusetts Amherst',
            'University of Maryland College Park', 'University of Illinois Urbana-Champaign', 'University of Illinois Chicago',
            'University of Florida', 'University of Colorado Boulder', 'University of Cincinnati',
            'University of California Santa Cruz', 'University of California Santa Barbara',
            'University of California San Diego', 'University of California Los Angeles', 'University of California Irvine',
            'University of California Davis', 'University of California Davis', 'University of Arizona',
            'Texas A and M University College Station', 'Syracuse University', 'SUNY Stony Brook', 'SUNY Buffalo',
            'Stanford University', 'Rutgers University New Brunswick/Piscataway', 'Purdue University', 'Princeton University',
            'Ohio State University Columbus', 'Northwestern University', 'Northeastern University',
            'North Carolina State University', 'New York University', 'New Jersey Institute of Technology',
            'Massachusetts Institute of Technology', 'Johns Hopkins University', 'Harvard University',
            'Georgia Institute of Technology', 'George Mason University', 'Cornell University', 'Columbia University',
            'Clemson University', 'Carnegie Mellon University', 'California Institute of Technology',
            'Arizona State University']

univNameIdDict = {}
for i in range(len(univIdList)):
    univNameIdDict[univIdList[i]] = univList[i]
    
userDict= {}  
count = 0
for ln in open("../univdata/allUsers.csv"):
    vals = ln.split(",")
    userDict[vals[0]] = ln


Attlist = ["userName", "major", "researchExp", "industryExp", "specialization", "toeflscore", "program", "department", 
        "toeflEssay", "internExp", "greV", "greQ", "userprofilelink", "journalPubs", "greA", "topperCgpa", "termAndYear",
        "confPubs", "ugcollege", "gmatA", "cgpa", "gmatQ", "cgpaScale", "gmatV", "univName", "admit"]
final = open("../univdata/finaldata.csv", "w")
final.write(','.join(Attlist) + "\n")

for ent in open("../univdata/allColleges.json"):
    ent = eval(ent)
    usrName = ent['userName']
    if usrName not in userDict:
        print (usrName)
        continue
    usrstr = userDict[usrName].strip()
    vals = usrstr.split(",")
    vals.append(univNameIdDict[ent['univId']])
    vals.append(ent['admit'])
    final.write(','.join(vals) + "\n")    
    