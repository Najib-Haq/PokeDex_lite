import transfer_learning as tl
import dataset_prep as dp
import tensorflow as tf
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
data_dir = 'E:\Projects\Side_projects\PokeDex_lite\Dataset'
validation_dir = 'E:\Projects\Side_projects\PokeDex_lite\Validation'





data = dp.Data(
    data_dir,
    batch_size=4,
    image_height=160,
    image_width=160
)

data.image_generator_tf()
data.plot_batch_data(3,2,6)
################ image augmentation ? ###################
# print("Hoise")
#
# data.data_gen = (
#     data.data_gen.take(1).map(lambda image, label: (tf.image.random_flip_left_right(image), label)).repeat(5))
# print("Hoise2")
# images = [image[0] for image in data.data_gen]
#
# for i in range(len(images)):
#
#     for j in range(len(images[i])):
#         plt.figure()
#         print(images[i])
#         plt.imshow(images[i][1])
#     plt.show()
#
#
# validation = dp.Data(
#     validation_dir,
#     batch_size=2,
#     image_width=160,
#     image_height=160
# )
#
# validation.image_generator_tf()
#
# model = tl.CNN(
#     num_classes=len(data.class_names),
#     image_size=160,
#     learning_rate=0.0001,
#     training_steps=(data.image_count/data.batch_size),
#     validation_steps=(validation.image_count/validation.batch_size),
#     epochs=50
# )
#
# img, label = data.process_path('E:\Projects\Side_projects\PokeDex_lite\Validation\Charizard\img2.png')
# print(img)
# print(label)
# #model = tl.CNN(2)
# model.train(data.data_gen, validation.data_gen)#, fine_tune_epochs=10)


#
# img = tf.reshape(img,[1,160,160,3])
# #model.reuse_model(img)
# #model.model.summary()
# ans = model.model.predict(img)
# print(ans)
# print(label)


