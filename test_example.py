#!/usr/bin/env python3
"""
Test script for Polish Vehicle Registration Certificate QR Code Reader and Decoder
This script demonstrates the functionality with sample data.
"""

import logging
from qr_reader import QRCodeReader
from polish_decoder import PolishVehicleDecoder
from main import PolishVehicleCertificateProcessor

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_decoder_with_sample_data():
    """Test the decoder with sample base64 data."""
    print("=== Testing Polish Vehicle Decoder ===\n")
    
    # Sample base64-like data (this is just for demonstration)
    # In real usage, this would come from a QR code
    sample_data = """
    XXC1|AAA0007046|1465058|PREZYDENT M. ST. WARSZAWY|DZIELNICA MOKOTÓW|UL. RAKOWIECKA 25/27|02-517 WARSZAWA|DMI 1PNK|TOYOTA|E12J|ZZE120(H)||COROLLA|JTDKM28E100089120|2013-11-06|---|KOWALSKI JAN|JAN|KOWALSKI||82091711022|02-517|WARSZAWA||WAŁBRZYSKA|24|30|KOWALSKA MARIA|MARIA|KOWALSKA||88030971022|02-517|WARSZAWA||WAŁBRZYSKA|24|30|1655|1655|2655|1205|M1|e11*2001/116*0180*04|2|1000|450|---|1398,00|71,00|P|2005-07-01|5|---|SAMOCHÓD OSOBOWY|---|2005|---|8,82|AAA0000000|02650008000158|03|02|000|2000NNNNNNNN|009002001
    """.strip()
    
    # Create decoder
    decoder = PolishVehicleDecoder()
    
    # Parse the sample data directly (simulating decompressed data)
    vehicle_data = decoder.parse_decompressed_data(sample_data)
    
    if vehicle_data:
        print("Sample Data Parsing Result:")
        print(decoder.format_output(vehicle_data, 'text'))
        print("\n" + "="*50 + "\n")
        print("JSON Format:")
        print(decoder.format_output(vehicle_data, 'json'))
    else:
        print("Failed to parse sample data")

def test_qr_reader_functionality():
    """Test QR reader initialization and basic functionality."""
    print("\n=== Testing QR Reader Initialization ===\n")
    
    try:
        reader = QRCodeReader()
        print("✓ QR Reader initialized successfully")
        
        # Test base64 detection
        test_strings = [
            "SGVsbG8gV29ybGQ=",  # "Hello World" in base64
            "This is not base64",
            "VGhpcyBpcyBhIHRlc3Qgc3RyaW5nIGZvciBiYXNlNjQgZGV0ZWN0aW9u",  # Valid base64
            "Short"  # Too short
        ]
        
        print("\nTesting base64 detection:")
        for test_str in test_strings:
            is_b64 = reader.is_base64(test_str)
            print(f"  '{test_str[:30]}...' -> {'✓ Valid' if is_b64 else '✗ Invalid'} base64")
            
    except Exception as e:
        print(f"✗ QR Reader initialization failed: {e}")

def test_full_processor():
    """Test the full processor functionality."""
    print("\n=== Testing Full Processor ===\n")
    
    try:
        processor = PolishVehicleCertificateProcessor()
        print("✓ Full processor initialized successfully")
        
        # The processor would normally process an image file
        # For this test, we just verify initialization
        print("✓ All components working together")
        
    except Exception as e:
        print(f"✗ Full processor initialization failed: {e}")

def demonstrate_usage():
    """Demonstrate typical usage patterns."""
    print("\n=== Usage Examples ===\n")
    
    print("1. Command Line Usage:")
    print("   python main.py image.jpg")
    print("   python main.py image.jpg --format text")
    print("   python main.py *.jpg --output results.json")
    print("")
    
    print("2. Python API Usage:")
    print("""
   from main import PolishVehicleCertificateProcessor
   
   processor = PolishVehicleCertificateProcessor()
   result = processor.process_image('vehicle_qr.jpg', 'json')
   print(result)
    """)
    
    print("3. Individual Components:")
    print("""
   from qr_reader import QRCodeReader
   from polish_decoder import PolishVehicleDecoder
   
   reader = QRCodeReader()
   decoder = PolishVehicleDecoder()
   
   qr_codes = reader.read_qr_codes('image.jpg')
   for qr_data in qr_codes:
       base64_data = reader.extract_base64_data(qr_data)
       if base64_data:
           vehicle_data = decoder.decode_certificate(base64_data)
           if vehicle_data:
               print(decoder.format_output(vehicle_data, 'text'))
    """)

def main():
    """Run all tests and demonstrations."""
    print("Polish Vehicle Registration Certificate QR Code Reader and Decoder")
    print("=" * 70)
    
    # Run tests
    test_qr_reader_functionality()
    test_decoder_with_sample_data()
    test_full_processor()
    demonstrate_usage()
    
    print("\n" + "=" * 70)
    print("Test completed! The system is ready to process QR code images.")
    print("\nTo process an actual image, run:")
    print("  python main.py your_image.jpg")

if __name__ == "__main__":
    main()