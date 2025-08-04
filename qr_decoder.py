#!/usr/bin/env python3
"""
Polish Vehicle Registration Certificate QR Code Decoder

This script processes QR code images from Polish vehicle registration certificates
and uses the polish-vehicle-registration-certificate-decoder package to extract
vehicle information.
"""

import cv2
import numpy as np
from pyzbar import pyzbar
from PIL import Image
import requests
import json
import os
import sys
from typing import Optional, Dict, Any
import hashlib


class PolishVehicleQRDecoder:
    """Main class for decoding Polish vehicle registration QR codes."""
    
    def __init__(self):
        """Initialize the decoder."""
        self.base_url = "https://www.jsdelivr.com/package/npm/polish-vehicle-registration-certificate-decoder"
        self.api_endpoint = "https://api.jsdelivr.com/v1/package/npm/polish-vehicle-registration-certificate-decoder"
    
    def read_qr_code_from_image(self, image_path: str) -> Optional[str]:
        """
        Read QR code from an image file.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            Optional[str]: QR code data if found, None otherwise
        """
        try:
            # Read image using OpenCV
            image = cv2.imread(image_path)
            if image is None:
                print(f"Error: Could not read image from {image_path}")
                return None
            
            # Convert to grayscale for better QR detection
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect QR codes
            qr_codes = pyzbar.decode(gray)
            
            if not qr_codes:
                print("No QR codes found in the image")
                return None
            
            # Return the first QR code data
            qr_data = qr_codes[0].data.decode('utf-8')
            print(f"QR Code detected: {qr_data[:50]}...")
            return qr_data
            
        except Exception as e:
            print(f"Error reading QR code: {e}")
            return None
    
    def generate_qr_hash(self, qr_data: str) -> str:
        """
        Generate hash from QR code data.
        
        Args:
            qr_data (str): Raw QR code data
            
        Returns:
            str: Hash of the QR code data
        """
        return hashlib.sha256(qr_data.encode()).hexdigest()
    
    def decode_vehicle_data(self, qr_data: str) -> Optional[Dict[str, Any]]:
        """
        Decode vehicle registration data using the Polish decoder package via Node.js bridge.
        
        Args:
            qr_data (str): QR code data
            
        Returns:
            Optional[Dict[str, Any]]: Decoded vehicle information
        """
        try:
            # Generate hash
            qr_hash = self.generate_qr_hash(qr_data)
            
            # Prepare request data
            request_data = {
                "qrData": qr_data
            }
            
            # Make request to the Node.js bridge
            response = requests.post(
                "http://localhost:3001/decode-qr",
                json=request_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"Successfully decoded QR data with hash: {qr_hash}")
                return result
            else:
                print(f"Error from Node.js bridge: {response.status_code} - {response.text}")
                return None
            
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to Node.js bridge server. Make sure it's running on port 3001.")
            return None
        except Exception as e:
            print(f"Error decoding vehicle data: {e}")
            return None
    
    def process_image(self, image_path: str) -> Optional[Dict[str, Any]]:
        """
        Process an image file and return decoded vehicle information.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            Optional[Dict[str, Any]]: Decoded vehicle information
        """
        print(f"Processing image: {image_path}")
        
        # Check if file exists
        if not os.path.exists(image_path):
            print(f"Error: Image file not found: {image_path}")
            return None
        
        # Read QR code
        qr_data = self.read_qr_code_from_image(image_path)
        if qr_data is None:
            return None
        
        # Decode vehicle data
        vehicle_info = self.decode_vehicle_data(qr_data)
        return vehicle_info
    
    def save_results(self, results: Dict[str, Any], output_file: str = "vehicle_data.json"):
        """
        Save decoded results to a JSON file.
        
        Args:
            results (Dict[str, Any]): Decoded vehicle information
            output_file (str): Output file path
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"Results saved to: {output_file}")
        except Exception as e:
            print(f"Error saving results: {e}")


def main():
    """Main function to run the QR code decoder."""
    if len(sys.argv) < 2:
        print("Usage: python qr_decoder.py <image_path> [output_file]")
        print("Example: python qr_decoder.py qr_code.jpg vehicle_info.json")
        sys.exit(1)
    
    image_path = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "vehicle_data.json"
    
    # Initialize decoder
    decoder = PolishVehicleQRDecoder()
    
    # Process image
    results = decoder.process_image(image_path)
    
    if results:
        print("\n" + "="*50)
        print("DECODED VEHICLE INFORMATION")
        print("="*50)
        print(json.dumps(results, indent=2, ensure_ascii=False))
        
        # Save results
        decoder.save_results(results, output_file)
    else:
        print("Failed to process image or decode QR code data")


if __name__ == "__main__":
    main()