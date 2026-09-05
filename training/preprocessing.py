"""
Builds features.npy / labels.npy from the RAVDESS dataset, with
augmentation to help the model generalize (RAVDESS is only 1440 clips
across 8 classes, which is small).

Each real clip produces 4 training examples:
  1. original
  2. + background noise
  3. pitch-shifted
  4. time-stretched

This roughly 4x's the training set. Change AUGMENT below to False to
reproduce the old behavior (original features only).

Usage:
    python preprocessing.py /path/to/ravdess/root
"""
import os
import sys
import numpy as np

# training/preprocessing.py lives in training/, but the feature extractor
# lives in utils/ (it's shared with the live app for inference). Add the
# project root to the path so both scripts import the exact same file --
# using two separate copies risks them drifting apart, which breaks accuracy
# silently (train-time features != inference-time features).
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.audio_features import extract_features

AUGMENT = True

def main():
    if len(sys.argv) > 1:
        dataset_path = sys.argv[1]
    else:
        dataset_path = "/Users/asjadshaikh/Downloads/archive"  # fallback to old default

    if not os.path.isdir(dataset_path):
        print(f"Dataset path not found: {dataset_path}")
        print("Usage: python preprocessing.py /path/to/ravdess/root")
        sys.exit(1)

    features = []
    labels = []
    variants = [None, "noise", "pitch", "stretch"] if AUGMENT else [None]

    n_files = 0
    for actor_fold in sorted(os.listdir(dataset_path)):
        actor_path = os.path.join(dataset_path, actor_fold)
        if not os.path.isdir(actor_path):
            continue

        for file in sorted(os.listdir(actor_path)):
            if not file.endswith(".wav"):
                continue

            parts = file.split("-")
            emotion_num = parts[2]
            file_path = os.path.join(actor_path, file)
            n_files += 1

            for variant in variants:
                try:
                    combined = extract_features(file_path, augment=variant)
                except Exception as e:
                    print(f"Skipping {file} ({variant}): {e}")
                    continue
                features.append(combined)
                labels.append(emotion_num)

            if n_files % 100 == 0:
                print(f"Processed {n_files} source files "
                      f"({len(features)} total examples so far)...")

    features = np.array(features)
    labels = np.array(labels)

    np.save("features.npy", features)
    np.save("labels.npy", labels)

    print("Done.")
    print("Source files:", n_files)
    print("Total examples (with augmentation):", features.shape[0])
    print("Feature vector shape:", features.shape)


if __name__ == "__main__":
    main()