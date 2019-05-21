# import the Flask class from the flask module
from flask import Flask, render_template, request
import pandas as pd
import os
    
# create the application object
app = Flask(__name__)
app._static_folder = os.path.abspath("templates/static/")
consumerDF = pd.DataFrame()
productDF =pd.DataFrame()
OrderProductsPriorDF =pd.DataFrame()
OrderProductTrainDF = pd.DataFrame()
consumerNamelist = pd.DataFrame()
productNamelist =pd.DataFrame()
currentCartSession = []

@app.route('/')
def login():
    return render_template('login.html')


@app.route('/loginsubmit', methods=['GET', 'POST'])
def loginsubmit():
    username = ''   
    if request.method == 'POST':
        username = request.form['username']
    
    if(username == 'admin'):
        return render_template('admin.html', consumerDF = consumerDF)
    else:
        currentCartSession.clear()
        return render_template('cart.html', username = username, productDF = productDF)


@app.route('/admitsubmit', methods=['GET', 'POST'])
def admitsubmit():
    consumer = ''   
    if request.method == 'POST':
        consumer = request.form['consumer']
    
    ConsumerFiltered = consumerDF[consumerDF['user_id'] == int(consumer)]
    
    
    # All orders (prior & train): order_id, product_id
    OrderProductDF = pd.concat([OrderProductsPriorDF, OrderProductTrainDF])
    
    # orders in prior/train merged with product names
    OrderProductFilteredDF = pd.merge(ConsumerFiltered, 
                                    OrderProductDF, how='left', on='order_id')
    
    MasterDF = pd.merge(OrderProductFilteredDF, 
                                    productDF, how='left', on='product_id')
    
    MasterDF = MasterDF.groupby(['product_id', 'product_name'], as_index=False).agg({'reordered': 'sum'})
    MasterDF = MasterDF.sort_values(by='reordered', ascending=False)
    MasterDF = MasterDF.rename(index=str, columns={"product_name": "Product Name", 'reordered': "Total Reordered"})
    
                              
    return render_template('admin.html',tables=[MasterDF[['Product Name', 'Total Reordered']].to_string(index = False).to_html()],
        titles = ['na', 'Consumer History'])

@app.route('/cartsubmit', methods=['GET', 'POST'])
def cartsubmit():
    consumer = ''
    product = ''
    if request.method == 'POST':
        product = int(request.form['product'])
    
    if(action == 'product' and (product not in currentCartSession)):
        currentCartSession.append(product) 
    
    MasterDF = productDF[productDF.product_id.isin(currentCartSession)]
    MasterDF = MasterDF.rename(index=str, columns={"product_name": "Product Name"})
                           
    return render_template('cart.html',tables=[MasterDF[['Product Name']].to_string(index = False).to_html()],
        titles = ['na', 'Cart'])
    
@app.route("/tables")
def show_tables():
    data = pd.read_excel('dummy_data.xlsx')
    data.set_index(['Name'], inplace=True)
    data.index.name=None
    females = data.loc[data.Gender=='f']
    males = data.loc[data.Gender=='m']
    return render_template('view.html',tables=[females.to_html(classes='female'), males.to_html(classes='male')],
    titles = ['na', 'Female surfers', 'Male surfers'])



# start the server with the 'run()' method
if __name__ == '__main__':
    consumerDF = pd.read_csv('data/orders.csv')
    productDF = pd.read_csv('data/products.csv')
    OrderProductsPriorDF = pd.read_csv('data/order_products__prior.csv')
    OrderProductTrainDF = pd.read_csv('data/order_products__train.csv')
    consumerNamelist = sorted(consumerDF['user_id'].unique())
    productNamelist = productDF['product_name'].unique()
    app.run(debug=True)
