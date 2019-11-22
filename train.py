import transfer_learning as tl
import dataset_prep as dp

data_dir = 'E:\Projects\Side_projects\PokeDex_lite\Dataset'
validation_dir = 'E:\Projects\Side_projects\PokeDex_lite\Validation'

################ image augmentation ? #################################
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
####################################################################


# get data in Dataset folder
data = dp.Data(
    data_dir,
    batch_size=32,
    image_height=160,
    image_width=160
)

# augment data
# ia.augment_images('Dataset', class_names=data.class_names, num_files_desired=100)

data.image_generator_tf()

# get data in Validation folder
validation = dp.Data(
    validation_dir,
    batch_size=5,
    image_width=160,
    image_height=160
)

# augment data
# ia.augment_images('Validation', class_names=validation.class_names, num_files_desired=10)

validation.image_generator_tf()

# build model object
model = tl.CNN(
    num_classes=len(data.class_names),
    image_size=160,
    learning_rate=0.0001,
    training_steps=(data.image_count/data.batch_size),
    validation_steps=(validation.image_count/validation.batch_size),
    epochs=50
)

# train
model.train(data.data_gen, validation.data_gen)#, fine_tune_epochs=10)

print("Training ended.")







