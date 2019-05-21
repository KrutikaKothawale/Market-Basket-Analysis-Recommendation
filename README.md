# Market-Basket-Analysis-Recommendation

### Web Application Link : 
https://instacartanalytics.herokuapp.com/

### Dataset :
We have build models using the dataset below: 
• https://www.instacart.com/datasets/grocery-shopping-2017

This repository contains end-to-end tutorial-like code samples to help solve text classification problems using machine learning.

### Prerequisites:

*   [Scikit-learn](http://scikit-learn.org/stable/)
*   [Light Gradient boosting] (https://lightgbm.readthedocs.io/en/latest/)
*   [Logistic Regression] (https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html)
*   [Truricreate] 

### Modules:

We have one module for each step in the text classification workflow.

1. **Data Cleaning.ipynb** - Functions to load and clean data from different datasets. For each of the dataset we:

+ Read the required fields (texts and labels).
+ Do any pre-processing if required. For example, cleaning data (handling missing values, etc)


2. **LightGBM_Final.ipynb*  -- Prediction Model

+ Merges and joins to datasets
+ Extensive Feature Engineering to get optimal results of prediction
+ Split the data into training and validation sets
+ Build the model to predict if the customer will reorder or not
+ Calculated Metrics: F1_score, Precision, recall, ROC curve, AUC, Confusion Matrix

3. *Logistic Regression.ipynb*   -- Prediction Model

+ Merges and joins to datasets
+ Extensive Feature Engineering to get optimal results of prediction
+ Split the data into training and validation sets
+ Build the model to predict if the customer will reorder or not
+ Calculated Metrics: F1_score, Precision, recall, ROC curve, AUC, Confusion Matrix

4. *RecommendationModel.ipynb*  -- Recommendation Model

+ Create a utility matrix of user_product and their quantities
+ Normalized the data 
+ Train three models namely popularity, cosine, pearson using Turicreate 
+ Compare models based on precision, recall and RMSE Scores

3. *LUIGI* - Pipelining

+ The jupyter notebooks are actually an another representation of the pipelined code:
+ For pipelining, we have used Luigi package
+ Documentation: https://luigi.readthedocs.io/en/stable/
+ Pipeline folder has four files:

   *datacleaning.py*  
+ This file has necessary user defined functions to load and clean the data. It outputs the cleaned data in the form of csv files.

   *featureengineering.py* 
+ This file has all the nessecary functions to preprocess the data before it could be passed to the model i.e. generating new features,    creating train and test data sets, etc.
+ The input to this file is the output of datacleaning.py file

   *buildmodel.py*  
+ This is the final file containing the final tasks required to generated the model in an external pickle file. The input to this model   is the output of featureengineering.py file. The pickle file would be further used by our Flask web application.

   *run_luigi.py* 
+ This file is the main file which controls the execution of above three files.



### CLAAT Document : 
+ Project Proposal: https://codelabs-preview.appspot.com/?file_id=100MhnqZGVbRi3XDuG272nsCoKidBvNYNakn8gD9jRh0#0
+ Report: https://codelabs-preview.appspot.com/?file_id=18fnXR4mLXmYJTgLYWbRml1yIPukWQVflZ4j0j070Sy8#0

