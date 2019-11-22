import transfer_learning as tl
import dataset_prep as dp
import tensorflow as tf
import os

data_dir = 'E:\Projects\Side_projects\PokeDex_lite\Dataset'

def class_name_index(prediction_array):
    prediction = prediction_array[0] # as 2d array
    return prediction.argmax()


def prep_data(data_dir = data_dir):
    data = dp.Data(
        data_dir,
        batch_size=64,
        image_height=160,
        image_width=160
    )
    model = tl.CNN(len(data.class_names))
    img, label = data.process_path('E:\Projects\Side_projects\PokeDex_lite\Dataset\Pikachu\\1.png')
    img = tf.reshape(img, [1, 160, 160, 3])
    model.reuse_model(img)

    return data, model





def predict(data, model, no_of_predictions = 10, show_prediction_data = True):
    count = 0
    while count<no_of_predictions:
        path = input("Please input path to image or -1 to stop : ")
        if path == '-1':
            break
        try:
            img, label = data.process_path(path)
        except Exception as e:
            print(path)
            print("Invalid path. Please enter again.")
            print(e)
            continue
        img = tf.reshape(img,[1,160,160,3])
        ans = model.model.predict(img)
        if show_prediction_data:
            print('Model Prediction : ', ans)
            print('True label : ', label)
        print('=====>')
        print('Label is : '+data.class_names[class_name_index(ans)])
        print('#################################################################')
        count += 1


def predict_dir(data, model, dir_name):
    try:
        images = [os.path.join(dir_name, f) for f in os.listdir(dir_name) if
                  os.path.isfile(os.path.join(dir_name, f))]
    except:
        print("Invalid path. Please enter again.")
        return
    count = 0
    correct = 0
    for image_path in images:
        img, label = data.process_path(image_path)
        img = tf.reshape(img, [1, 160, 160, 3])
        ans = model.model.predict(img)
        print('File is : '+str(image_path.split('\\')[-1]))
        print('Label is : ' + data.class_names[class_name_index(ans)])
        print('#####################################################')
        if image_path.split('\\')[-2] ==  data.class_names[class_name_index(ans)]:
            correct += 1
        count += 1
    print('Correction percentage is : '+str(correct/count))








if __name__ == '__main__':
    data, model = prep_data(data_dir)
    while True:
        n = input('Press 1 for single prediction, 2 for directory prediction, -1 to exit : ')
        if n == '1':
            predict(data = data, model = model, no_of_predictions=100)
        elif n == '2':
            dir = input('Input Directory : ')
            predict_dir(data = data, model = model, dir_name=dir)
        elif n == '-1':
            break


    # blastoise and sceptile not working







