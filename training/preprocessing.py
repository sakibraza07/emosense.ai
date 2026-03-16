# import os
# import librosa
# import numpy as np

# dataset_path="/Users/asjadshaikh/Downloads/archive"

# features = []
# labels = []

# for actor_fold in os.listdir(dataset_path):
#     actor_path=os.path.join(dataset_path,actor_fold)

#     if os.path.isdir(actor_path):
#         for file in os.listdir(actor_path):
#             if file.endswith(".wav"):
#                 parts=file.split("-")
#                 emotion_num=parts[2]

#                 file_path=os.path.join(actor_path,file)

#                 signal,sample_rate=librosa.load(file_path,sr=None)

#                 mfccs=librosa.feature.mfcc(
#                     y=signal,
#                     sr=sample_rate,
#                     n_mfcc=40
#                 )

#                 mfccs_mean=np.mean(mfccs,axis=1)

#                 features.append(mfccs_mean)
#                 labels.append(emotion_num)

#                 print(f"{file} --> Emotion: {emotion_num}")
#                 print("MFCC Shape: ",mfccs_mean.shape)
#                 print("-" * 40)

# features = np.array(features)
# labels = np.array(labels)

# np.save("features.npy", features)
# np.save("labels.npy", labels)

# print("Saved features and labels successfully.")
import os
import librosa
import numpy as np

dataset_path="/Users/asjadshaikh/Downloads/archive"

features = []
labels = []

for actor_fold in os.listdir(dataset_path):
    actor_path=os.path.join(dataset_path,actor_fold)

    if os.path.isdir(actor_path):
        for file in os.listdir(actor_path):
            if file.endswith(".wav"):
                parts=file.split("-")
                emotion_num=parts[2]

                file_path=os.path.join(actor_path,file)

                signal,sample_rate=librosa.load(file_path,sr=None)

                # 🔹 MFCC
                mfccs=np.mean(
                    librosa.feature.mfcc(
                        y=signal,
                        sr=sample_rate,
                        n_mfcc=40
                    ),
                    axis=1
                )

                # 🔹 Chroma
                chroma = np.mean(
                    librosa.feature.chroma_stft(
                        y=signal,
                        sr=sample_rate
                    ),
                    axis=1
                )

                # 🔹 Mel Spectrogram
                mel = np.mean(
                    librosa.feature.melspectrogram(
                        y=signal,
                        sr=sample_rate
                    ),
                    axis=1
                )

                # 🔹 Combine all features
                combined = np.concatenate([mfccs, chroma, mel])

                features.append(combined)
                labels.append(emotion_num)

features = np.array(features)
labels = np.array(labels)

np.save("features.npy", features)
np.save("labels.npy", labels)

print("New features saved.")
print("Feature vector shape:", features.shape)