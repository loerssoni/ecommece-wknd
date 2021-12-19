def construct_outlier_variables(df, outlier_days=['2017-11-24'], day_name='outlier_day',
                                outlier_weeks = ['2017-11-23'], week_name='outlier_week'):
    outlier_days = pd.to_datetime(outlier_days).date
    df[day_name] = df.index.isin(outlier_days)
    
    outlier_weeks = [pd.date_range(d, d+pd.Timedelta('7d')).date for d in pd.to_datetime(outlier_weeks)]
    outlier_weeks = np.hstack(outlier_weeks)
    df[week_name] = df.index.isin(outlier_weeks)
    return df

def construct_weekday_dummies(df):
    weekdays = pd.get_dummies(df.index.weekday).set_index(df.index)
    df = pd.concat([df, weekdays], axis=1)
    return df

def construct_rolling(df, col='demand', horizon=7, upto=10):
    for i in range(1, upto):
        df[f'rolling_{i}'] = df[col].rolling(i).mean().shift(horizon)
    return df

def construct_lags(df, col='demand', horizon=7, upto=7):
    for i in range(1, upto+1):
        df[f'lag_{i}'] = df[col].shift(horizon + i)
    return df

    
def construct_features(df, outlier_args={}, horizon=7, lag_upto=10, roll_upto=10):
    df = construct_outlier_variables(df, **outlier_args)
    df = construct_weekday_dummies(df)
    df = construct_rolling(df, col='demand', horizon=horizon, upto=lag_upto)
    df = construct_lags(df, col='demand', horizon=horizon, upto=roll_upto)
    return df

def add_total(df, total_preds):
    df = df.join(total_preds, rsuffix='_pred_total')
    return df