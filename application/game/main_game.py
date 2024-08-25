import random

player_1_score = 0
player_2_score = 0
def main_games():
    global player_2_score
    global player_1_score
    score_card_22 = [2,3,4,5,6,7,8,9,10,11,12,13,14]
    player_1_card = random.choice(score_card_22)
    player_2_card = random.choice(score_card_22)
    player_1_score += player_1_card
    player_2_score += player_2_card
    return player_1_score, player_2_score
player_1_score , player_2_score = main_games()
    
        


