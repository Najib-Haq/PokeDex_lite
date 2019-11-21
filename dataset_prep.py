import pathlib
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from PIL import Image
import os


AUTOTUNE = tf.data.experimental.AUTOTUNE
BATCH_SIZE = 6
IMG_HEIGHT = 160
IMG_WIDTH = 160
dir = 'E:\Projects\Side_projects\PokeDex_lite\Dataset'

def augmentation(x, y, HEIGHT=160, WIDTH=160, NUM_CHANNELS=3):
    x = tf.image.resize_with_crop_or_pad(
        x, HEIGHT + 8, WIDTH + 8)
    x = tf.image.random_crop(x, [HEIGHT, WIDTH, NUM_CHANNELS])
    x = tf.image.random_flip_left_right(x)
    return x, y


class Data:
    def __init__(self, dir=dir, batch_size = BATCH_SIZE, image_height = IMG_HEIGHT, image_width = IMG_WIDTH):
        self.data_dir = pathlib.Path(dir)
        self.image_count = len(list(self.data_dir.glob('*/*')))
        self.class_names = np.array([item.name for item in self.data_dir.glob('*')])
        self.batch_size = batch_size
        self.image_height = image_height
        self.image_width = image_width
        self.STEPS_PER_EPOCH = np.ceil(self.image_count / self.batch_size)
        self.data_gen = 0
        self.is_keras = False


    def check_class(self, class_name, no_of_data = 3):
        '''
        shows data from the class_name class
        :param class_name:  name of class whose data you want to view
        :param no_of_data:  no of data of class_name to view
        :return:
        '''
        if class_name not in self.class_names:
            print("Given class names couldn't be found. Please check class_names variable for valid classes")
            return
        class_name_data = list(self.data_dir.glob(class_name+'/*'))
        for image_path in class_name_data[:no_of_data]:
            img = Image.open(image_path)
            plt.imshow(img)
            plt.show()


    def show_batch(self,image_batch, label_batch, n_row, n_col, no_of_images):
        '''
        plots no_of_images images from image_batch and label_batch
        :param image_batch: batch of images to plot
        :param label_batch: batch of labels corresponding to image_batch
        :param n_row: row_number of subplot
        :param n_col: col_number of subplot
        :param no_of_images: how many images to plot
        :return:
        '''
        print(len(image_batch))
        plt.figure(figsize=(10, 10))
        for n in range(no_of_images):
            ax = plt.subplot(n_row, n_col, n + 1)
            plt.imshow(image_batch[n])
            plt.title(self.class_names[label_batch[n] == 1][0].title())
            plt.axis('off')
        plt.show()


    def image_generator_keras(self):
        '''
        preprocess all image data according to paramters given in constructor and creates a generator
        :return: a data generator from the data
        '''
        self.is_keras = True
        image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale = 1./255)
        self.data_gen = image_generator.flow_from_directory(directory=str(self.data_dir),
                                                             batch_size=self.batch_size,
                                                             shuffle=True,
                                                             target_size=(self.image_height, self.image_height),
                                                             classes = list(self.class_names))
        return self.data_gen



    ########################## CODE FOR TF.DATA #############################################
    def get_label(self,file_path):
        '''
        :param file_path: the file whose label is returned
        :return: label of file in file_path
        '''
        # convert the path to a list of path components
        parts = tf.strings.split(file_path, os.path.sep)
        # The second to last is the class-directory
        return parts[-2] == self.class_names


    def decode_img(self,img):
        '''
        :param img: image to be decoded
        :return: decoded image with specific shape
        '''
        # convert the compressed string to a 3D uint8 tensor
        img = tf.image.decode_jpeg(img, channels=3)
        # Use `convert_image_dtype` to convert to floats in the [0,1] range.
        img = tf.image.convert_image_dtype(img, tf.float32)
        # resize the image to the desired size.
        return tf.image.resize(img, [self.image_width, self.image_height])


    def process_path(self,file_path):
        '''
        :param file_path: file_path of file to be processed
        :return: returns image and label of file in file_path
        '''
        label = self.get_label(file_path)
        # load the raw data from the file as a string
        img = tf.io.read_file(file_path)
        img = self.decode_img(img)
        return img, label



    def prepare_for_training(self, ds, cache=True, shuffle_buffer_size=1000):
        # This is a small dataset, only load it once, and keep it in memory.
        # use `.cache(filename)` to cache preprocessing work for datasets that don't
        # fit in memory.
        if cache:
            if isinstance(cache, str):
                ds = ds.cache(cache)
            else:
                ds = ds.cache()

        ds = ds.shuffle(buffer_size=shuffle_buffer_size)

        # Repeat forever
        ds = ds.repeat()

        ds = ds.batch(BATCH_SIZE)

        # `prefetch` lets the dataset fetch batches in the background while the model
        # is training.
        ds = ds.prefetch(buffer_size=AUTOTUNE)

        return ds


    def image_generator_tf(self):
        '''
        preprocesses all image data according to paramters given in constructor and creates a generator
        :return: the generator (not exactly a generator use iter to generate)
        '''
        self.is_keras = False
        list_ds = tf.data.Dataset.list_files(str(self.data_dir / '*/*'))
        print("Some random files found in directory : ")
        for f in list_ds.take(5):
            print(f.numpy())

        # preprocesses the data
        labeled_ds = list_ds.map(self.process_path, num_parallel_calls=AUTOTUNE)

        # checking labeled_ds
        # for image, label in labeled_ds:
        #     print(label)
        #
        # print(labeled_ds)
        # for image, label in labeled_ds.take(1):
        #     print("Image shape: ", image.numpy().shape)
        #     print("Label: ", label.numpy())

        self.data_gen = self.prepare_for_training(labeled_ds)
        return self.data_gen



    def plot_batch_data(self, n_row, n_col, no_of_images):
        '''
        :param n_row: row_number of subplot
        :param n_col: col_number of subplot
        :param no_of_images: how many images to plot
        :return:
        '''
        if self.is_keras:
            image_batch, label_batch = next(self.data_gen)
        else:
            image_batch, label_batch = next(iter(self.data_gen))
            image_batch = image_batch.numpy()
            label_batch = label_batch.numpy()

        self.show_batch(image_batch, label_batch, n_row, n_col, no_of_images)
        #self.show_batch(image_batch.numpy(), label_batch.numpy(), n_row, n_col, no_of_images)




if __name__ == '__main__':
    d = Data(dir)
    d.image_generator_keras()
    d.plot_batch_data(3,2,d.batch_size)

    d.image_generator_tf()
    d.plot_batch_data(3, 2, d.batch_size)


















