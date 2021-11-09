import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor

linear_regressor = LinearRegression() 
log_regressor = LogisticRegression() 
random_tree = model =  RandomForestRegressor(n_estimators=15, max_features=2)

linear_data = []
log_data = []
tree_data = []
real_data = []
overall = []

def prepare_models():
    dataset = pd.read_csv('result_with_score.csv')
    dataset['Result'] = dataset['Result'].astype(int)
    dataset['Is_Chest_Taken'] = dataset['Is_Chest_Taken'].astype(int)
    x = dataset[['Health', 'Time']].values
    y = dataset['Score'].values
    linear_regressor.fit(x, y)

    x = (np.asarray(dataset['Score'])).reshape(-1, 1)
    y = (np.asarray(dataset['Result'])).ravel()
    log_regressor.fit(x, y)

    x = dataset[['Time', 'Score', 'Is_Chest_Taken']].values
    y = dataset['Result'].values
    random_tree.fit(x, y)

def predict_score_health_time(health, time):
    return linear_regressor.predict([[health, time]])[0]

def predict_result_score(score):
    inp = np.array([score])
    return log_regressor.predict(inp.reshape(-1, 1))[0]

def predict_result_health_time_score_isTaken(health, time, score, is_chest_taken):
    return random_tree.predict([[time, score, is_chest_taken]])[0]

def write_result(Result, Health, Time, Score, is_chest_taken):
    linear_data.append([Result, Health, is_chest_taken, Time, predict_score_health_time(Health, Time)])
    log_data.append([predict_result_score(Score) , Health, is_chest_taken, Time, Score])
    tree_data.append([predict_result_health_time_score_isTaken(Health, Time, Score, is_chest_taken) , Health, is_chest_taken, Time, Score])
    real_data.append([Result , Health, is_chest_taken, Time, Score])
    overall.append([int(Result), tree_data[-1][0], log_data[-1][0], Health, is_chest_taken, Time, Score, linear_data[-1][4]])

def save_result():
    df = pd.DataFrame(overall,columns=['is_won','is_won(forest prediction)','is_won(logistic prediction)', 'player_health', 'is_chest_taken', 'game_time', 'score', 'score(linear prediction)'])
    df.to_csv('Random_prediction_results.csv', header=False)

    

def get_result_errors_count(calculated, real):
    count = 0
    for i in range(len(calculated)):
        if calculated[i][0] != real[i][0]:
            count += 1
    return count 

def calculate_mean_error(calculated, real):
    errors = []
    for i in range(len(calculated)):
        errors.append(abs(real[i][4] - calculated[i][4]))
    return sum(errors) / len(errors) 

def show_efficiency():
    print('---------------------------------------------------')
    log_efficiency = (len(log_data) - get_result_errors_count(log_data, real_data))/len(log_data)
    print("logistic result prediction efficiency:" + str(log_efficiency * 100) + '%')

    tree_efficiency = (len(tree_data) - get_result_errors_count(tree_data, real_data))/len(tree_data)
    print("random forest result prediction efficiency:" + str(tree_efficiency * 100) + '%')

    linear_error = calculate_mean_error(linear_data, real_data)
    print("linear score prediction error:" + str(linear_error))
    print('---------------------------------------------------')
    
