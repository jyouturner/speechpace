from flask import Flask, request, send_file
from flask_cors import CORS
from sklearn.linear_model import LinearRegression
import numpy as np
import coremltools as ct
import os

app = Flask(__name__)
CORS(app)

@app.route('/train_model', methods=['POST'])
def train_model():
    if 'file' not in request.files:
        return 'No file provided', 400

    audio_file = request.files['file']

    # TODO: Extract features from the audio file

    # Example: Creating dummy data for demonstration purposes
    X = np.random.rand(100, 2)
    y = 2 * X[:, 0] + 3 * X[:, 1]

    # Train a simple model
    model = LinearRegression()
    model.fit(X, y)

    # Convert the model to Core ML format
    coreml_model = ct.converters.sklearn.convert(model, input_features=['x1', 'x2'], output_feature_names='y')
    coreml_model.save('trained_model.mlmodel')

    # Send the Core ML model back to the client
    return send_file('trained_model.mlmodel', mimetype='application/octet-stream', as_attachment=True, attachment_filename='trained_model.mlmodel')

if __name__ == '__main__':
    app.run(debug=True)
