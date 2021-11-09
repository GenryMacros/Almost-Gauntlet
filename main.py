from config import *
from game import *
import time
import pandas as pd
from predictor import *

games_count = 50
data = []
prepare_models()
while games_count >= 0:
    start_time = time.time()
    game = Game()
    is_won, player_health, is_chest_taken = game.run()
    game_time = time.time() - start_time
    games_count -= 1
    write_result(is_won, player_health, game_time, game.score.score, is_chest_taken)

save_result()
show_efficiency()