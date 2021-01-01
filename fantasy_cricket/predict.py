'''
Module predicts the current performance of a player using
Linear Regresion based on the previous performances
'''

import json
import numpy as np
from sklearn.linear_model import LinearRegression

class Predict:
    """
    A class to predict performance of a player

    Attributes
    ----------
        name (str) : Name of the player
        path (str) : Path to the data 

    Methods
    -------
        predict(str,str) : Applies linear regression to output predicted score
    """

    @staticmethod
    def predict(name, path):
        """
            Predicts performance of player based on previous scores

            Parameters
            ----------
                name (str) : Name of player
                path (str) : Path to data 
            
            Returns
            -------
                score (float) : Predicted score of player

            Raises
            ------
                FileNotFoundError
                ValueError
                Exception
        """

        score = -1
        matches = 0
        file_handler = None

        try:
            file_handler = open(path)
            data = json.load(file_handler)

            for i in data["Players"]:
                if i["Name"] == name:
                    scores = i["Scores"]
                    matches = 1
                    break

            if not matches:
                raise Exception("Player not found")
            
            x_train = np.array(range(5)).reshape(-1,1)
            y_train = np.array(scores).reshape(-1,1)

            regr = LinearRegression(fit_intercept=True)

            try:
                regr.fit(x_train, y_train)
                pred = regr.predict(np.array(5).reshape(1, -1))
                if pred[0][0] < 0:
                    score = 0
                else:
                    score = pred[0][0]
            except ValueError:
                score = -1     

        except FileNotFoundError as e:
            print("Error Message: ", e)
        except Exception as e:
            print("Error Message: ", e)
        finally:
            if file_handler is not None:
                file_handler.close()
            return float(score)
