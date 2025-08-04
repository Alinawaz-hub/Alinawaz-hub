#!/usr/bin/env python3
"""
Test script to verify the Polish Vehicle QR Decoder setup.
"""

import sys
import requests
import json
from qr_decoder import PolishVehicleQRDecoder

def test_python_dependencies():
    """Test if all Python dependencies are available."""
    print("Testing Python dependencies...")
    
    try:
        import cv2
        print("✅ OpenCV imported successfully")
    except ImportError:
        print("❌ OpenCV not found. Run: pip install opencv-python")
        return False
    
    try:
        from pyzbar import pyzbar
        print("✅ pyzbar imported successfully")
    except ImportError:
        print("❌ pyzbar not found. Run: pip install pyzbar")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow imported successfully")
    except ImportError:
        print("❌ Pillow not found. Run: pip install Pillow")
        return False
    
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError:
        print("❌ requests not found. Run: pip install requests")
        return False
    
    return True

def test_node_bridge():
    """Test if the Node.js bridge server is running."""
    print("\nTesting Node.js bridge server...")
    
    try:
        response = requests.get("http://localhost:3001/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Node.js bridge server is running")
            print(f"   Status: {data.get('status', 'Unknown')}")
            print(f"   Decoder: {data.get('decoder', 'Unknown')}")
            return True
        else:
            print(f"❌ Node.js bridge server returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Node.js bridge server")
        print("   Make sure to run: npm start")
        return False
    except Exception as e:
        print(f"❌ Error testing Node.js bridge: {e}")
        return False

def test_qr_decoder():
    """Test the QR decoder functionality."""
    print("\nTesting QR decoder functionality...")
    
    try:
        decoder = PolishVehicleQRDecoder()
        print("✅ PolishVehicleQRDecoder initialized successfully")
        
        # Test hash generation
        test_data = "test_qr_data"
        hash_result = decoder.generate_qr_hash(test_data)
        print(f"✅ Hash generation works: {hash_result[:20]}...")
        
        return True
    except Exception as e:
        print(f"❌ Error testing QR decoder: {e}")
        return False

def test_mock_decoding():
    """Test mock decoding functionality."""
    print("\nTesting mock decoding...")
    
    try:
        decoder = PolishVehicleQRDecoder()
        test_qr_data = "POLISH_VEHICLE_REGISTRATION_DATA_SAMPLE"
        
        result = decoder.decode_vehicle_data(test_qr_data)
        
        if result and result.get('success'):
            print("✅ Mock decoding works")
            print(f"   Vehicle info: {result.get('vehicleInfo', {}).get('brand', 'Unknown')} {result.get('vehicleInfo', {}).get('model', 'Unknown')}")
            return True
        else:
            print("❌ Mock decoding failed")
            return False
            
    except Exception as e:
        print(f"❌ Error testing mock decoding: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("Polish Vehicle QR Decoder - Setup Test")
    print("=" * 50)
    
    tests = [
        ("Python Dependencies", test_python_dependencies),
        ("QR Decoder", test_qr_decoder),
        ("Node.js Bridge", test_node_bridge),
        ("Mock Decoding", test_mock_decoding),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} test failed")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready to use.")
        print("\nNext steps:")
        print("1. Start the web interface: python web_decoder.py")
        print("2. Open http://localhost:5000 in your browser")
        print("3. Upload a QR code image to test")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Install missing dependencies: pip install -r requirements.txt")
        print("2. Install Node.js dependencies: npm install")
        print("3. Start Node.js bridge: npm start")
    
    print("=" * 50)

if __name__ == "__main__":
    main()