# PokeDex Lite
A humble attempt to create a real life PokeDex using deep learning for image recognition.
<br><br>
# Project Insight
### Data preparation
Due to the cumbersome nature of the task, only 10 classes were created. Meaning, this app can recognise only 10 different pokemon. These are : <b>Blastoise, Blaziken, Charizard, Chesnaught, Delphox, Greninja, Pikachu, Sceptile, Swampert and Venusaur</b>. 10 images were collected of each class and image augmentation was used to make it 128 images per class. Though the dataset is really small, the belief was that image augmentation and transfer learning will make accurate predictions nevetheless. Due to image augmentation, the only disadvantage is a specific class might be more prejudiced towards some particular data. But the collection of more data can overcome this.
<br>
### Deep Learning
Transfer learning on the MobileNetV2 model was done using Tensorflow for this dataset. The model was saved in h5 format and then converted to tflite format for use in an android application. The models can be found in the ![saved_model](saved_model) directory.
<br>
### Android Application
This app was inspired by the PokeDex used in the Kalos region. Tapping on the screen will open and close the input layout (like the original Kalos PokeDex). Click on the pokeball icon in the middle to capture a photo. The app will instantly recognise the most likeliest pokemon in the photo (only from the upper 10 classes mentioned) and will display their types (color coded). Swipping to the right will reveal their PokeDex data.
<br><br><br>
# Usage
The procedure is depicted below as a GIF file. <br><br>
<img src="Prototype/usage.gif" height=400 width=193/>
<br><br><br>
# Future Plan
Update more training images for each class for better classification and to extend classes to cover more Pokemon.
<br><br><br>
# Installation
The apk file is available ![here](https://github.com/Najib-Haq/PokeDex_lite/releases).
