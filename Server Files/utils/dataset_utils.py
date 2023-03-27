import os
from progress.bar import Bar, ChargingBar
import pandas as pd
from tqdm import tqdm
import time
from models.sign_model import SignModel
from utils.landmark_utils import save_landmarks_from_video, load_array


def load_dataset():
    dataset = [
        file_name.replace(".pickle", "").replace("pose_", "")
        for root, dirs, files in os.walk(os.path.join("data", "dataset"))
        for file_name in files
        if file_name.endswith(".pickle") and file_name.startswith("pose_")
    ]
    print(len(dataset))
    # Create the dataset from the reference videos
    return dataset


def load_reference_signs(videos):
    bar = ChargingBar('Loading referenced signs: ', max = 814)
    start = time.process_time()
    reference_signs = {"name": [], "sign_model": [], "distance": []}
    for video_name in videos:
        
        sign_name = video_name.split("-")[0]
        path = os.path.join("data", "dataset", sign_name, video_name)

        left_hand_list = load_array(os.path.join(path, f"lh_{video_name}.pickle"))
        right_hand_list = load_array(os.path.join(path, f"rh_{video_name}.pickle"))

        reference_signs["name"].append(sign_name)
        reference_signs["sign_model"].append(SignModel(left_hand_list, right_hand_list))
        reference_signs["distance"].append(0)
        bar.next()
    reference_signs = pd.DataFrame(reference_signs, dtype=object)
    print(
        f'Dictionary count: {reference_signs[["name", "sign_model"]].groupby(["name"]).count()}'
    )
    bar.finish()
    print('Time used for loading the referenced signs:' + str(time.process_time() - start))
    print('Calculating sign . . .')
    return reference_signs
