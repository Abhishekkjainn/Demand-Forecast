from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pathlib import Path
from forecasting import predict_demand, check_stock_and_alert
from bokeh_forecast import create_bokeh_plots
from utils import load_data
import os
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Set up environment and logging
UPLOAD_FOLDER = Path(os.getenv('UPLOAD_FOLDER', 'uploads'))
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max file size
app.config['ENV'] = 'production'  # Ensure production mode
app.config['DEBUG'] = False  # Disable debug mode for production

# Configure logging
app.logger.setLevel(logging.INFO)
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}
data_file_path = None

# Allowed file type check function
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home route
@app.route('/')
def home():
    return "Welcome. Use /upload to upload a file and /forecast for forecasting."

# Upload file route
@app.route('/upload', methods=['POST'])
def upload_file():
    global data_file_path

    if 'file' not in request.files:
        app.logger.error("No file part in the request")
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        app.logger.error("No file selected")
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        app.logger.error("Invalid file type")
        return jsonify({"error": "Only .csv and .xlsx files are allowed"}), 400

    try:
        data_file_path = UPLOAD_FOLDER / file.filename
        file.save(data_file_path)

        # Remove any existing plots in the upload folder
        for plot in UPLOAD_FOLDER.glob("*.html"):
            plot.unlink()

        app.logger.info(f"File uploaded successfully: {data_file_path}")
        return jsonify({"message": "File uploaded successfully", "file_path": str(data_file_path)})

    except Exception as e:
        app.logger.error(f"File upload error: {e}")
        return jsonify({"error": "Failed to upload file"}), 500

# Forecast route
@app.route('/forecast', methods=['POST'])
def forecast():
    global data_file_path

    if not data_file_path:
        app.logger.error("No data file uploaded yet.")
        return jsonify({"error": "No data file uploaded yet. Please upload a file first."}), 400

    data = request.get_json()
    item_id = data.get('item_id')

    if item_id is None:
        app.logger.error("Item ID is required.")
        return jsonify({"error": "Item ID is required."}), 400

    try:
        # Load the dataset
        df = load_data(data_file_path)

        # Check if the item exists in the dataset
        if item_id not in df['item_id'].values:
            app.logger.error(f"Item ID {item_id} not found in the dataset")
            return jsonify({"error": f"Item ID {item_id} not found in the dataset."}), 404

        # Predict demand
        future_months, predicted_demand = predict_demand(df, item_id)

        if predicted_demand is None:
            app.logger.error(f"Could not generate forecasts for item ID {item_id}.")
            return jsonify({"error": f"Could not generate forecasts for item ID {item_id}."}), 500

        # Check stock and generate alerts
        alerts = check_stock_and_alert(df, item_id, predicted_demand, future_months)

        # Create Bokeh plot
        plot_path = create_bokeh_plots(df, item_id, future_months, predicted_demand)

        response = {
            "future_months": future_months if isinstance(future_months, list) else future_months.tolist(),
            "predicted_demand": predicted_demand if isinstance(predicted_demand, list) else predicted_demand.tolist(),
            "alerts": alerts,
            "plot_url": f"/plot/{item_id}"
        }

        app.logger.info(f"Forecast successfully generated for item ID {item_id}")
        return jsonify(response)

    except Exception as e:
        app.logger.error(f"Error during forecasting: {e}")
        return jsonify({"error": "An error occurred during forecasting. Please try again."}), 500


# Plot route to serve the forecast plot
@app.route('/plot/<item_id>')
def plot(item_id):
    plot_path = UPLOAD_FOLDER / f"demand_forecast_{item_id}.html"
    if plot_path.exists():
        return send_file(plot_path)
    else:
        app.logger.error(f"Plot for item ID {item_id} not found")
        return jsonify({"error": "Plot not found"}), 404

# Run the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
