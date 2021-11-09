from config import *
from game import *
import time
import pandas as pd

games_count = 100
data = []
while games_count >= 0:
    start_time = time.time()
    game = Game()
    is_won, player_health, is_chest_taken = game.run()
    algo = "expectimax"
    game_time = time.time() - start_time
    games_count -= 1
    data.append([is_won , player_health, is_chest_taken, algo, game_time, game.score.score])

df = pd.DataFrame(data,columns=['is_won', 'player_health', 'is_chest_taken', 'algorithm', 'game_time', 'score'])
df.to_csv('result_with_score.csv', mode='a', header=False)