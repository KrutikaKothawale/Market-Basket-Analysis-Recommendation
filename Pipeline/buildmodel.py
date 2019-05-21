import pandas as pd
import numpy as np
import lightgbm as lgb


def build_model():

    
    df_train_train = pd.read_csv('data/df_train_train.csv') 
    labels_train_train = pd.read_csv('data/labels_train_train.csv') 
    df_train_test= pd.read_csv('data/df_train_test.csv') 
    labels_train_test= pd.read_csv('data/labels_train_test.csv')
    train_test = pd.read_csv('data/train_test.csv') 
    # In[36]:
    
    features_to_use = ['user_total_orders', 'user_total_items', 'total_unique_items', 
                  'user_avgDaysBetwOrders', 'user_avg_per_cart', 'order_hour_of_day',
                  'days_since_prior_order', 'daysSincePrior_avgDaysBetw_ratio',
                  'aisle_id', 'department_id', 'product_order', 'product_reorder',
                  'product_reorder_rate', 'CP_numOrders', 'CP_orders_ratio', 
                  'CP_avg_pos_inCart', 'CP_order_since_last', 'CP_hour_vs_last',
                  'product_distinct_user']
    
    
    # In[37]:
    
    
    f1_score = []
    precision1 = []
    recall1 = []
        
    d_train_lgb = lgb.Dataset(df_train_train[features_to_use],
                              label = labels_train_train,
                              categorical_feature = ['aisle_id', 'department_id'], free_raw_data = False)
    
    
    # ## LightBGM Train model:
    
    # In[38]:
    
    
    # Set parameters
    lgb_params = {
        'task': 'train',
        'boosting_type': 'gbdt',
        'objective': 'binary',
        'metric': {'binary_logloss'},
        'num_leaves': 96,
        'max_depth': 10,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.95,
        'bagging_freq': 5
    }
    
    ROUNDS = 80
    
    
    # ## Training model
    
    # In[39]:
    
    
    lgb_bst = lgb.train(lgb_params, d_train_lgb, ROUNDS)
    
    
    # In[40]:
    
    
    # Plot importance of predictors
    lgb.plot_importance(lgb_bst)
    
    
    # ## Predict on test data
    
    # In[41]:
    
    
    lgb_preds = lgb_bst.predict(df_train_test[features_to_use])
    df_train_test_copy = df_train_test
    df_train_test_copy['pred'] = lgb_preds
    
    
    # In[42]:
    
    # threshold = 0.2
    d = dict()
    for row in df_train_test_copy.itertuples():
        if row.pred > 0.2:
            try:
                d[row.order_id] += ' ' + str(row.product_id)
            except:
                d[row.order_id] = str(row.product_id)
                
    for order in train_test.order_id:
        if order not in d:
            d[order] = 'None'
    
    sub = pd.DataFrame.from_dict(d, orient='index')
    
    sub.reset_index(inplace=True)
    sub.columns = ['order_id', 'products']
    
    
    df_train_test_copy['true'] = labels_train_test
    
    e = dict()
    for row in df_train_test_copy.itertuples():
        if row.true == 1:
            try:
                e[row.order_id] += ' ' + str(row.product_id)
            except:
                e[row.order_id] = str(row.product_id)
    
    for order in train_test.order_id:
        if order not in e:
            d[order] = 'None'
    
    sub_true = pd.DataFrame.from_dict(e, orient='index')
    
    sub_true.reset_index(inplace=True)
    
    sub_true.columns = ['order_id', 'true']
        
    
    sub_merge = pd.merge(sub_true, sub, how = 'inner', on = 'order_id')
    
    res = list()
    
    def eval_fun(labels, preds):
        labels = labels.split(' ')
        preds = preds.split(' ')
        rr = (np.intersect1d(labels, preds))
        precision = np.float(len(rr)) / len(preds)
        recall = np.float(len(rr)) / len(labels)
        try:
            f1 = 2 * precision * recall / (precision + recall)
        except ZeroDivisionError:
            return (precision, recall, 0.0)
        return (precision, recall, f1)
    
    
    
    for entry in sub_merge.itertuples():
        res.append(eval_fun(entry[2], entry[3]))
    
    res = pd.DataFrame(np.array(res), columns=['precision', 'recall', 'f1'])
        
    
    precision1.append(np.mean(res['precision']))
    recall1.append(np.mean(res['recall']))
    f1_score.append(np.mean(res['f1']))
    
    
    # In[43]:
    
    
    f1_score
    
    
    # In[44]:
    
    
    precision1
    
    
    # In[45]:
    
    
    recall1
    
    
    # In[46]:
    
    
    import pickle
    filename = 'Trained_LightGBM_model.sav'
    pickle.dump(lgb_bst,open(filename,'wb'))
    
    
    # In[48]:
    
    
    from sklearn.metrics import confusion_matrix
    from sklearn.metrics import classification_report
        
    print("For Test Data:")
    y_test_pred_bow = lgb_bst.predict(df_train_test[features_to_use])
    for i in range(len(y_test_pred_bow)):
        if y_test_pred_bow[i] < 0.2:
            y_test_pred_bow[i] = 0
        else:
            y_test_pred_bow[i] = 1
    
    
    # In[49]:
    
    
    print("For Test Data:")
    print(confusion_matrix(labels_train_test, y_test_pred_bow))
    
    
    # In[50]:
    
    
    print(classification_report(labels_train_test, y_test_pred_bow))
    
    
    # In[ ]:
    
