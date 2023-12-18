import datetime
from keras.layers import Dense, Activation, Flatten, Dropout, BatchNormalization
from keras.models import Sequential, Model
from keras.layers import Conv2D, MaxPooling2D, MaxPool2D
from keras import regularizers, optimizers
from keras.optimizers.schedules import ExponentialDecay
import pandas as pd
from keras.preprocessing.image import ImageDataGenerator
import pickle

from modelDAO import ModelDAO
import initial_csv_label
from processing_data import delete_old_image_files, split_train_and_test_dataset, convert_voice_to_images
from test_model import  test_model
from model import Model

train_data_path='data/train/'
wav_path = 'data/wav/'

# Function to convert waw to png
def append_ext(fn):
    fn = fn.replace(".wav",".png")
    fn = fn.split('/')[-1]
    return fn

def train_model():
    # First, we convert all audio in database to DataFrame to process easily for the future.
    initial_csv_label.assign_label_to_voice_from_database()

    train_data_path = 'data/train/'
    test_data_path = 'data/test/'

    # Delete old image training and testing files to clean disk.
    delete_old_image_files(train_data_path)
    delete_old_image_files(test_data_path)

    # Split the training and testing dataset with the specified ratio.
    split_train_and_test_dataset(0.85)

    # Convert training voice to images.
    convert_voice_to_images(train_data_path, 'data/train_data.csv')

    # Convert testing voice to images.
    convert_voice_to_images(test_data_path, 'data/test_data.csv')

    # Load training data from csv files.
    traindf=pd.read_csv('data/train_data.csv',dtype=str)
    traindf["voice_location"]=traindf["voice_location"].apply(append_ext)


    print(traindf)
    datagen=ImageDataGenerator(rescale=1./255.,validation_split=0.25)

    # Load generator train
    train_generator=datagen.flow_from_dataframe(
        dataframe=traindf,
        directory=train_data_path,
        x_col="voice_location",
        y_col="label",
        subset="training",
        batch_size=32,
        seed=42,
        shuffle=True,
        class_mode="categorical",
        target_size=(64,64))

    # Load generator val
    valid_generator=datagen.flow_from_dataframe(
        dataframe=traindf,
        directory=train_data_path,
        x_col="voice_location",
        y_col="label",
        subset="validation",
        batch_size=32,
        seed=42,
        shuffle=True,
        class_mode="categorical",
        target_size=(64,64))

    # Khoi tao model
    model = Sequential()
    model.add(Conv2D(32, (3, 3), padding='same',
                     input_shape=(64,64,3)))
    model.add(Activation('relu'))
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))
    model.add(Conv2D(128, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(128, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(2, activation='softmax'))

    initial_learning_rate = 0.0005
    lr_schedule = ExponentialDecay(
        initial_learning_rate,
        decay_steps=10000,  # Adjust this based on your training schedule
        decay_rate=0.9  # Adjust this as needed
    )

    optimizer = optimizers.RMSprop(learning_rate=lr_schedule)
    model.compile(optimizer=optimizer, loss="categorical_crossentropy", metrics=["accuracy"])
    # model.compile(optimizers.RMSprop(lr=0.0005, decay=1e-6),loss="categorical_crossentropy",metrics=["accuracy"])

    model.summary()

    # Tinh so buoc trong 1 epoch khi train
    STEP_SIZE_TRAIN=train_generator.n//train_generator.batch_size
    # Tinh so buoc trong 1 epoch khi val
    STEP_SIZE_VALID=valid_generator.n//valid_generator.batch_size

    # Train model
    model.fit(train_generator,
                        steps_per_epoch=STEP_SIZE_TRAIN,
                        validation_data=valid_generator,
                        validation_steps=STEP_SIZE_VALID,
                        epochs=100,verbose=1
    )

    model_dao = ModelDAO()
    last_model_id = model_dao.getLastModelId()
    new_modal_name = 'data/model/model' + str(last_model_id+1)+'.keras'

    model.save(new_modal_name)

    # Save label.
    model_indices_path = 'data/model/model_indices'+str(last_model_id+1)+'.pickle'
    with open(model_indices_path, 'wb') as handle:
        pickle.dump(train_generator.class_indices, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print("Model trained!")

    accuracy, precision, recall, f1_score_ =  test_model(new_modal_name, model_indices_path)
    print(accuracy, precision, recall, f1_score_)
    print('Model test!')

    model_entity = (last_model_id+1, 'model'+str(last_model_id+1), new_modal_name, datetime.datetime.now(), accuracy, precision,
                    recall, f1_score_, '', 0, traindf.shape[0])
    return Model(model_entity)


# train_model()