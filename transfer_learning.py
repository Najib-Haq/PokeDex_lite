import tensorflow as tf
import matplotlib.pyplot as plt

IMG_SIZE = 160
LEARNING_RATE = 0.001
EPOCHS = 10

class CNN:
    def __init__(self, data, num_classes, image_size = IMG_SIZE, learning_rate = LEARNING_RATE,
                 optimizer = tf.keras.optimizers.RMSprop, loss_function = 'binary_crossentropy',
                 epochs = EPOCHS, fine_tune = False, fine_tune_node = 0):
        self.image_size = image_size
        self.image_shape = (image_size, image_size, 3)
        self.base_model = tf.keras.applications.MobileNetV2(
            input_shape = self.image_shape,
            include_top = False, # that means doesn't include the topmost(output) classification layer
            weights = 'imagenet' # weights trained under imagenet dataset
        )
        self.data = data
        self.num_classes = num_classes
        self.learning_rate = learning_rate
        self.optimizer = optimizer
        self.loss_function = loss_function
        self.epochs = epochs
        self.model = 0
        self.history = 0
        self.fine_tune = fine_tune
        self.fine_tune_node = fine_tune_node # node from which trainable nodes will be

    def build_layer(self, image_batch):
        # result shape (batch , 5,5,1280)
        feature_batch = self.base_model(image_batch)  # get the topmost layer available to you
        self.base_model.trainable = False

        # convert this layer to a flattened layer by pooling
        global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
        # result shape (batch ,1280)
        feature_batch_average = global_average_layer(feature_batch)

        prediction_layer = tf.keras.layers.Dense(self.num_classes)
        # result shape (batch ,num_classes)
        prediction_batch = prediction_layer(feature_batch_average)

        # putting it together
        self.model = tf.keras.Sequential([
            self.base_model,
            global_average_layer,
            prediction_layer
        ])



    def feature_extraction(self, image_batch):
        self.build_layer(image_batch)

        #compile
        self.model.compile(optimizer = self.optimizer(lr = self.learning_rate),
                           loss = self.loss_function,
                           metrics = ['accuracy']
                           )


    def fine_tune(self, image_batch):
        self.build_layer(image_batch)
        self.base_model.trainable = True

        for layer in self.base_model.layers[:self.fine_tune_node]:
            layer.trainable = False

        self.model.compile(optimizer = self.optimizer(lr = self.learning_rate),
                           loss = self.loss_function,
                           metrics = ['accuracy']
                           )


    def plot(self):
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
        plt.ylim([min(plt.ylim()), 1])
        plt.title('Training and Validation Accuracy')

        plt.subplot(2, 1, 2)
        plt.plot(loss, label='Training Loss')
        plt.plot(val_loss, label='Validation Loss')
        plt.legend(loc='upper right')
        plt.ylabel('Cross Entropy')
        plt.ylim([0, 1.0])
        plt.title('Training and Validation Loss')
        plt.xlabel('epoch')
        plt.savefig("Plots/plot.png")
        plt.show()


    def train(self, train_batches, validation_batches, plot = False, fine_tune_epochs = 10):
        image_batch = train_batches[0]  # TODO: find out for sure
        if not self.fine_tune:
            self.feature_extraction(image_batch)
            self.history = self.model.fit(train_batches,
                                          epochs = self.epochs,
                                          validation_data = validation_batches)

        else:
            self.fine_tune(image_batch)
            total_epochs = self.epochs + fine_tune_epochs
            self.history = self.model.fit(train_batches,
                                          epochs = total_epochs,
                                          initial_epoch = self.epochs,
                                          validation_data = validation_batches)


        if not plot:
            self.plot()



if __name__ == '__main__':
    cnn = CNN([1,2,3],2)
















