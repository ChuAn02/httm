import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import gc
import pandas as pd
import numpy as np




# Create the spectrogram from the wav files
def create_spectrogram(filename,name, file_path):
    plt.interactive(False)
    clip, sample_rate = librosa.load(filename, sr=None)
    fig = plt.figure(figsize=[0.72,0.72])
    ax = fig.add_subplot(111)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.set_frame_on(False)
    S = librosa.feature.melspectrogram(y=clip, sr=sample_rate)
    librosa.display.specshow(librosa.power_to_db(S, ref=np.max))
    filename  = file_path + name + '.png'
    plt.savefig(filename, dpi=400, bbox_inches='tight',pad_inches=0)
    plt.close()
    fig.clf()
    plt.close(fig)
    plt.close('all')
    del filename,name,clip,sample_rate,fig,ax,S

def delete_old_image_files(folder_path):
    # List all files in the folder
    file_names = os.listdir(folder_path)

    # Iterate over the file names and delete each file
    for file_name in file_names:
        file_path = os.path.join(folder_path, file_name)

        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_name}")
            except OSError as e:
                print(f"Error deleting file: {file_name} - {e}")

def split_train_and_test_dataset(train_ratio=0.7):
    # Load the original CSV file into a DataFrame
    original_file = 'data/labels.csv'  # Replace with the path to your CSV file
    df = pd.read_csv(original_file)

    # Define the ratio for splitting the data

    # Split the data into two DataFrames
    total_rows = len(df)
    train_rows = int(train_ratio * total_rows)

    # Shuffle the rows of the original DataFrame to randomize the data
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    train_df = df.iloc[:train_rows]
    test_df = df.iloc[train_rows:]

    # Save the two new CSV files
    train_file = 'data/train_data.csv'
    test_file = 'data/test_data.csv'

    train_df.to_csv(train_file, index=False)
    test_df.to_csv(test_file, index=False)

    print(f"Training data saved to '{train_file}'")
    print(f"Testing data saved to '{test_file}'")

def convert_voice_to_images(destination_image_path, csv_data_path):
    df =pd.read_csv(csv_data_path)

    # destination_image_path is train_data_path or test_data_path
    for row in df.itertuples():
        filename, name = row.voice_location, row.voice_location.split('/')[-1].split('.')[0]
        print(filename, name)

        # Convert voice to image files and store them in the destination_image_path
        create_spectrogram(filename, name, destination_image_path)

    # Clean garbage data.
    gc.collect()
    print('Process Done!')

# # Delete old image training and testing files to clean disk.
# delete_old_image_files(train_data_path)
# delete_old_image_files(test_data_path)
#
# # Split the training and testing dataset with the specified ratio.
# split_train_and_test_dataset(0.5)
#
# # Convert training voice to images.
# convert_voice_to_images(train_data_path, 'data/train_data.csv')
#
# # Convert testing voice to images.
# convert_voice_to_images(test_data_path, 'data/test_data.csv')