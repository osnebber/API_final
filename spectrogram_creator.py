import librosa
import soundfile as sf
import os
import numpy as np
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
import shutil
import cv2
import matplotlib.pyplot as plt 

# Specify the path to the output directory
spec_path = 'data/spectrograms_computed/'

# Iterate through the files and subdirectories in the output directory
for item in os.listdir(spec_path):
    item_path = os.path.join(spec_path, item)
    if os.path.isfile(item_path):
        os.remove(item_path)
        print(item_path)
    elif os.path.isdir(item_path):
        shutil.rmtree(item_path)

print("Output directory cleared.")

'Define the function to compute and save the spectograms'

def spectrogram_creation(audio_path,spectrogram_path):
    y, sr = librosa.load(audio_path)
    spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
    
#     # Normalize the spectrogram
#     scaler = StandardScaler()
#     normalized_spectrogram = scaler.fit_transform(spectrogram)
#     norm_spec = np.array(normalized_spectrogram)

    # Convert to decibels (log scale)
    spectrogram_db = librosa.power_to_db(spectrogram, ref=np.max)
    
    librosa.display.specshow(spectrogram_db)
    plt.savefig(spectrogram_path)
    plt.close()

'Iterate throught the genres folders, compute the spectograms and create the new spectrogram dataset'

try:
    os.makedirs("data/spectrograms_computed")
except FileExistsError:
    pass
filenames = ['blues', 'classical', 'country', 'disco', 'hiphop','jazz', 'metal', 'pop', 'reggae', 'rock']
for filename in filenames: 
    os.makedirs("data/Spectrograms_computed/"+filename)


dataset_path = 'data/genres_original'

dataset_spec = []



# Iterate through all directories in the specified directory
for genre in os.listdir(dataset_path):
    print(f"Creating {genre} spectrograms")
    count_song_genre = 1
    genre_path = os.path.join(dataset_path, genre)
    
    for song in os.listdir(genre_path):
        song_path = os.path.join(genre_path, song)
        try:
            song_name=song.replace('.wav','')
            spectrogram_creation(song_path, spec_path+genre+'/'+song_name+'.png')
            count_song_genre +=1
        except Exception as e:
            print(e)