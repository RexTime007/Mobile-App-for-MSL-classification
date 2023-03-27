import pandas as pd
from fastdtw import fastdtw
import numpy as np
from models.sign_model import SignModel


def dtw_distances(recorded_sign: SignModel, reference_signs: pd.DataFrame, results, index):
    
    print('ha empezado un hilo de scoop')
    """
    Use DTW to compute similarity between the recorded sign & the reference signs

    :param recorded_sign: a SignModel object containing the data gathered during record
    :param reference_signs: pd.DataFrame
                            columns : name, dtype: str
                                      sign_model, dtype: SignModel
                                      distance, dtype: float64
    :return: Return a sign dictionary sorted by the distances from the recorded sign
    
        Preguntar al doctor si es correcto lo siguiente:
            
            1) Primero vamos a implemetar el scoop

            import numpy as np
            import scoop

            2) Despues vamos a dividir el df en 10, para que los grupos se ejecuten con el método y obtengan los df 
            de forma separada
            
            # divide la lista de referencias en 10 subconjuntos
            n = 10
            subsets = np.array_split(reference_signs, n)

            3) Mandamos llamar la funcion con el scoop
            results = list(scoop.map(dtw_distances, [recorded_sign]*n, subsets))

            4) Ahora, si tenemos que mandar la misma función, probablemente no funcionará de forma recursiva /*idk*/
            Por lo que tendremos que generar un método dentro del método prinicipal
            donde

            import numpy as np
            import scoop
            import pandas as pd
            from fastdtw import fastdtw
            from models.sign_model import SignModel

            def dtw_distances(recorded_sign: SignModel, reference_signs: pd.DataFrame):
                def distances_with_scoop(self ?) -> Según yo aquí no necesitamos el self
                    /*
                        Todo el proceso original
                    */
                n = 10
                subsets = np.array_split(reference_signs, n)
                results = list(scoop.map(distances_with_scoop, [recorded_sign]*n, subsets))
                return reference_signs.sort_values(by=["distance"])

            
    """
    # Embeddings of the recorded sign
    rec_left_hand = recorded_sign.lh_embedding
    rec_right_hand = recorded_sign.rh_embedding

    for idx, row in reference_signs.iterrows():
        # Initialize the row variables
        ref_sign_name, ref_sign_model, _ = row

        # If the reference sign has the same number of hands compute fastdtw
        if (recorded_sign.has_left_hand == ref_sign_model.has_left_hand) and (
            recorded_sign.has_right_hand == ref_sign_model.has_right_hand
        ):
            ref_left_hand = ref_sign_model.lh_embedding
            ref_right_hand = ref_sign_model.rh_embedding

            if recorded_sign.has_left_hand:
                row["distance"] += list(fastdtw(rec_left_hand, ref_left_hand))[0]
            if recorded_sign.has_right_hand:
                row["distance"] += list(fastdtw(rec_right_hand, ref_right_hand))[0]

        # If not, distance equals infinity
        else:
            row["distance"] = np.inf
    results[index]=reference_signs
    print(reference_signs.sort_values(by=["distance"]))
    return reference_signs.sort_values(by=["distance"])
