from scipy import ndarray
import skimage as sk
from skimage import transform
from skimage import util
import random
import os
from PIL import Image
import numpy as np

dir = 'Validation'

class_names = ['Charizard', 'Pikachu']

def random_rotation(image_array: ndarray):
    # pick a random degree of rotation between 25% on the left and 25% on the right
    random_degree = random.uniform(-45, 45)
    return sk.transform.rotate(image_array, random_degree)

def random_noise(image_array: ndarray):
    # add random noise to the image
    return sk.util.random_noise(image_array)

def horizontal_flip(image_array: ndarray):
    # horizontal flip doesn't need skimage, it's easy as flipping the image array of pixels !
    return image_array[:, ::-1]



def augment_images(dir = dir, class_names = class_names, num_files_desired = 100):
    '''
    augments images
    :param dir: directory or path of images
    :param class_names: class names
    :param num_files_desired: number of imaged to be generated per class
    :return:
    '''
    # dictionary of the transformations functions we defined earlier
    available_transformations = {
    'rotate': random_rotation,
    'noise': random_noise,
    'horizontal_flip': horizontal_flip
    }

    folder_paths = []
    for cn in class_names:
        folder_paths.append(dir+'\\'+cn)


    for folder_path in folder_paths:
        # loop on all files of the folder and build a list of files paths
        images = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]


        num_generated_files = 0
        while num_generated_files <= num_files_desired:
            print(num_generated_files)
            # random image from the folder
            image_path = random.choice(images)
            # read image as an two dimensional array of pixels
            image_to_transform = np.array(Image.open(image_path))


            # random num of transformations to apply
            num_transformations_to_apply = random.randint(1, len(available_transformations))

            num_transformations = 0
            transformed_image = None
            while num_transformations <= num_transformations_to_apply and num_generated_files <= num_files_desired:
                # choose a random transformation to apply for a single image
                key = random.choice(list(available_transformations))
                transformed_image = available_transformations[key](image_to_transform)
                sk.io.imsave(folder_path+'\\'+str(num_generated_files)+'.png', transformed_image)
                num_transformations += 1
                num_generated_files += 1