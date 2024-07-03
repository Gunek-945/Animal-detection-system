# Augmentation

import os
from tensorflow import keras
from keras._tf_keras.keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

original_data_dir = 'ENTER DIRECTORY PATH WHERE IMAGES ARE STORED'

datagen = ImageDataGenerator(
        #Differnet parameters for augmentation
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest')

for filename in os.listdir(original_data_dir):
    # Load the image
    image_path = os.path.join(original_data_dir, filename)
    img = load_img(image_path)  # this is a PIL image
    x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
    x = x.reshape((1,) + x.shape)  # this is a Numpy array with shape (1, 3, 150, 150)

# the .flow() command below generates batches of randomly transformed images
# and saves the results to the `preview/` directory
    i = 0
    for batch in datagen.flow(x, batch_size=1, save_to_dir='ENTER DIRECTORY WHERE YOU WANT TO SAVE THE ANNOTATED IMAGES', save_prefix='aug', save_format='jpeg'):
        i += 1
        if i > 7:
            break  # otherwise the generator would loop indefinitely


        # Do nothing for the other images
        pass

print("Image conversion complete.")
