import os
import csv

import pandas

from sample import  SampleDAO

def assign_label_to_voice():
    real_voice_folder_path = 'data/wav/real_voice'
    fake_voice_folder_path = 'data/wav/fake_voice'

    # List all files in the folder
    real_voice_file_names = os.listdir(real_voice_folder_path)
    fake_voice_file_names = os.listdir(fake_voice_folder_path)

    # Assign label for these wav files.
    labels = []
    columns_name = ['voice_location', 'label']
    labels.append(columns_name)

    for file_name in real_voice_file_names:
        row = [real_voice_folder_path + '/' + file_name, '1']
        labels.append(row)

    for file_name in fake_voice_file_names:
        row = [fake_voice_folder_path + '/' + file_name, '0']
        labels.append(row)

    labels_file_name = 'data/labels.csv'
    with open(labels_file_name, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write the data to the CSV file
        csv_writer.writerows(labels)

    print(f'CSV file "{labels_file_name}" has been created successfully.')

def assign_label_to_voice_from_database():


    # Assign label for these wav files.
    labels = []
    columns_name = ['voice_location', 'label']
    labels.append(columns_name)

    sample_dao = SampleDAO()
    samples = sample_dao.getAllSamples()
    for sample in samples:
        row = [sample[0], sample[1]]
        labels.append(row)

    labels_file_name = 'data/labels.csv'
    with open(labels_file_name, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write the data to the CSV file
        csv_writer.writerows(labels)

    print(f'CSV file "{labels_file_name}" has been created successfully.')
# assign_label_to_voice_from_database()

# assign_label_to_voice()



