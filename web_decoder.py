#!/usr/bin/env python3
"""
Web-based Polish Vehicle Registration Certificate QR Code Decoder

This script provides a web interface for processing QR code images from Polish
vehicle registration certificates.
"""

from flask import Flask, request, render_template, jsonify, send_file
import os
import json
import tempfile
from werkzeug.utils import secure_filename
from qr_decoder import PolishVehicleQRDecoder

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and QR code processing."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Save uploaded file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process the image
            decoder = PolishVehicleQRDecoder()
            results = decoder.process_image(filepath)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            if results:
                return jsonify(results)
            else:
                return jsonify({'error': 'Failed to process QR code'}), 400
                
        except Exception as e:
            return jsonify({'error': f'Processing error: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/decode', methods=['POST'])
def api_decode():
    """API endpoint for QR code decoding."""
    data = request.get_json()
    
    if not data or 'qrData' not in data:
        return jsonify({'error': 'QR data not provided'}), 400
    
    try:
        decoder = PolishVehicleQRDecoder()
        results = decoder.decode_vehicle_data(data['qrData'])
        
        if results:
            return jsonify(results)
        else:
            return jsonify({'error': 'Failed to decode QR data'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Decoding error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)