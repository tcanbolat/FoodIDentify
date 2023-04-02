from collections import defaultdict
from shutil import copy, copytree, rmtree
import os

def txt_to_list(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        lst = [line.strip() for line in lines]
    return lst

def setup_training_data(txtfile, source, destination, food_list=['cheesecake', 'baklava', 'ramen']):
    # food list defaults to cheesecake, baklava, and ramen if not indicated
    food_types = defaultdict(list)
    with open(txtfile, "r") as file:
        lines = [line.strip() for line in file.readlines()]
        for l in lines:
            food_type = l.split("/")
            if food_type[0] in food_list:
                food_types[food_type[0]].append(food_type[1] + ".jpg")

    for food in food_types.keys():
        print("  " + food, end="  ")
        if not os.path.exists(os.path.join(destination, food)):
            os.makedirs(os.path.join(destination, food))
        for n in food_types[food]:
            copy(os.path.join(source, food, n), os.path.join(destination, food, n))


setup_training_data('meta/train.txt', 'meta/images', 'training-data/train', txt_to_list('meta/classes.txt'))
setup_training_data('meta/test.txt', 'meta/images', 'training-data/test', txt_to_list('meta/classes.txt'))
