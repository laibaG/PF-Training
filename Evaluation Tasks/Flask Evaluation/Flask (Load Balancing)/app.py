import traceback
from flask import Flask, request, render_template

class ML:
    def __init__(self):
        self.available_models = {
            "face_detection": "/additional_drive/ML/face_detection",
            "car_detection": "/additional_drive/ML/car_detection",
            "shoe_detection": "/additional_drive/ML/shoe_detection",
            "cloth_detection": "/additional_drive/ML/cloth_detection",
            "signal_detection": "/additional_drive/ML/signal_detection",
            "water_level_detection": "/additional_drive/ML/water_level_detection",
            "missile_detection": "/additional_drive/ML/missile_detection"
        }
        self.loaded_models_limit = 2
        self.loaded_models = {
            #added a var of requests to keep track of frequencies since we are not using any DB
            model: {"path": self.load_weights(model), "requests": 0}
            for model in list(self.available_models)[:self.loaded_models_limit]
        }

    def load_weights(self, model):
        return self.available_models.get(model, None)

    def load_balancer(self, new_model):
        #error msg if requested model doesnt exists in the list
        if new_model not in self.available_models:
            raise ValueError("The requested model is not available.")

        #incrementing only the requested model frequency by 1
        for model in self.loaded_models:
            if model == new_model:
                self.loaded_models[model]["requests"] += 1

        #add new model if not already in the loaded models
        if new_model not in self.loaded_models:
            lrm = min(self.loaded_models, key=lambda x: self.loaded_models[x]["requests"])
            del self.loaded_models[lrm]
            self.loaded_models[new_model] = {"path": self.load_weights(new_model), "requests": 0}

        self.loaded_models[new_model]["requests"] = 0


app = Flask(__name__)
ml = ML()

@app.route('/get_loaded_models', methods=['GET', 'POST'])
def get_loaded_models():
    return ml.loaded_models


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        model = request.form["model"]
        if model not in ml.loaded_models:
            ml.load_balancer(model)
        ml.loaded_models[model]["requests"] += 1
    return render_template('index.html', loaded_models=ml.loaded_models)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)