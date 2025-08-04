# Polish Vehicle Registration QR Code Decoder

A comprehensive solution for decoding QR codes from Polish vehicle registration certificates using the `polish-vehicle-registration-certificate-decoder` npm package.

## Features

- 🖼️ **Image Processing**: Upload and process QR code images from vehicle registration certificates
- 🔍 **QR Code Detection**: Automatic QR code detection and extraction using OpenCV and pyzbar
- 🚗 **Vehicle Data Decoding**: Decode vehicle information using the official Polish decoder package
- 🌐 **Web Interface**: Modern, responsive web interface with drag-and-drop functionality
- 🔧 **API Endpoints**: RESTful API for programmatic access
- 📊 **JSON Output**: Structured JSON output with vehicle information
- 🔒 **Hash Generation**: SHA-256 hash generation for QR code data

## Architecture

The solution consists of two main components:

1. **Python Backend** (`qr_decoder.py`, `web_decoder.py`): Handles image processing, QR code detection, and web interface
2. **Node.js Bridge** (`node_bridge.js`): Interfaces with the `polish-vehicle-registration-certificate-decoder` npm package

## Prerequisites

- Python 3.7+
- Node.js 14+
- npm

## Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd polish-vehicle-qr-decoder
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Node.js dependencies
```bash
npm install
```

## Usage

### Option 1: Command Line Interface

Process a single image file:

```bash
python qr_decoder.py path/to/qr_code_image.jpg
```

Save results to a specific file:

```bash
python qr_decoder.py path/to/qr_code_image.jpg output.json
```

### Option 2: Web Interface

1. Start the Node.js bridge server:
```bash
npm start
```

2. In a new terminal, start the Python web server:
```bash
python web_decoder.py
```

3. Open your browser and navigate to `http://localhost:5000`

4. Upload your QR code image using the web interface

### Option 3: API Usage

#### Decode QR code from image:
```bash
curl -X POST -F "image=@qr_code.jpg" http://localhost:3001/decode
```

#### Decode QR data directly:
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"qrData":"your_qr_code_data_here"}' \
  http://localhost:3001/decode-qr
```

#### Health check:
```bash
curl http://localhost:3001/health
```

## API Endpoints

### Node.js Bridge (Port 3001)

- `POST /decode` - Decode QR code from uploaded image
- `POST /decode-qr` - Decode QR data directly
- `GET /health` - Health check endpoint

### Python Web Server (Port 5000)

- `GET /` - Web interface
- `POST /upload` - Upload and process image
- `POST /api/decode` - API endpoint for QR data decoding

## Output Format

The decoder returns structured JSON data:

```json
{
  "success": true,
  "hash": "sha256_hash_of_qr_data",
  "qrData": "original_qr_code_data",
  "vehicleInfo": {
    "registrationNumber": "ABC12345",
    "vin": "1HGBH41JXMN109186",
    "brand": "Honda",
    "model": "Civic",
    "year": "2023",
    "engineCapacity": "1.5L",
    "fuelType": "Petrol",
    "color": "White",
    "registrationDate": "2023-01-15",
    "expiryDate": "2028-01-15",
    "owner": "Jan Kowalski",
    "address": "Warszawa, Poland"
  }
}
```

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- BMP (.bmp)

## Error Handling

The application includes comprehensive error handling for:

- Invalid image files
- Missing QR codes
- Network connectivity issues
- Decoder package errors
- File upload errors

## Development

### Project Structure
```
polish-vehicle-qr-decoder/
├── qr_decoder.py          # Main QR code processing script
├── web_decoder.py         # Flask web application
├── node_bridge.js         # Node.js bridge server
├── package.json           # Node.js dependencies
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html         # Web interface template
├── uploads/               # Temporary upload directory
└── README.md             # This file
```

### Adding New Features

1. **Custom Decoders**: Extend the `PolishVehicleQRDecoder` class
2. **Additional Output Formats**: Modify the output methods in both Python and Node.js components
3. **Enhanced Image Processing**: Add image preprocessing in `read_qr_code_from_image()`

## Troubleshooting

### Common Issues

1. **"Could not connect to Node.js bridge server"**
   - Ensure the Node.js server is running: `npm start`
   - Check if port 3001 is available

2. **"No QR codes found in the image"**
   - Verify the image contains a clear, readable QR code
   - Try improving image quality or lighting

3. **"polish-vehicle-registration-certificate-decoder not found"**
   - Run `npm install` to install dependencies
   - Check if the package is available in npm registry

4. **Import errors in Python**
   - Install missing dependencies: `pip install -r requirements.txt`
   - Ensure you're using Python 3.7+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Uses the `polish-vehicle-registration-certificate-decoder` npm package
- Built with OpenCV, pyzbar, Flask, and Express.js
- Inspired by the need for automated vehicle registration processing
