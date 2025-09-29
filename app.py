import os
import uuid
import pandas as pd
from flask import Flask, render_template, request, session, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from eda_functions import get_data_preview, get_statistics, create_chart_with_api, get_ai_recommendations
from chart_logic import get_compatible_columns, get_chart_requirements
import logging

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24))
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv', 'xlsx', 'xls'}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file selected'}), 400
        
        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file format. Please upload CSV or Excel files only.'}), 400

        session_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        unique_filename = f"{session_id}_{filename}"
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
        file.save(filepath)
        
        session['uploaded_file'] = unique_filename
        session['original_filename'] = filename
        session['session_id'] = session_id
        
        if filename.lower().endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)
        
        columns = df.columns.tolist()
        data_types = {col: str(df[col].dtype) for col in columns}
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        return jsonify({
            'success': True,
            'filename': filename,
            'columns': columns,
            'data_types': data_types,
            'numeric_columns': numeric_columns,
            'categorical_columns': categorical_columns,
            'shape': df.shape
        })
    
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500

@app.route("/preview", methods=["POST"])
def get_preview():
    try:
        if 'uploaded_file' not in session:
            return jsonify({'error': 'No file uploaded'}), 400
        
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], session['uploaded_file'])
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 400
        
        filename = session['uploaded_file']
        if filename.lower().endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)
        
        data = request.get_json()
        table_option = data.get('tableOption', 'head') if data else 'head'
        
        preview_html = get_data_preview(df, table_option)
        stats_html = get_statistics(df)
        
        return jsonify({
            'preview': preview_html,
            'statistics': stats_html
        })
    
    except Exception as e:
        return jsonify({'error': f'Error generating preview: {str(e)}'}), 500

@app.route("/get-compatible-columns", methods=["POST"])
def get_compatible_columns_route():
    try:
        if 'uploaded_file' not in session:
            return jsonify({'error': 'No file uploaded'}), 400
        
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], session['uploaded_file'])
        filename = session['uploaded_file']
        if filename.lower().endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)
        
        data = request.get_json()
        chart_type = data.get('chartType')
        
        compatible_columns = get_compatible_columns(df, chart_type)
        
        return jsonify({
            'compatible_columns': compatible_columns,
            'requirements': get_chart_requirements(chart_type)
        })
    
    except Exception as e:
        return jsonify({'error': f'Error getting compatible columns: {str(e)}'}), 500

@app.route("/visualize", methods=["POST"])
def create_visualization():
    try:
        if 'uploaded_file' not in session:
            return jsonify({'error': 'No file uploaded'}), 400
        
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], session['uploaded_file'])
        filename = session['uploaded_file']
        if filename.lower().endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)
        
        data = request.get_json()
        chart_type = data.get('chartType')
        x_column = data.get('xColumn')
        y_column = data.get('yColumn')
        
        chart_config = create_chart_with_api(df, chart_type, x_column, y_column)
        
        return jsonify({
            'chart_config': chart_config,
            'success': True
        })
    
    except Exception as e:
        return jsonify({'error': f'Error creating visualization: {str(e)}'}), 500

@app.route("/ai-recommendations", methods=["POST"])
def get_ai_recommendations_route():
    try:
        if 'uploaded_file' not in session:
            return jsonify({'error': 'No file uploaded'}), 400
        
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], session['uploaded_file'])
        filename = session['uploaded_file']
        if filename.lower().endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)
        
        data = request.get_json()
        x_column = data.get('xColumn')
        y_column = data.get('yColumn')
        
        recommendations = get_ai_recommendations(df, x_column, y_column)
        
        return jsonify({'recommendations': recommendations})
    
    except Exception as e:
        return jsonify({'error': f'Error getting AI recommendations: {str(e)}'}), 500



# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    try:
        # Get port from environment variable (Render sets this automatically)
        port = int(os.environ.get("PORT", 5000))
        logging.info(f"Starting Flask app on port {port}")

        # Verify critical environment variables
        required_vars = ["AI21_API_KEY", "MONGODB_URI", "DB_NAME"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]

        if missing_vars:
            logging.error(f"Missing environment variables: {missing_vars}")
            # You can choose to exit or continue with warnings
            # sys.exit(1)  # Uncomment this line if you want to fail fast

        # Production settings
        app.run(
            debug=False,  # Never use debug=True in production
            host="0.0.0.0",  # Bind to all interfaces
            port=port,
            threaded=True  # Enable threading for better performance
        )

    except ValueError as e:
        logging.error(f"Invalid PORT environment variable: {e}")
        # Fallback to default port
        app.run(debug=False, host="0.0.0.0", port=5000)
    except Exception as e:
        logging.error(f"Failed to start Flask app: {e}")
        raise



