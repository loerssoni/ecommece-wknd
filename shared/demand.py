import pandas as pd
import numpy as np
from shared.ingest import download_default_s3

def format_datecols(data, cols):
    for col in cols:
        data[col] = pd.to_datetime(data[col])
    return data

## define separate load function, so it is easier to plugin a data source here
def get_df(filename):
    items = pd.read_csv(filename)
    return items


def process_orders(filename, included_status = ['delivered']):
    orders = get_df(filename)
    
    # format datecols
    datecols = orders.loc[:,'order_purchase_timestamp':].columns
    orders = format_datecols(orders, datecols)
    
    orders = orders[orders['order_status'].isin(included_status)].copy()
    return orders
    

def get_delivered_items(orders_filename='tempdata/olist_orders_dataset.csv',
                        items_filename='tempdata/olist_order_items_dataset.csv',
                        products_filename='tempdata/olist_products_dataset.csv',
                        ingest=False, ingest_args={}, orders_args={}):
    if ingest:
        download_default_s3(**ingest_args)
    
    items = get_df(items_filename)
    orders = process_orders(orders_filename, **orders_args)
    orders = items.merge(orders, on='order_id')
    
    del items

    products = get_df(products_filename)
    
    orders = orders.merge(products[['product_id', 'product_category_name']], how='left', on='product_id')
    return orders

def demand_from_orders(orders, aggtype='demand',
                       index_col='order_purchase_timestamp',
                      freq='d', by_category=True):
    
    agg_funcs = {'revenue':'sum', 'demand':'count'}
    try:
        agg_func = agg_funcs[aggtype]
    except KeyError:
        agg_func = aggtype
    
    orders = orders.set_index(index_col)
    orders = orders.sort_index()
    
    ts = orders[['price']].resample(freq).agg(agg_func)
    if by_category:
        by_cat = orders.groupby('product_category_name')['price'].resample(freq).agg(agg_func)
        by_cat = by_cat.reset_index(level=0)
        ts['product_category_name'] = 'total'
        ts = pd.concat([ts, by_cat])
    ts.columns = ts.columns.str.replace('price', aggtype)
    return ts

def create_ds(read_args={}, process_args={}):
    orders = get_delivered_items(**read_args)
    demands = demand_from_orders(orders, **process_args)
    return demands
    