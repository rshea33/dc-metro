# DC Metro Board
import time

from config import config
from train_board import TrainBoard
from metro_api import MetroApi, MetroApiOnFireException

STATION_CODE = config['metro_station_code']
TRAIN_GROUP = config['train_group']
REFRESH_INTERVAL = config['refresh_interval']
ALTERNATING_TRAINS = TRAIN_GROUP == '0'
CURRENT_TRAIN_GROUP = '1'

def refresh_trains() -> [dict]:
    global CURRENT_TRAIN_GROUP
    group = CURRENT_TRAIN_GROUP if ALTERNATING_TRAINS else TRAIN_GROUP
    try:
        trains = MetroApi.fetch_train_predictions(STATION_CODE, group)
    except MetroApiOnFireException:
        print('WMATA Api is currently on fire. Trying again later ...')
        return None
    if ALTERNATING_TRAINS:
        CURRENT_TRAIN_GROUP = '2' if CURRENT_TRAIN_GROUP == '1' else '1'
    return trains

train_board = TrainBoard(refresh_trains)

while True:
	train_board.refresh()
	time.sleep(REFRESH_INTERVAL)
