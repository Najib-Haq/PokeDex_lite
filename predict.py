import transfer_learning as tl
import dataset_prep as dp
import tensorflow as tf

data_dir = 'E:\Projects\Side_projects\PokeDex_lite\Dataset'

def class_name_index(prediction_array):
    prediction = prediction_array[0] # as 2d array
    return prediction.argmax()


def predict(data_dir = data_dir, no_of_predictions = 10, show_prediction_data = True):
    count = 0
    data = dp.Data(
        data_dir,
        batch_size=32,
        image_height=160,
        image_width=160
    )
    model = tl.CNN(2)
    while count<no_of_predictions:
        path = input("Please input path to image or -1 to stop : ")
        if path == '-1':
            break
        try:
            img, label = data.process_path(path)
        except:
            print("Invalid path. Please enter again.")
            continue
        img = tf.reshape(img,[1,160,160,3])
        if count==0:
            model.reuse_model(img)
        ans = model.model.predict(img)
        if show_prediction_data:
            print('Model Prediction : ', ans)
            print('True label : ', label)
        print('=====>')
        print('Label is : '+data.class_names[class_name_index(ans)])
        print('#################################################################')
        count += 1

if __name__ == '__main__':
    predict()












