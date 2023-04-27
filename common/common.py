import datetime
import glob
import matplotlib.pyplot as plt
import numpy as np
import os

######################################################################

# GET THE LATEST MODEL OR MODEL HISTORY FROM THE MODEL DIRECTORY

def get_latest_file(extension, directory_path):
    if extension == 'model':
        extension = '*.h5'
    elif extension == 'history':
        extension = '*.npy'
    else:
        return ''

    file_list = glob.glob(os.path.join(directory_path, extension))
    return max(file_list, key=os.path.getctime) if file_list else ''

######################################################################

# TIME STAMP FUNCTION TO GIVE MODEL WEIGHT UNIQUE FILE NAME IN ModelCheckpoint CALLBACK

def time_stamp():
    return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


######################################################################

# CONVERTS CLASSES.TXT INTO A LIST

def txt_to_list(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        lst = [line.strip() for line in lines]
        print(lst)
    return lst


######################################################################

# LIST CREATED FROM classes.txt USING txt_to_list(../meta/classes.txt)

food_list = [
    'apple_pie', 'baby_back_ribs', 'baklava', 'beef_carpaccio', 'beef_tartare', 'beet_salad', 'beignets',
    'bibimbap', 'bread_pudding', 'breakfast_burrito', 'bruschetta', 'caesar_salad', 'cannoli', 'caprese_salad',
    'carrot_cake', 'ceviche', 'cheesecake', 'cheese_plate', 'chicken_curry', 'chicken_quesadilla', 'chicken_wings',
    'chocolate_cake', 'chocolate_mousse', 'churros', 'clam_chowder', 'club_sandwich', 'crab_cakes', 'creme_brulee',
    'croque_madame', 'cup_cakes', 'deviled_eggs', 'donuts', 'dumplings', 'edamame', 'eggs_benedict', 'escargots',
    'falafel', 'filet_mignon', 'fish_and_chips', 'foie_gras', 'french_fries', 'french_onion_soup', 'french_toast',
    'fried_calamari', 'fried_rice', 'frozen_yogurt', 'garlic_bread', 'gnocchi', 'greek_salad', 'grilled_cheese_sandwich',
    'grilled_salmon', 'guacamole', 'gyoza', 'hamburger', 'hot_and_sour_soup', 'hot_dog', 'huevos_rancheros', 'hummus',
    'ice_cream', 'lasagna', 'lobster_bisque', 'lobster_roll_sandwich', 'macaroni_and_cheese', 'macarons', 'miso_soup',
    'mussels', 'nachos', 'omelette', 'onion_rings', 'oysters', 'pad_thai', 'paella', 'pancakes', 'panna_cotta',
    'peking_duck', 'pho', 'pizza', 'pork_chop', 'poutine', 'prime_rib', 'pulled_pork_sandwich', 'ramen', 'ravioli',
    'red_velvet_cake', 'risotto', 'samosa', 'sashimi', 'scallops', 'seaweed_salad', 'shrimp_and_grits',
    'spaghetti_bolognese', 'spaghetti_carbonara', 'spring_rolls', 'steak', 'strawberry_shortcake', 'sushi', 'tacos',
    'takoyaki', 'tiramisu', 'tuna_tartare', 'waffles'
]


######################################################################

# PLOT HISTORY OF TEST AND VALIDATION ACCURACY / LOSS

def plot_model_history(epochs):

    file = get_latest_file('history', '../model')

    history = np.load(file, allow_pickle='TRUE').item()
    auc = history['auc']
    val_auc = history['val_auc']

    loss = history['loss']
    val_loss = history['val_loss']

    epochs_range = range(epochs)

    plt.figure(figsize=(8, 8))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, auc, label='Training Accuracy')
    plt.plot(epochs_range, val_auc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.savefig('./graph.png')
    plt.show()
