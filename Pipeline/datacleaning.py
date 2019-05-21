#!/usr/bin/env python
# coding: utf-8

# In[1]:


#importing libraries

import pandas as pd

def data_load_clean():
        
    #Loading all the csv files
    
    df_aisles = pd.read_csv("data/aisles.csv")
    df_departments = pd.read_csv("data/departments.csv")
    df_order_products_prior = pd.read_csv("data/order_products__prior.csv")
    df_order_products_train = pd.read_csv("data/order_products__train.csv")
    df_orders = pd.read_csv("data/orders.csv")
    
    
    # ## Data Cleaning
    
    # In[2]:
    
    
    #Reading the orders.csv file
    df_orders.head()
    
    
    # In[3]:
    
    
    #Counting the number of rows and columns in orders.csv
    df_orders.shape
    
    
    # In[4]:
    
    
    #Finding if the dataset has any null values
    total=df_orders.isnull().sum()
    total
    
    
    # In[5]:
    
    
    #checking for the percentage
    percentage=total/df_orders.isnull().count()
    percentage
    
    
    # In[6]:
    
    
    missing_value_in_orders = pd.concat([total,percentage],keys=['Total','Percentage'],axis=1)
    missing_value_in_orders
    
    
    # Only 6% of the data is missing. So we can exclude this missing data and use it
    
    # In[7]:
    
    
    df_neworders=df_orders[df_orders['days_since_prior_order'].notnull()]
    df_neworders.head()
    
    
    # Similarly checking for the remaining datasets:
    
    # In[8]:
    
    
    #aisles
    aislestotal=df_aisles.isnull().count()
    aislestotal
    
    
    # In[9]:
    
    
    aisles_percentage_miss=aislestotal/df_aisles.isnull().count()
    aisles_percentage_miss
    
    
    # In[10]:
    
    
    missing_value_in_aisles = pd.concat([aislestotal,aisles_percentage_miss],keys=['Total','Percentage'],axis=1)
    missing_value_in_aisles
    
    
    # In[11]:
    
    
    #departments
    totaldepartments=df_departments.isnull().sum()
    totaldepartments
    
    
    # In[12]:
    
    
    department_percentage=totaldepartments/df_departments.isnull().count()
    department_percentage
    
    
    # In[13]:
    
    
    missing_value_in_departments = pd.concat([totaldepartments,department_percentage],keys=['Total','Percentage'],axis=1)
    missing_value_in_departments
    
    
    # In[14]:
    
    
    #orders_prior
    totalorder_products_prior=df_order_products_prior.isnull().sum()
    totalorder_products_prior
    
    
    # In[15]:
    
    
    percentageorder_products_prior=totalorder_products_prior/df_order_products_prior.isnull().count()
    percentageorder_products_prior
    
    
    # In[16]:
    
    
    missing_value_in_order_products_prior = pd.concat([totalorder_products_prior,percentageorder_products_prior],keys=['Total','Percentage'],axis=1)
    missing_value_in_order_products_prior
    
    
    # In[17]:
    
    
    #order_train
    totalOrderProducttrain=df_order_products_train.isnull().sum()
    totalOrderProducttrain
    
    
    # In[18]:
    
    
    percentageOrdertrain=totalOrderProducttrain/df_order_products_train.isnull().count()
    percentageOrdertrain
    
    
    # In[19]:
    
    
    missing_value_in_order_train = pd.concat([totalOrderProducttrain,percentageOrdertrain],keys=['Total','Percentage'],axis=1)
    missing_value_in_order_train
    
    
    # Except the orders data, all the other data looks fine,
    # So creating a new data file for the existing order dataset
    
    # In[20]:
    
    
    #creating the clean csv file
    df_neworders.to_csv('data/clean_orders.csv')
    
    
    # In[ ]:
    



