# Polish Vehicle Registration Certificate QR Code Reader and Decoder

A comprehensive Python solution for reading QR codes from images and decoding Polish Vehicle Registration Certificate data. This project combines advanced QR code detection with certificate data parsing to extract detailed vehicle information.

## Features

- **Multi-library QR Code Reading**: Uses QReader, pyzbar, and OpenCV for maximum compatibility
- **Advanced Image Preprocessing**: Multiple preprocessing techniques to improve QR code detection
- **Polish Certificate Decoding**: Specialized decoder for Polish vehicle registration certificates
- **Multiple Output Formats**: JSON, text, and dictionary formats
- **Batch Processing**: Process multiple images at once
- **Comprehensive Logging**: Detailed logging for debugging and monitoring
- **Command-line Interface**: Easy-to-use CLI with various options

## Repository Information

This project is inspired by and based on research from several GitHub repositories:

- [dex4er/js-polish-vehicle-registration-certificate-decoder](https://github.com/dex4er/js-polish-vehicle-registration-certificate-decoder) - JavaScript implementation
- [icedevml/decode-polish-aztec](https://github.com/icedevml/decode-polish-aztec) - C implementation for decoding Aztec codes
- [dex4er/drpdecompress](https://github.com/dex4er/drpdecompress) - Decompression utility

## Installation

### Prerequisites

- Python 3.8 or higher
- System dependencies for QR code reading

### System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y python3-venv python3-pip libzbar0
```

**macOS:**
```bash
brew install zbar
```

**Windows:**
The required DLLs are included with the Python packages.

### Python Environment Setup

1. Clone or download this repository
2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

The main script provides a comprehensive command-line interface:

```bash
# Basic usage - process a single image
python main.py image.jpg

# Specify output format
python main.py image.jpg --format text

# Process multiple images
python main.py image1.jpg image2.jpg image3.jpg

# Save results to file
python main.py image.jpg --output results.json

# Verbose logging
python main.py image.jpg --verbose

# Quiet mode (errors only)
python main.py image.jpg --quiet
```

### Output Formats

#### JSON Format (default)
```json
{
  "format_id": "XXC1",
  "series_dr": "AAA0007046",
  "registration_number": "DMI 1PNK",
  "vehicle_brand": "TOYOTA",
  "vehicle_model": "COROLLA",
  "vin_number": "JTDKM28E100089120",
  "owner_full_name": "KOWALSKI JAN",
  "first_registration_date": "2005-07-01",
  "fuel_type": "P",
  "fuel_type_description": "benzyna"
}
```

#### Text Format
```
=== Polish Vehicle Registration Certificate ===

Format Id: XXC1
Series Dr: AAA0007046
Registration Number: DMI 1PNK
Vehicle Brand: TOYOTA
Vehicle Model: COROLLA
Vin Number: JTDKM28E100089120
Owner Full Name: KOWALSKI JAN
First Registration Date: 2005-07-01
Fuel Type: P
Fuel Type Description: benzyna
```

### Python API

You can also use the components programmatically:

```python
from qr_reader import QRCodeReader
from polish_decoder import PolishVehicleDecoder
from main import PolishVehicleCertificateProcessor

# Using the combined processor
processor = PolishVehicleCertificateProcessor()
result = processor.process_image('path/to/image.jpg', 'json')
print(result)

# Using individual components
qr_reader = QRCodeReader()
decoder = PolishVehicleDecoder()

# Read QR codes from image
qr_codes = qr_reader.read_qr_codes('path/to/image.jpg')

# Extract base64 data
for qr_data in qr_codes:
    base64_data = qr_reader.extract_base64_data(qr_data)
    if base64_data:
        # Decode certificate
        vehicle_data = decoder.decode_certificate(base64_data)
        if vehicle_data:
            print(decoder.format_output(vehicle_data, 'text'))
```

## Technical Details

### QR Code Reading

The system uses three different libraries for maximum compatibility:

1. **QReader**: Advanced QR detection with YOLOv8-based segmentation
2. **pyzbar**: Fast and reliable QR/barcode decoding
3. **OpenCV**: Built-in QR code detection

### Image Preprocessing

Multiple preprocessing techniques are applied to improve detection:

- Gaussian blur for noise reduction
- Adaptive thresholding
- Morphological operations
- Histogram equalization
- Contrast enhancement

### Certificate Decoding

Polish vehicle registration certificates use:

- Base64 encoding for QR code data
- NRV2E compression (simplified implementation)
- Pipe-separated field format
- UTF-16LE encoding for text data

### Supported Data Fields

The decoder extracts over 60 different fields including:

- **Basic Information**: Registration number, VIN, brand, model
- **Owner Details**: Name, address, PESEL/REGON number
- **Technical Data**: Weight, dimensions, engine specifications
- **Administrative**: Issue date, validity period, issuing authority

## File Structure

```
├── main.py                 # Main CLI application
├── qr_reader.py           # QR code reading functionality
├── polish_decoder.py      # Polish certificate decoder
├── requirements.txt       # Python dependencies
├── README.md             # This documentation
└── examples/             # Example images and outputs
```

## Examples

### Example 1: Basic Usage

```bash
python main.py vehicle_qr.jpg
```

Output:
```json
{
  "format_id": "XXC1",
  "registration_number": "WB 12345",
  "vehicle_brand": "VOLKSWAGEN",
  "vehicle_model": "GOLF",
  "owner_full_name": "NOWAK ANNA"
}
```

### Example 2: Multiple Images with Text Output

```bash
python main.py *.jpg --format text --output results.txt
```

### Example 3: Verbose Processing

```bash
python main.py vehicle_qr.jpg --verbose
```

This will show detailed logging of the QR detection and decoding process.

## Troubleshooting

### Common Issues

1. **No QR codes detected**
   - Ensure the image is clear and well-lit
   - Try different image formats (JPG, PNG)
   - Check if the QR code is not too small or distorted

2. **QR code detected but not decoded**
   - The QR code might not contain Polish certificate data
   - Check the QR code content manually

3. **Installation issues**
   - Make sure all system dependencies are installed
   - Use a virtual environment to avoid conflicts

### Debug Mode

Enable verbose logging to see detailed processing information:

```bash
python main.py image.jpg --verbose
```

## Limitations

1. **Compression**: The current implementation uses simplified decompression. Real Polish certificates use NRV2E compression which requires specialized libraries.

2. **Format Support**: Primarily supports the newer certificate format (XXC1). Older formats may require additional parsing logic.

3. **Image Quality**: Very poor quality images or severely distorted QR codes may not be readable.

## Contributing

Contributions are welcome! Please consider:

1. Adding support for proper NRV2E decompression
2. Improving image preprocessing techniques
3. Adding support for older certificate formats
4. Enhancing error handling and user feedback

## License

This project is provided for educational and research purposes. Please respect privacy and data protection laws when processing vehicle registration data.

## Acknowledgments

- [dex4er](https://github.com/dex4er) for the JavaScript implementation and research
- [icedevml](https://github.com/icedevml) for the Aztec code decoding research
- The Polish government for the open format specification
- Contributors to QReader, pyzbar, and OpenCV projects

## Disclaimer

This tool is for educational and research purposes only. Always ensure you have proper authorization before processing vehicle registration documents. The accuracy of decoded data depends on image quality and QR code integrity.
