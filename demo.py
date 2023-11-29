import os
import numpy as np
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
import cv2
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import tensorflow as tf
from sklearn.manifold import TSNE

# Define the parent directory you want to analyze
parent_directory = 'spectrograms_computed'  

# Create an empty dictionary to store directory names and file counts
directory_file_counts = {}

# Walk through the parent directory and count files in each subdirectory
print("Reading files...")
for root, dirs, files in os.walk(parent_directory):
    # Count the files in the current directory
    file_count = len(files)
    
    # Store the directory name and file count in the dictionary
    directory_file_counts[root] = file_count

# Print the directory names and their respective file counts
# for directory, file_count in directory_file_counts.items():
#     print(f"Directory: {directory}, File Count: {file_count}")

classes = [a for a in os.listdir('genres_original') if '.' not in a]
# print(classes)


'Create X and Y for: train, valid, test'

img_size = 256
dataset=[]
names=[]
print("Loading files...")
for label in classes:
    # print(f"Loading {label}...")
    path = os.path.join(parent_directory, label)
    class_num = classes.index(label)
    
    for img in os.listdir(path):
        try:
            img_arr = cv2.imread(os.path.join(path, img))[...,::-1] #convert BGR to RGB format
            resized_arr = cv2.resize(img_arr, (img_size, img_size)) # Reshaping images to preferred size
            dataset.append([resized_arr, class_num])
            names.append(img.replace('.png',''))
        except Exception as e:
            print(e)

dataset_toUse = np.array(dataset,dtype=object)
# print(dataset_toUse.shape)

X = []
Y = []
for feature, label in dataset_toUse:
    X.append(feature)
    Y.append(label)

X = np.array(X) / 255.
Y = np.array(Y)


loaded_model = tf.keras.models.load_model("models\MobileNetModel.keras")
embedding_deep_model=keras.Model(loaded_model.input,loaded_model.layers[-3].output)

genreLabelsDic = {
    "blues" : 0,
    "classical": 1,
    "country": 2,
    "disco" : 3,
    "hiphop": 4,
    "jazz": 5,
    "metal":6,
    "pop": 7,
    "reggae": 8,
    "rock":9
}

inverseGenreLabelsDic={k:v for v,k in genreLabelsDic.items()}
Y_labeled=[inverseGenreLabelsDic[y] for y in Y]

print("Embedding the songs...")
# x_deep_embedded=embedding_deep_model.predict(X)
# np.save("embedded_X",x_deep_embedded)

x_deep_embedded=np.load("embedded_X.npy")

def cosine_similarity(A,B):
    return np.dot(A,B)/(np.linalg.norm(A)*np.linalg.norm(B))

categories=[*genreLabelsDic.keys()]

def k_closest_neighbors(X,i,k=1):
    similarity=[cosine_similarity(X[i],X_j) for X_j in X]
    order=np.argsort(similarity)[::-1]
    order=np.delete(order,np.where(order==i))
    top_k_order=order[:k]
    top_k_similarity=[similarity[j] for j in top_k_order]
    return top_k_order, top_k_similarity


def explore_neighbors(X,i,k=15):
    top_index,top_sim=k_closest_neighbors(X,i,k)
    
    fig=plt.figure()

    print("Mapping the songs...")
    tsne = TSNE(n_components=2, verbose=0, random_state=123)
    X_hat=StandardScaler().fit_transform(X)
    X_hat = tsne.fit_transform(X_hat)
    print("Building discovery map...")
    
    max_a=4/5; min_a=1/5
    max_w=2.5; min_w=0.5
    for index,sim in zip(top_index,top_sim):
        relative_sim=(sim-min(top_sim))/(max(top_sim)-min(top_sim))
        interpolated_a=relative_sim*max_a+(1-relative_sim)*min_a
        interpolated_w=relative_sim*max_w+(1-relative_sim)*min_w
        plt.plot([X_hat[i,0],X_hat[index,0]],[X_hat[i,1],X_hat[index,1]],
                 c='k',alpha=interpolated_a,linewidth=interpolated_w,
                zorder=0)
        plt.scatter(X_hat[index,0],X_hat[index,1], marker="o", s=50,
                 c='k',alpha=interpolated_a,linewidth=interpolated_w,
                zorder=-1)
            
            
    df = pd.DataFrame()
    df["y"] = np.delete(Y_labeled,i,axis=0)
    df["comp-1"] = np.delete(X_hat,i,axis=0)[:,0]
    df["comp-2"] = np.delete(X_hat,i,axis=0)[:,1]

    sns.scatterplot(x="comp-1", y="comp-2", hue=df.y.tolist(),
                    palette=sns.color_palette("colorblind", 10),
                    data=df)
    
    plt.scatter(X_hat[i,0],X_hat[i,1],marker="*",s=100,
                color=sns.color_palette("colorblind", 10)[Y[i]],
               zorder=10)
    
    
    margin_prop=1.4
    
    x_range=margin_prop*(max(X_hat[top_index,0])-min(X_hat[top_index,0]))
    x_0=(max(X_hat[top_index,0])+min(X_hat[top_index,0]))/2
    y_range=margin_prop*(max(X_hat[top_index,1])-min(X_hat[top_index,1]))
    y_0=(max(X_hat[top_index,1])+min(X_hat[top_index,1]))/2
    xy_range=max(x_range,y_range)
    plt.xlim([x_0-xy_range/2,x_0+xy_range/2])
    plt.ylim([y_0-xy_range/2,y_0+xy_range/2])
    
    # plt.legend(bbox_to_anchor=(1.05, 1),loc='upper left', borderaxespad=0.,ncol=3)
    plt.legend(bbox_to_anchor=(1.2, 1),loc='upper left', borderaxespad=0.,ncol=3)
    
#     plt.show()
    ax=fig.axes[0]
    return fig,ax,top_index,top_sim


test_i=np.random.randint(len(x_deep_embedded))#15
fig,ax,top_index,top_sim=explore_neighbors(x_deep_embedded,test_i)
top_names=[names[i] for i in top_index]
print(test_i)


top_names=[names[test_i]]+top_names
top_sim=[1]+[top_sim]

from DiscoveryMap import DiscoveryMap
DiscoveryMap(fig,ax,dirs=top_names,similarities=top_sim)