import pandas as pd

def cleaning_data(df):

    df = df.drop(columns = ["Gig_ID","Merch_Sales_Post_Show"])

    ################################################################ Cleaning Crowd_Size

    df.loc[df["Crowd_Size"] <= 0, "Crowd_Size"] = None

    # computing z-score
    df["z_score"] = (df["Crowd_Size"] - df["Crowd_Size"].mean()) / df["Crowd_Size"].std()

    # marking extreme outliers as null (e.g., 50,000)
    df.loc[df["z_score"].abs() > 3, "Crowd_Size"] = None

    # impute missing values using median
    df["Crowd_Size"] = df["Crowd_Size"].fillna(df["Crowd_Size"].median())

    # cleanup helper column
    df = df.drop(columns=["z_score"])

    ################################################################# Cleaning Volume_Level

    # Imputing Volume_Level (Refer EDA_Cleaning.ipynb)
    if "Volume_Level" in df.columns:
        df.loc[df["Volume_Level"] <= 0, "Volume_Level"] = None
        
        z = (df["Volume_Level"] - df["Volume_Level"].mean()) /  df["Volume_Level"].std()
        df.loc[z.abs() > 3, "Volume_Level"] = None

    df["Volume_Level"] = df["Volume_Level"].fillna(df["Volume_Level"].median())


    ################################################################# Money currencies cleaning
    EUR_TO_USD=1.09
    GBP_TO_USD=1.27

    prices_usd = []

    for val in df["Ticket_Price"]:
        if pd.isna(val):
            prices_usd.append(None)
            continue

        s= str(val).strip().lower()   #lower uses for to convert FREE/.. to free

       # assignin 0 for free tickets
        if s == "free":
            prices_usd.append(0)
            continue

       # removing VIP 
        if "(" in s:
            s = s.split("(")[0]

        s = s.replace("usd", "").strip()

        if "€" in s:
            prices_usd.append(float(s.replace("€", "")) * EUR_TO_USD)

        elif "£" in s:
            prices_usd.append(float(s.replace("£", "")) * GBP_TO_USD)

        elif "$" in s:
            prices_usd.append(float(s.replace("$", "")))

        else:
            prices_usd.append(float(s))  # assume already USD

    df["Ticket_Price"] = prices_usd
    df["Ticket_Price"] = df["Ticket_Price"].fillna(df["Ticket_Price"].median())

    ############################################################################### Cleaning Date and Time

    time_cat = []

    for val in df["Show_DateTime"]:
        
        cat = "Late_Night"

        if pd.isna(val):
            time_cat.append("Late Night")
            continue

        s = str(val).lower().strip()

    # 1. textual cases
        if "morning" in s:
            category = "Morning"
        elif "afternoon" in s:
            category = "Afternoon"
        elif "evening" in s:
            category = "Evening"
        elif "late night" in s:
            category = "Late Night"


        else:
            for part in s.split():
                if ":" in part:
                    try:
                        hour = int(part.split(":")[0])

                        if "pm" in s and hour != 12:
                            hour += 12
                        if "am" in s and hour == 12:
                            hour = 0

                        if 5 <= hour < 12:
                            category = "Morning"
                        elif 12 <= hour < 17:
                            category = "Afternoon"
                        elif 17 <= hour < 22:
                            category = "Evening"
                        else:  
                            category = "Late Night"
                        break
                        
                    except:
                        pass

        time_cat.append(category)
    
    df["Show_DateTime"] = time_cat


    return df  