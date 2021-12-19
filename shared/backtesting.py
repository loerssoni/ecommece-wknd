import pandas as pd
import numpy as np

from sklearn.linear_model import LassoCV
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def backtest_pred(X, y, dates, tscv, model_func):
    preds = {'date':[], 'true':[],'pred':[]}
    for tr_ind, ts_ind in tscv.split(y):
        preds['date'] += dates[ts_ind].tolist()
        preds['true'] += y[ts_ind].tolist()
        
        m = model_func()
        m.fit(X[tr_ind], y[tr_ind])
        
        preds['pred'] += m.predict(X[ts_ind]).tolist()

    pred_df = pd.DataFrame(preds)
    pred_df = pred_df.set_index('date')
    m = model_func()
    m.fit(X, y)
    return pred_df, m

def get_tscv(ts, split_day, horizon=7, n_splits=20):
    n_ts = np.sum(ts.index >= split_day)
    test_size = n_ts // n_splits
    tscv = TimeSeriesSplit(n_splits=n_splits, gap=horizon, test_size=test_size)
    return tscv

def get_x_y_dates(ts, ycol='demand', dropcols=['product_category_name']):
    X = ts.loc[:, ~ts.columns.isin([ycol]+dropcols)].values
    y = ts[ycol].values
    dates = ts.index    
    return X, y, dates

def train_test_iteration(ts, model_func, split_day, horizon=7,
                         n_splits=20):
    metrics = {}
    X, y, dates = get_x_y_dates(ts)
    tscv = get_tscv(ts, split_day, horizon, n_splits)
    pred_df, model = backtest_pred(X, y, dates, tscv, model_func=model_func)
    metrics['mae'] = mean_absolute_error(pred_df['true'], pred_df['pred'])
    metrics['r2'] = r2_score(pred_df['true'], pred_df['pred'])
    return model, metrics, pred_df