#!/usr/bin/env python3
"""
Script to process the user's QR code image for Polish Vehicle Registration Certificate decoding.
"""

import os
import sys
import json
import base64
from PIL import Image
import io
from main import PolishVehicleCertificateProcessor

def extract_image_from_notebook(notebook_path="imag_processing_pynb.ipynb"):
    """
    Extract image data from Jupyter notebook if it contains embedded images.
    """
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_content = f.read()
        
        # Parse the notebook JSON
        notebook_data = json.loads(notebook_content)
        
        # Look for image outputs in cells
        for cell in notebook_data.get('cells', []):
            if cell.get('cell_type') == 'code':
                outputs = cell.get('outputs', [])
                for output in outputs:
                    if 'data' in output:
                        data = output['data']
                        if 'image/png' in data:
                            # Found a PNG image
                            image_data = data['image/png']
                            # Decode base64 image
                            image_bytes = base64.b64decode(image_data)
                            # Save as temporary file
                            temp_image_path = 'temp_extracted_image.png'
                            with open(temp_image_path, 'wb') as img_file:
                                img_file.write(image_bytes)
                            print(f"✓ Extracted image from notebook: {temp_image_path}")
                            return temp_image_path
        
        print("⚠️  No embedded images found in notebook")
        return None
        
    except Exception as e:
        print(f"❌ Failed to extract image from notebook: {e}")
        return None

def find_user_image():
    """
    Find the user's QR code image in various possible locations.
    """
    # Possible image file names and locations
    possible_images = [
        "test1.jpeg",
        "test1.jpg", 
        "qr_code.jpg",
        "qr_code.jpeg",
        "qr_code.png",
        "vehicle_qr.jpg",
        "vehicle_qr.jpeg",
        "vehicle_qr.png",
        "image.jpg",
        "image.jpeg",
        "image.png"
    ]
    
    print("🔍 Searching for your QR code image...")
    
    # Check current directory
    for image_name in possible_images:
        if os.path.exists(image_name):
            print(f"✓ Found image: {image_name}")
            return image_name
    
    # Try to extract from notebook
    extracted_image = extract_image_from_notebook()
    if extracted_image:
        return extracted_image
    
    print("❌ Could not find your QR code image.")
    print("\nPlease ensure your image is in the current directory with one of these names:")
    for name in possible_images:
        print(f"  - {name}")
    
    return None

def process_image(image_path):
    """
    Process the QR code image and decode Polish vehicle certificate data.
    """
    print(f"\n🚀 Processing QR code image: {image_path}")
    print("="*60)
    
    # Create processor
    processor = PolishVehicleCertificateProcessor()
    
    # Process the image
    result = processor.process_image(image_path, 'json')
    
    if result:
        print("✅ SUCCESS! Polish vehicle certificate decoded:")
        print("\n" + "="*60)
        print("DECODED VEHICLE DATA:")
        print("="*60)
        
        # Parse JSON to make it more readable
        try:
            data = json.loads(result)
            
            # Display key information
            key_fields = [
                ('Registration Number', 'registration_number'),
                ('Vehicle Brand', 'vehicle_brand'), 
                ('Vehicle Model', 'vehicle_model'),
                ('VIN Number', 'vin_number'),
                ('Owner Name', 'owner_full_name'),
                ('First Registration', 'first_registration_date'),
                ('Fuel Type', 'fuel_type_description'),
                ('Engine Capacity', 'engine_capacity'),
                ('Vehicle Category', 'vehicle_category')
            ]
            
            print("\n📋 KEY INFORMATION:")
            print("-" * 40)
            for label, field in key_fields:
                value = data.get(field, 'N/A')
                if value and value != 'N/A':
                    print(f"{label:20}: {value}")
            
            print(f"\n📄 COMPLETE DATA (JSON):")
            print("-" * 40)
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
        except json.JSONDecodeError:
            print(result)
            
    else:
        print("❌ FAILED to decode Polish vehicle certificate")
        print("\nPossible reasons:")
        print("1. The QR code doesn't contain Polish vehicle certificate data")
        print("2. The QR code is damaged or unclear")
        print("3. The image quality is too poor")
        print("4. The QR code contains data in an unsupported format")
        
        print(f"\n🔍 Let's check what the QR code actually contains...")
        
        # Try to read the QR code content anyway
        from qr_reader import QRCodeReader
        reader = QRCodeReader()
        qr_codes = reader.read_qr_codes(image_path)
        
        if qr_codes:
            print(f"\n📱 QR Code Content Found ({len(qr_codes)} code(s)):")
            for i, qr_data in enumerate(qr_codes, 1):
                print(f"\nQR Code {i}:")
                print(f"Content: {qr_data[:200]}{'...' if len(qr_data) > 200 else ''}")
                print(f"Length: {len(qr_data)} characters")
                
                # Check if it contains base64-like data
                base64_data = reader.extract_base64_data(qr_data)
                if base64_data:
                    print(f"Base64 data found: {len(base64_data)} characters")
                else:
                    print("No base64 data detected")
        else:
            print("❌ No QR codes detected in the image")

def main():
    """
    Main function to process the user's QR code image.
    """
    print("🇵🇱 Polish Vehicle Registration Certificate QR Code Processor")
    print("=" * 65)
    
    # Check if image path provided as argument
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        if os.path.exists(image_path):
            process_image(image_path)
            return
        else:
            print(f"❌ Image file not found: {image_path}")
    
    # Try to find the user's image automatically
    image_path = find_user_image()
    
    if image_path:
        process_image(image_path)
    else:
        print("\n💡 USAGE:")
        print("1. Place your QR code image in this directory")
        print("2. Run: python process_your_image.py")
        print("   OR: python process_your_image.py your_image.jpg")
        
        print("\n📝 SUPPORTED FORMATS:")
        print("- JPG/JPEG")
        print("- PNG") 
        print("- GIF")
        print("- BMP")
        
        print("\n🎯 FOR BEST RESULTS:")
        print("- Ensure the QR code is clear and well-lit")
        print("- The QR code should be reasonably large in the image")
        print("- Avoid blurry or distorted images")

if __name__ == "__main__":
    main()