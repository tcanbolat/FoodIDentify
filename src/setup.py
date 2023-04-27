import os
from collections import defaultdict
from common.common import food_list
from shutil import copy

def setup_training_data(txtfile, source, destination, foods):
    food_types = defaultdict(list)
    with open(txtfile, "r") as file:
        lines = [line.strip() for line in file.readlines()]
        for l in lines:
            food_type = l.split("/")
            if food_type[0] in foods:
                food_types[food_type[0]].append(food_type[1] + ".jpg")

    for food in food_types.keys():
        print("  " + food, end="  ")
        if not os.path.exists(os.path.join(destination, food)):
            os.makedirs(os.path.join(destination, food))
        for n in food_types[food]:
            copy(os.path.join(source, food, n), os.path.join(destination, food, n))

setup_training_data('meta/train.txt', 'meta/images', 'meta/training-data/train', food_list)
setup_training_data('meta/test.txt', 'meta/images', 'meta/training-data/test', food_list)
