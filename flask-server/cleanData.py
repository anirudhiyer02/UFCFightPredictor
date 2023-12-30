from flask import Flask, request, jsonify

app=Flask(__name__)
@app.route("/members", methods=['POST'])
def members():
    import pandas as pd
    import numpy as np
    import sklearn
    # Pass data through pandas and into a df.
    data = pd.read_csv('ufc-master.csv')
    ufcdata = pd.DataFrame(data)
    ufcdata = ufcdata.fillna(0)
    pd.set_option('display.max_columns', None)

    # Drop columns to consolidate dataset with only candidate variables
    ufcdata.columns.get_loc("empty_arena")
    ufcdata.drop(ufcdata.iloc[:,78:138],inplace = True, axis = 1)
    ufcdata.drop(['date','location','country','title_bout','R_ev','B_ev','B_odds','weight_class','no_of_rounds'],axis = 1, inplace = True)
    ufcdata.set_index(["R_fighter"]+["B_fighter"],inplace=True)
    GenderMap = {'MALE': 1, 'FEMALE': 2}
    ufcdata['gender'] = ufcdata['gender'].map(GenderMap)

    StanceMap = {'Orthodox': 1, 'Southpaw': 2}
    ufcdata['B_Stance'] = ufcdata['B_Stance'].map(StanceMap)
    ufcdata['R_Stance'] = ufcdata['R_Stance'].map(StanceMap)
    ufcdata = ufcdata.fillna(0)

    WinnerMap = {'Red': 0, 'Blue': 1}

    ufcdata['Winner'] = ufcdata['Winner'].map(WinnerMap)
    ufcdata = ufcdata.fillna(0)


    from sklearn.model_selection import train_test_split
    from sklearn.dummy import DummyClassifier
    from sklearn.metrics import mean_squared_error

    # To avoid overfitting, we will only focus on the Odds, Gender, then the differnces between the fighters in each category.

    # Additionally, there were some incorrect values in the dataset for Significant Strikes, so it was removed as a possible feature. 
    columns = ['R_odds','gender','lose_streak_dif',
        'win_streak_dif', 'longest_win_streak_dif', 'win_dif', 'loss_dif',
        'total_round_dif', 'ko_dif', 'sub_dif',
        'height_dif', 'reach_dif', 'age_dif','avg_sub_att_dif',
        'avg_td_dif']

    X = ufcdata[columns]
    y = ufcdata["Winner"]

    # print(ufcdata.shape)
    # print(X.shape)
    # print(y.shape)


    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.4,stratify=y,random_state=50)
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import (
        classification_report,
        recall_score,
        precision_score,
        accuracy_score)

    # Create a Random Forest Model

    model_rf = RandomForestClassifier(n_estimators=100, max_features=7, random_state=42)
    model_rf.fit(X_train, y_train)
    predict_rf = model_rf.predict(X_test)
    recall_rf = recall_score(y_test, predict_rf)
    precision_rf = precision_score(y_test, predict_rf)
    acc_rf = accuracy_score(y_test, predict_rf)
    #print("Random Forest Accuracy:",acc_rf)

    # Compare Features of RF model.
    feature_importances = model_rf.feature_importances_
    features = X_train.columns
    df = pd.DataFrame({'features': features, 'importance': feature_importances})
    df = df.sort_values(by=["importance"],ascending=False)
    




    fighters ={}
    for index, row in data.iterrows():
        if row['R_fighter'] not in fighters:
            fighters[row['R_fighter']] = [0,1 if row['gender']=='MALE' else 2, row['R_current_lose_streak'], row['R_current_win_streak'],
            row['R_longest_win_streak'], row['R_wins'], row['R_losses'], row['R_total_rounds_fought'], 
            row['R_win_by_KO/TKO'], row['R_win_by_Submission'], row['R_Height_cms'], row['R_Reach_cms'],
            row['R_age'], row['R_avg_SUB_ATT'], row['R_avg_TD_landed']]
        if row['B_fighter'] not in fighters:
            fighters[row['B_fighter']] = [0,1 if row['gender']=='MALE' else 2, row['B_current_lose_streak'], row['B_current_win_streak'],
            row['B_longest_win_streak'], row['B_wins'], row['B_losses'], row['B_total_rounds_fought'], 
            row['B_win_by_KO/TKO'], row['B_win_by_Submission'], row['B_Height_cms'], row['B_Reach_cms'],
            row['B_age'], row['B_avg_SUB_ATT'], row['B_avg_TD_landed']]
    import numpy as np
    data = request.json
    user_input1 = str(data.get('userInput1'))
    user_input2 = str(data.get('userInput2'))
    odds = float(data.get('odds'))
    arr2 = np.array(fighters[user_input2])
    arr1 = np.array(fighters[user_input1])

    data_array = np.subtract(arr2, arr1)
    data_array[0] = odds
    # Add more variables as needed
    #print("Using the Random Forest model, we can predict that the Red_Fighter will win, with a win probability of",model_rf.predict_proba([data_array])[:,1])
    response_data = {'result':"Using the model, we can predict that {} will win with a probability of {}".format(user_input1, model_rf.predict_proba([data_array])[:,1])}

    return jsonify(response_data)



if __name__ == "__main__":
    app.run(debug=True)
