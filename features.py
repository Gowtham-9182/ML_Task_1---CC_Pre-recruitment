import pandas as pd
import numpy as np

def features_preparation(df):
    
    # dropping columns
    df = df.drop(columns = ["Band_Outfit","Moon_Phase"])

    # Encoding features with One Hot Label encoder
    df = pd.get_dummies(
        df,
        columns=["Venue_ID", "Weather", "Show_DateTime"],
        drop_first = True
    )
    # without drop first = true, it will just create excess columns
    
    df = df.astype(int)


    return df


    

