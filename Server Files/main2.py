import cv2
import mediapipe
from progress.bar import Bar, ChargingBar
from utils.dataset_utils import load_dataset, load_reference_signs
from utils.mediapipe_utils import mediapipe_detection
from sign_recorder import SignRecorder


def preproceso():
    videos = load_dataset()
    print('Loading dataset')
    # Create a DataFrame of reference signs (name: str, model: SignModel, distance: int)
    reference_signs = load_reference_signs(videos)
    print('Creating dataframe with referenced signs')
    # Object that stores mediapipe results and computes sign similarities
    sign_recorder = SignRecorder(reference_signs)
    print('Preparing SignRecorded object to store mediapipe results and compute similarities')
    return  sign_recorder


def proceso(sign_recorder):
    print("Process started, calculating distances ...")
    # Turn on the webcam
    #cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    c = 0
    cap = cv2.VideoCapture('video.mp4')
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    bar = ChargingBar('Analyzing frames: ', max = length)
    # Set up the Mediapipe environment
    with mediapipe.solutions.holistic.Holistic(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as holistic:
            # Read feed
            ret = True
            recorded_results = []
            while ret:
                # Read feed
                ret, frame = cap.read()
                if ret == True:
                    # print('frames counted:'+ str(c))
                    # Make detections
                    image, results = mediapipe_detection(frame, holistic)
                    # Process results
                    recorded_results.append(results)
                    c = c+1
                    bar.next()
            sign_detected = sign_recorder.process_video(recorded_results)
            bar.finish()
            print("preprocess finished")
            return sign_detected