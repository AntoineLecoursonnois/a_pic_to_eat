import numpy as np
from tensorflow import keras


def predict(X):
    '''
    Load a keras model using VGG16 to identify products from an image
    '''
    # Load the model
    model = keras.models.load_model("keras_model_256_96.h5")

    # Identify products presents in X
    # X is a list of pacthes converted into numpy arrays
    model_prediction = model.predict(X)

    # Convert the numpy prediction into encoded products
    y_predict_back = np.argmax(model_prediction, axis=-1)

    # Transfer encoded product result to product name
    products_encoded = {
        'ananas': 0,
        'aubergine': 1,
        'banane': 2,
        'brocoli': 3,
        'carotte': 4,
        'citron': 5,
        'concombre': 6,
        'gingembre': 7,
        'melon': 8,
        'pasteque': 9,
        'poivron': 10,
        'pomme_de_terre': 11,
        'raisin': 12,
        'salade': 13,
        'tomate': 14
    }

    # Instance the list of results
    results = []

    # Append each product name detected into the list
    for code in y_predict_back:
        for products, label in products_encoded.items():
            if code == label:
                results.append(products)

    # set a list of unique products name
    results = set(results)

    # Dictionary format is necessary for Streamlit to read our datas as a json
    return dict(prediction=results)
