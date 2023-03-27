import multiprocessing
import pandas as pd
import numpy as np
from collections import Counter
from scoop import futures
from utils.dtw import dtw_distances
from models.sign_model import SignModel
from utils.landmark_utils import extract_landmarks
from multiprocessing import Pool
import threading
import os

class SignRecorder(object):
    def __init__(self, reference_signs: pd.DataFrame, seq_len=50):
        # Variables for recording
        self.is_recording = False
        self.seq_len = seq_len

        # List of results stored each frame
        self.recorded_results = []

        # DataFrame storing the distances between the recorded sign & all the reference signs from the dataset
        self.reference_signs = reference_signs

    def process_results(self, results):
        """
        If the SignRecorder is in the recording state:
            it stores the landmarks during seq_len frames and then computes the sign distances
        :param results: mediapipe output
        :return: Return the word predicted (blank text if there is no distances)
                & the recording state
        """
        if self.is_recording:
            if len(self.recorded_results) < self.seq_len:
                self.recorded_results.append(results)
            else:
                self.compute_distances()
                print(self.reference_signs)

        if np.sum(self.reference_signs["distance"].values) == 0:
            return "", self.is_recording
        return self._get_sign_predicted(), self.is_recording

    def process_video(self, recorded_results):
        self.reference_signs["distance"].values[:] = 0
        self.recorded_results = recorded_results
        seña = self.compute_distances()
        print("A-------------------------------------"+seña)
        print(len(seña))
        df = pd.DataFrame(seña)
        print(seña)
        neww = seña[0]
        print(str(type(neww))+ " AAAA")
        type(seña)
        print("A-------------------------------------"+seña)
        return neww

    def compute_distances(self):
        """
        Updates the distance column of the reference_signs
        and resets recording variables
        """
        left_hand_list, right_hand_list = [], []
        for results in self.recorded_results:
            _, left_hand, right_hand = extract_landmarks(results)
            left_hand_list.append(left_hand)
            right_hand_list.append(right_hand)

        # Create a SignModel object with the landmarks gathered during recording
        recorded_sign = SignModel(left_hand_list, right_hand_list)

        # Compute sign similarity with DTW (ascending order)


        #aqui se genera chido one
        # create as many processes as there are CPUs on your machine
        
        chunks = np.array_split(self.reference_signs, 4)
        hilos = []
        lista = [None]*4
        for i in range(4):
            hilo = threading.Thread(target=dtw_distances, args=(recorded_sign,chunks[i],lista, i))
            hilos.append(hilo)
        
        # Inicia los cuatro hilos
        for hilo in hilos:
            hilo.start()

        # Espera a que los cuatro hilos terminen la ejecución
        for hilo in hilos:
            hilo.join()
        print(hilos)
        final = pd.concat(lista)
        print(final)
        final.sort_values(by=["distance"], inplace = True)
        print(final)
        print("--------------------FINAL1-------------------")
        final2 = final.sort_values("distance")
        print("--------------------FINAL2-------------------")
        print(final2)
        df = final[final.distance != 'inf']
        print("Detalles del dataframe")
        print(df.dtypes)
        
        # convertir la columna a un tipo numérico
        df['distance'] = pd.to_numeric(df['distance'], errors='coerce')

        # reemplazar 'inf' con NaN
        df.replace([float('inf')], float('nan'), inplace=True)

        # eliminar filas con valores nulos
        df.dropna(inplace=True)

        # mostrar el dataframe resultante
        print(df)

        # Reset variables
        self.recorded_results = []
        self.is_recording = False
        
        sign_names = df.iloc[:13]["name"].values
        print(sign_names)
    
        #Ya suéltame dios
        # Get the list (of size batch_size) of the most similar reference signs
        sign_names = df.iloc[:13]["name"].values
        print(sign_names)
        sign_names_df = pd.DataFrame(df)
        print(sign_names_df)
        sign_names_df =  sign_names_df.drop('sign_model', axis=1)
        df_thirdteen = sign_names_df.iloc[:13]
        df_thirdteen['distance'] =  df_thirdteen['distance'].astype(float)
        print(df_thirdteen)
        suma = df_thirdteen.groupby('name')['distance'].sum()
        count = df_thirdteen.groupby('name').count()
        min_letter= (df_thirdteen.groupby('name').min())/count
        dfd =  pd.DataFrame(min_letter)
        print(dfd)
        dfd = dfd.idxmin()
        dfd = dfd.astype(str)
        print(dfd)
        print("Conteo de variables")
        print(count)
        print("Distancias minimas por letra")
        print(min_letter)
        print("Distancia minima despues del promedio de conteos y minmia distnaci")
        print(dfd)
        print('sum of the groupings of each letter')
        print(suma)
        return dfd
  