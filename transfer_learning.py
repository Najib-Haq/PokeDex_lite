import tensorflow as tf
import matplotlib.pyplot as plt
import os


IMG_SIZE = 160
LEARNING_RATE = 0.001
EPOCHS = 10
TRAINING_STEPS = 1000
VALIDATION_STEPS = 10
LOSS_FUNCTION = 'binary_crossentropy'
#TODO: if input is numpy array then validation_split paramter is available in model.fit()

class CNN:
    def __init__(self, num_classes, image_size = IMG_SIZE, learning_rate = LEARNING_RATE,
                 optimizer = tf.keras.optimizers.RMSprop, loss_function = 'categorical_crossentropy',
                 epochs = EPOCHS, training_steps = TRAINING_STEPS, validation_steps = VALIDATION_STEPS,
                 fine_tune = False, fine_tune_node = 0):
        '''
        :param num_classes: number of classes
        :param image_size: size of image
        :param learning_rate: learning rate
        :param optimizer: optimization function
        :param loss_function: loss function
        :param epochs: how many times will training iterate over the entire dataset
        :param training_steps: ( total_data / batch_size )
        :param validation_steps: number of batches to run validation on
        :param fine_tune: if you want to fine tune set to True
        :param fine_tune_node: from which numbered node will parameters be trainable
        '''
        self.image_size = image_size
        self.image_shape = (image_size, image_size, 3)
        self.base_model = tf.keras.applications.MobileNetV2(
            input_shape = self.image_shape,
            include_top = False, # that means doesn't include the topmost(output) classification layer
            weights = 'imagenet' # weights trained under imagenet dataset
        )
        #self.data = data
        self.num_classes = num_classes
        self.learning_rate = learning_rate
        self.optimizer = optimizer
        self.loss_function = loss_function
        self.epochs = epochs # how many times will training iterate over the entire dataset
        self.training_steps = training_steps # ( total_data / batch_size )
        self.validation_steps = validation_steps # number of batches to run validation on
        self.history = 0
        self.fine_tune = fine_tune
        self.fine_tune_node = fine_tune_node # node from which trainable nodes will be
        self.checkpoint_path = "training/cp.ckpt"
        self.checkpoint_dir = os.path.dirname(self.checkpoint_path)
        self.model = 0


    def build_layer(self, image_batch):
        # result shape (batch , 5,5,1280)
        feature_batch = self.base_model(image_batch)  # get the topmost layer available to you
        self.base_model.trainable = False

        # convert this layer to a flattened layer by pooling
        global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
        # result shape (batch ,1280)
        feature_batch_average = global_average_layer(feature_batch)

        prediction_layer = tf.keras.layers.Dense(self.num_classes, activation = tf.keras.activations.softmax)
        # result shape (batch ,num_classes)
        prediction_batch = prediction_layer(feature_batch_average)

        # putting it together
        self.model = tf.keras.Sequential([
            self.base_model,
            global_average_layer,
            prediction_layer
        ])



    def feature_extraction(self, image_batch):
        '''
        build feature extraction model
        :param image_batch: for input shape (as placeholder)
        :return:
        '''
        self.build_layer(image_batch)

        #compile
        self.model.compile(optimizer = self.optimizer(lr = self.learning_rate),
                           loss = self.loss_function,
                           metrics = ['accuracy']
                           )


    def fine_tuning(self, image_batch):
        '''
        builds fine tune model
        :param image_batch: for size of input (placeholder)
        :return:
        '''
        self.build_layer(image_batch)
        self.base_model.trainable = True

        for layer in self.base_model.layers[:self.fine_tune_node]:
            layer.trainable = False

        self.model.compile(optimizer = self.optimizer(lr = self.learning_rate),
                           loss = self.loss_function,
                           metrics = ['accuracy']
                           )


    def plot(self):
        '''
        plots accuracy and loss graphs
        :return:
        '''
        acc = self.history.history['accuracy']
        val_acc = self.history.history['val_accuracy']

        loss = self.history.history['loss']
        val_loss = self.history.history['val_loss']

        plt.figure(figsize=(8, 8))
        plt.subplot(2, 1, 1)
        plt.plot(acc, label='Training Accuracy')
        plt.plot(val_acc, label='Validation Accuracy')
        plt.legend(loc='lower right')
        plt.ylabel('Accuracy')
        plt.ylim([min(plt.ylim()), 1.2])
        plt.title('Training and Validation Accuracy')

        plt.subplot(2, 1, 2)
        plt.plot(loss, label='Training Loss')
        plt.plot(val_loss, label='Validation Loss')
        plt.legend(loc='upper right')
        plt.ylabel('Cross Entropy')
        plt.ylim([0, 1.2])
        plt.title('Training and Validation Loss')
        plt.xlabel('epoch')
        plt.savefig("Plots/plot.png")
        plt.show()


    def train(self, train_batches, validation_batches, plot = True, fine_tune_epochs = 10):
        '''
        trains the model
        :param train_batches: td.data.dataset object
        :param validation_batches: td.data.dataset object
        :param plot: set to True if want plot
        :param fine_tune_epochs: if fine tune is used this parameter must be given
        :return:
        '''
        for image_batch, label_batch in train_batches.take(1):
            pass


        # Create a callback that saves the model's weights
        cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=self.checkpoint_path,
                                                         save_weights_only=True,
                                                         verbose=1)

        if not self.fine_tune:
            self.feature_extraction(image_batch)
            self.history = self.model.fit(train_batches,
                                          epochs = self.epochs,
                                          validation_data = validation_batches,
                                          callbacks = [cp_callback], #TODO : check why not working (but works now)
                                          steps_per_epoch = self.training_steps,
                                          validation_steps = self.validation_steps) # run validation on this number of batches

        else:
            self.fine_tuning(image_batch)
            total_epochs = self.epochs + fine_tune_epochs
            self.history = self.model.fit(train_batches,
                                          epochs = total_epochs,
                                          initial_epoch = self.epochs,
                                          validation_data = validation_batches,
                                          callbacks=[cp_callback],
                                          steps_per_epoch= self.training_steps, # how many training steps in a single epoch
                                          validation_steps=self.validation_steps)


        if plot:
            self.plot()



    def reuse_model(self, img):
        '''
        to reinitialize model from checkpoint path
        :param img: for input shape (as placeholder) run Data.process_path() on an input image and
         pass to this parameter
        :return:
        '''
        if not self.fine_tune:
            self.feature_extraction(img)
        else:
            self.fine_tune(img)
        self.model.load_weights(self.checkpoint_path)





if __name__ == '__main__':
    cnn = CNN([1,2,3],2)
















