from keras.models import load_model
import pandas as pd
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
import pickle
from sklearn.metrics import accuracy_score, f1_score
from keras.preprocessing import image
from processing_data import  create_spectrogram
import os


def fake_voice_regconition(file_path='data/wav/real_voice/speaker4_10.wav', model_id = 1):

    # Convert voice to image and store it im the data/tmp/ folder.
    image_name = file_path.split('/')[-1].split('.')[0]
    file_folder = 'data/tmp/'
    create_spectrogram(file_path, image_name, file_folder)

    print('Convert voice to image successfully!')

    # Create ImageDataGenerator object to preprocess image.
    datagen = ImageDataGenerator(rescale=1./255.)

    # Image path
    image_path = file_folder+image_name+'.png'

    # Load image
    img = image.load_img(image_path, target_size=(64, 64))  # Chỉnh kích thước nếu cần

    # Convert image to numpy array
    img = image.img_to_array(img)
    img = img.reshape((1,) + img.shape)

    # Processing image
    img = datagen.standardize(img)

    # Load the trained model
    model = load_model('data/model/model' + str(model_id)+'.keras')

    pred = model.predict(img)

    # Lay class predict probality lon nhat
    predicted_class_indices=np.argmax(pred,axis=1)

    # Load labels from the pickle file.
    with open('data/model/model_indices' +str(model_id)+ '.pickle', 'rb') as handle:
        labels = pickle.load(handle)

    # Print the Accuracy and F1-Score metrics to the console.
    labels = dict((v,k) for k,v in labels.items())
    predictions = [labels[k] for k in predicted_class_indices]

    # print(predictions)

    # Remove image out of temporary folder.
    os.remove(image_path)
    return predictions[0]

# fake_voice_regconition('data/wav/real_voice/speaker1_10.wav')