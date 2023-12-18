from keras.models import load_model
import pandas as pd
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
import pickle
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score

# Function to convert waw to png
def append_ext(fn):
    fn = fn.replace(".wav",".png")
    fn = fn.split('/')[-1]
    return fn

def test_model(model_path = 'data/model/model1.keras', model_indices_path = 'data/model/model_indices1.pickle'):
    # Load the testing data
    testdf=pd.read_csv('data/test_data.csv',dtype=str)
    testdf["voice_location"]=testdf["voice_location"].apply(append_ext)

    test_data_path='data/test/'



    # Initial the testing data
    test_datagen=ImageDataGenerator(rescale=1./255.)
    test_generator=test_datagen.flow_from_dataframe(
        dataframe=testdf,
        directory=test_data_path,
        x_col="voice_location",
        y_col=None,
        batch_size=32,
        seed=42,
        shuffle=False,
        class_mode=None,
        target_size=(64,64))

    # TInh so buoc test
    STEP_SIZE_TEST=test_generator.n//test_generator.batch_size

    # Tien hanh predict
    test_generator.reset()

    # Load the trained model
    model = load_model(model_path)


    pred = model.predict(test_generator)

    # Lay class predict probality lon nhat
    predicted_class_indices=np.argmax(pred,axis=1)

    # Load labels from the pickle file.
    with open(model_indices_path, 'rb') as handle:
        labels = pickle.load(handle)

    # Print the Accuracy and F1-Score metrics to the console.
    labels = dict((v,k) for k,v in labels.items())
    predictions = [labels[k] for k in predicted_class_indices]

    precision = precision_score(testdf['label'], predictions, average='binary', pos_label='1')
    recall = recall_score(testdf['label'], predictions, average='binary', pos_label='1')
    accuracy = accuracy_score(testdf['label'], predictions)
    f1_score_ = f1_score(testdf['label'], predictions,average='binary', pos_label='1')

    print('Precision: ' + str(precision))
    print('Recall: ' + str(recall))
    print('Accuracy: '+ str(accuracy))
    print('F1-score: '+ str(f1_score_))

    return accuracy, precision, recall, f1_score_

# print(test_model())