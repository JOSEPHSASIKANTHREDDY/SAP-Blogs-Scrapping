#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 18:04:03 2021

@author: i327885
"""
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import getpass 
import requests
from bs4 import BeautifulSoup
import pandas as pd

# driver=webdriver.Chrome('/Users/i327885/Desktop/DS_ML/Online/Jp NaN/Gmail Login/chromedriver')
# driver.get('https:google.com')
title=[]
author=[]
postedon=[]
blogtype=[]
comments=[]
likes=[]
emptype=[]
tags=[]
links=[]

ENDPOINT='https://blogs.sap.com'
PATH='/page/'

for i in range(1,101):

    url=ENDPOINT+PATH+str(i)+'/'
    print(url)
    
    res=requests.get(url).content;
    
    soups=BeautifulSoup(res,'html.parser')
    
    s=soups.find_all('li',class_='dm-contentListItem')
    # print(len(s))
    
    
    for soup in soups.find_all('li',class_='dm-contentListItem'):
        
        # print(soup)
        
        
        
        blog_title=soup.find_all('div',class_='dm-contentListItem__title')
        title.append(blog_title[0].text)
        
        blog_author=soup.find_all('a',class_='dm-user__name')
        author.append(blog_author[0].text)
        
        posted_on=soup.find_all('span',class_='dm-user__date')
        postedon.append(posted_on[0].text.split('posted on')[1].strip())
        
        blog_type=soup.find_all('span',class_='dm-user__category')
        blogtype.append(blog_type[0].text)
        
        comment=soup.find_all('div',class_='dm-contentListItem__metadataNumber')
        comments.append(comment[0].text)
        likes.append(comment[1].text)
        
        # print(comments)
        emp_type=soup.find_all('span',class_='dm-icon-encoded--employee')
        emptype.append((emp_type[0]['data-role-name'] if len(emp_type) else 'N/A'))
     
        tag=','.join([i.text.strip() for i in soup.find_all('a',class_='dm-tags__list-item')])
        tags.append(tag)
        
        link=soup.find('div',class_='dm-contentListItem__title').find_all('a')
        links.append(link[0]['href'])
    
data=pd.DataFrame({
    "Title":title,
    'Author':author,
    'Date':postedon,
    'Blog Type':blogtype,
    'Comments':comments,
    'Likes':likes,
    'Employee Type':emptype,
    'Tags':tags,
    'Link':links
    })
print(data.head())
data.to_csv('blogs.csv',index=False)
