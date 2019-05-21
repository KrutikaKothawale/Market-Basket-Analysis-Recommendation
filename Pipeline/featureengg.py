
import pandas as pd
import numpy as np



def feature_engineering():
    # ## Loading Datasets:
    
    # ##### List of files imported and loaded
    # 
    # * Aisles.csv – This contains the names of the aisles based on the products in them.
    # * Departments.csv – It has the names of department categorized by products types.
    # * Order_Product_Prior – It has details of all the previous customer orders.
    # * Order_Product_Train.csv – This is the dataset which will be used to train the test dataset explained next.  
    # * Orders.csv – It is the main table containing details about the customer orders and also tells which record belongs to which table, train, prior or test.
    # * Products.csv – This contain detail of all the products sold by Instakart along with their ProductID.
    
    # In[2]:
    
    
    aislesDF = pd.read_csv('aisles.csv')
    departmentsDF = pd.read_csv('departments.csv')
    orderProductsPriorDF = pd.read_csv('order_products__prior.csv')
    orderProductsTrainDF = pd.read_csv('order_products__train.csv')
    ordersDF = pd.read_csv('clean_orders.csv')
    productsDF = pd.read_csv('products.csv')
    
    
    # In[3]:
    
    
    aislesDF.head(2)
    
    
    # In[4]:
    
    
    departmentsDF.head(2)
    
    
    # In[5]:
    
    
    orderProductsPriorDF.head(2)
    
    
    # In[6]:
    
    
    orderProductsTrainDF.head(2)
    
    
    # In[7]:
    
    
    ordersDF.head(2)
    
    
    # In[8]:
    
    
    productsDF.head(2)
    
    
    # ## Feature Engineering:
    
    # ### Features Engineering on Users:
    
    # In[9]:
    
    
    # priors: merge ordersDF to order_products_priorDF
    ordersDF.set_index('order_id', inplace = True, drop = False)
    priors = pd.merge(orderProductsPriorDF, ordersDF, how = 'left', on = 'order_id')
    
    
    # In[10]:
    
    
    priors.head(2)
    
    
    # In[11]:
    
    
    users = pd.DataFrame()
    users['total_user'] = priors.groupby('product_id').size()
    users['all_users'] = priors.groupby('product_id')['user_id'].apply(set)
    users['total_distinct_users_perProduct'] = users.all_users.map(len)
    
    
    # Reordering ratio - “does the user tends to purchase new products?”
    
    # In[12]:
    
    
    users_feature1 = priors.         groupby("user_id").         agg({'reordered': {'U_rt_reordered': 'mean'}})
    
    
    # In[13]:
    
    
    users_feature1.columns = users_feature1.columns.droplevel(0)
    users_feature1 = users_feature1.reset_index()
    
    
    # In[14]:
    
    
    users_feature1.head()
    
    
    # U_basket_sum - Number of products purchased
    # 
    # U_basket_mean - Mean number of products purchased per order (basket size) - “how much products does the user buys?”
    # 
    # U_basket_std - Standard deviation number of products per order - “does the user have different basked size?
    
    # In[15]:
    
    
    users_feature2 = priors.         groupby(["user_id", "order_id"]).size().         reset_index().         drop("order_id", axis=1).         groupby("user_id").         agg([np.sum, np.mean, np.std])
    
    
    # In[16]:
    
    
    users_feature2.columns = ["U_basket_sum", "U_basket_mean", "U_basket_std"]
    
    
    # In[17]:
    
    
    users_feature2 = users_feature2.reset_index()
    
    
    # In[18]:
    
    
    users_feature2.head(2)
    
    
    # In[19]:
    
    
    customersRaw = pd.DataFrame()
    customersRaw['avgDaysBetwOrders'] = ordersDF.groupby(
        'user_id')['days_since_prior_order'].mean().astype(np.float32)
    
    customersRaw['NumberOfOrders'] = ordersDF.groupby('user_id').size().astype(np.int16)
    
    
    # In[20]:
    
    
    customers = pd.DataFrame()
    
    customers['total_items'] = priors.groupby('user_id').size().astype(np.int16)
    customers['all_products'] = priors.groupby('user_id')['product_id'].apply(set)
    customers['total_unique_items'] = customers.all_products.map(len).astype(np.float32)
    
    customers = customers.join(customersRaw)
    customers['avg_per_cart'] = (customers.total_items / customers.NumberOfOrders).astype(np.float32)
    
    
    # In[21]:
    
    
    customers.head(2)
    
    
    # ## User & Product Features:
    
    # In[22]:
    
    
    #UP_order_strike
    
    
    # In[23]:
    
    
    priors["date"] = priors.iloc[::-1]['days_since_prior_order'].cumsum()[::-1].shift(-1).fillna(0)
    max_group = priors["order_number"].max()
    priors["order_number_reverse"] = max_group - priors["order_number"]
    
    
    # In[24]:
    
    
    # Could be something else than 1/2
    priors["users_prod_date_strike"] = 1 / 2 ** (priors["date"] / 7)
    # order_prior["UP_order_strike"] = 100000 * 1/2 ** (order_prior["order_number_reverse"])
    priors["users_prod_order_strike"] = 1 / 2 ** (priors["order_number_reverse"])
    
    order_stat = priors.groupby('order_id').agg({'order_id': 'size'})         .rename(columns={'order_id': 'order_size'}).reset_index()
    priors = pd.merge(priors, order_stat, on='order_id')
    priors['add_to_cart_order_inverted'] = priors.order_size - priors.add_to_cart_order
    priors['add_to_cart_order_relative'] = priors.add_to_cart_order / priors.order_size
    
    users_products = priors.         groupby(["user_id", "product_id"]).         agg({'reordered': {'users_prod_nb_reordered': "size"},              'add_to_cart_order': {'users_prod_add_to_cart_order_mean': "mean"},              'add_to_cart_order_relative': {'users_prod_add_to_cart_order_relative_mean': "mean"},              'add_to_cart_order_inverted': {'users_prod_add_to_cart_order_inverted_mean': "mean"},              'order_number_reverse': {'users_prod_last_order_number': "min", 'users_prod_first_order_number': "max"},              'date': {'users_prod_last_order_date': "min", 'users_prod_first_date_number': "max"},              'users_prod_date_strike': {"users_prod_date_strike": "sum"},              'users_prod_order_strike': {"users_prod_order_strike": "sum"}})
    
    users_products.columns = users_products.columns.droplevel(0)
    users_products = users_products.reset_index()
    
    
    # In[25]:
    
    
    users_products.head()
    
    
    # In[26]:
    
    
    productsRaw = pd.DataFrame()
    
    productsRaw['ordersTotal'] = orderProductsPriorDF.groupby(
        orderProductsPriorDF.product_id).size().astype(np.int32)
    
    productsRaw['reordersTotal'] = orderProductsPriorDF['reordered'].groupby(
        orderProductsPriorDF.product_id).sum().astype(np.float32)
    
    productsRaw['reorder_rate'] = (productsRaw.reordersTotal / productsRaw.ordersTotal).astype(np.float32)
    
    products = productsDF.join(productsRaw, on = 'product_id')
    products.head()
    
    
    # In[27]:
    
    
    customerProd = priors.copy()
    customerProd['user_product'] = (customerProd.product_id + 
                                        customerProd.user_id * 100000).fillna(0).astype(np.int64)
    
    customerProd = customerProd.sort_values('order_number')
    
    customerProd = customerProd.groupby('user_product', sort = False).agg(
    {'order_id': ['size', 'last', 'first'], 'add_to_cart_order': 'sum'})
    
    customerProd.columns = ['numbOfOrders', 'last_order_id', 'first_order_id','sum_add_to_cart_order']
    customerProd.astype(
        {'numbOfOrders': np.int16, 'last_order_id': np.int32, 'first_order_id': np.int32, 'sum_add_to_cart_order': np.int16}, 
        inplace=True)
    
    
    # In[28]:
    
    
    customerProd.head()
    
    
    # In[29]:
    
    
    priors.head()
    
    
    # ## Function to get all Features:
    
    # In[30]:
    
    
    def get_features(specified_orders, given_labels = False):
        print('create initial empty list')
        orders_list = []
        products_list = []
        labels = []
        
        training_index = set(orderProductsTrainDF.index)
        
        for row in specified_orders.itertuples():
            user_id = row.user_id
            order_id = row.order_id
            
            user_products = customers['all_products'][user_id]
            products_list += user_products
            orders_list += [order_id] * len(user_products)
            
            if given_labels:
                labels += [(order_id, product) in training_index for product in user_products]
            
        DF = pd.DataFrame({'order_id': orders_list, 'product_id': products_list}, dtype = np.int32)
        labels = np.array(labels, dtype = np.int8)
       
        DF['users_prod_add_to_cart_order_mean'] = DF.map(users_products.users_prod_add_to_cart_order_mean)
        DF['users_prod_last_order_number'] = DF.map(users_products.users_prod_last_order_number)
        DF['user_id'] = DF.order_id.map(ordersDF.user_id)
        DF['user_total_orders'] = DF.user_id.map(customers.NumberOfOrders)
        DF['user_total_items'] = DF.user_id.map(customers.total_items)
        DF['total_unique_items'] = DF.user_id.map(customers.total_unique_items)
        DF['user_avgDaysBetwOrders'] = DF.user_id.map(customers.avgDaysBetwOrders)
        DF['user_avg_per_cart'] = DF.user_id.map(customers.avg_per_cart)    
        DF['order_hour_of_day'] = DF.order_id.map(ordersDF.order_hour_of_day)
        DF['days_since_prior_order'] = DF.order_id.map(ordersDF.days_since_prior_order)
        DF['daysSincePrior_avgDaysBetw_ratio'] = DF.days_since_prior_order / DF.user_avgDaysBetwOrders   
        DF['aisle_id'] = DF.product_id.map(products.aisle_id)
        DF['department_id'] = DF.product_id.map(products.department_id)
        DF['product_order'] = DF.product_id.map(products.ordersTotal)
        DF['product_reorder'] = DF.product_id.map(products.reordersTotal)
        DF['product_reorder_rate'] = DF.product_id.map(products.reorder_rate)
        DF['product_distinct_user'] = DF.product_id.map(users.total_distinct_users_perProduct)
        DF['user_product_id']  = (DF.product_id + DF.user_id * 100000).astype(np.int64)
        DF.drop(['user_id'], axis = 1, inplace = True)
        DF['CP_numOrders'] = DF.user_product_id.map(customerProd.numbOfOrders)
        DF['CP_orders_ratio'] = DF.CP_numOrders / DF.user_total_orders
        DF['CP_last_order_id'] = DF.user_product_id.map(customerProd.last_order_id)
        DF['CP_avg_pos_inCart'] = DF.user_product_id.map(customerProd.sum_add_to_cart_order) / DF.CP_numOrders
        DF['CP_order_since_last'] = DF.user_total_orders - DF.CP_last_order_id.map(ordersDF.order_number)
        DF['CP_hour_vs_last'] = abs(DF.order_hour_of_day - DF.CP_last_order_id.map(
        ordersDF.order_hour_of_day)).map(lambda x: min(x, 24 - x)).astype(np.int8)
    
        
        DF.drop(['CP_last_order_id', 'user_product_id'], axis = 1, inplace = True)
        return(DF, labels)
    
    
    # ### Split Training and Test sets
    
    # In[31]:
    
    train = ordersDF[ordersDF.eval_set == 'train']
    
    orderProductsTrainDF.set_index(['order_id', 'product_id'], inplace = True, drop = False)
    
    
    # ## Features to train the model:
    
    # In[32]:
    
    

    
    
    # In[33]:
    
    
    train_train = train.sample(frac = 0.8, random_state=200)
    train_test = train.drop(train_train.index)
    
    
    # In[34]:
    
    
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
    
    
    # In[35]:
    
    
    df_train_train, labels_train_train = get_features(train_train, given_labels=True)
    
    df_train_test, labels_train_test = get_features(train_test,given_labels=True)
    
    
    df_train_train.to_csv('data/df_train_train.csv') 
    labels_train_train.to_csv('data/labels_train_train.csv') 
    df_train_test.to_csv('data/df_train_test.csv') 
    labels_train_test.to_csv('data/labels_train_test.csv')
    train_test.to_csv('data/train_test.csv') 
    

