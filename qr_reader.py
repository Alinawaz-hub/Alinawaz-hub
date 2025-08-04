#!/usr/bin/env python3
"""
QR Code Reader for Polish Vehicle Registration Certificate
This module provides functionality to read QR codes from images and extract base64 data.
"""

import cv2
import numpy as np
from PIL import Image
import base64
import os
from typing import List, Optional, Tuple, Union
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from qreader import QReader
    QREADER_AVAILABLE = True
except ImportError:
    QREADER_AVAILABLE = False
    logger.warning("QReader not available, falling back to pyzbar and OpenCV")

try:
    from pyzbar import pyzbar
    PYZBAR_AVAILABLE = True
except ImportError:
    PYZBAR_AVAILABLE = False
    logger.warning("pyzbar not available")


class QRCodeReader:
    """
    A comprehensive QR code reader that uses multiple methods to decode QR codes from images.
    """
    
    def __init__(self):
        """Initialize the QR code reader with available libraries."""
        self.qreader = None
        self.opencv_detector = None
        
        # Initialize QReader if available
        if QREADER_AVAILABLE:
            try:
                self.qreader = QReader()
                logger.info("QReader initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize QReader: {e}")
                self.qreader = None
        
        # Initialize OpenCV QR detector
        try:
            self.opencv_detector = cv2.QRCodeDetector()
            logger.info("OpenCV QR detector initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize OpenCV QR detector: {e}")
            self.opencv_detector = None
    
    def load_image(self, image_path: str) -> Optional[np.ndarray]:
        """
        Load an image from file path.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            numpy array representing the image, or None if loading failed
        """
        try:
            if not os.path.exists(image_path):
                logger.error(f"Image file does not exist: {image_path}")
                return None
            
            # Try loading with OpenCV first
            image = cv2.imread(image_path)
            if image is not None:
                # Convert BGR to RGB for consistency
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                logger.info(f"Successfully loaded image: {image_path}")
                return image
            
            # Fallback to PIL
            pil_image = Image.open(image_path)
            image = np.array(pil_image)
            if len(image.shape) == 3 and image.shape[2] == 3:
                # Already RGB
                pass
            elif len(image.shape) == 3 and image.shape[2] == 4:
                # RGBA to RGB
                image = image[:, :, :3]
            elif len(image.shape) == 2:
                # Grayscale to RGB
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            
            logger.info(f"Successfully loaded image with PIL: {image_path}")
            return image
            
        except Exception as e:
            logger.error(f"Failed to load image {image_path}: {e}")
            return None
    
    def read_qr_with_qreader(self, image: np.ndarray) -> List[str]:
        """
        Read QR codes using QReader library.
        
        Args:
            image: Input image as numpy array
            
        Returns:
            List of decoded QR code strings
        """
        if not self.qreader:
            return []
        
        try:
            decoded_texts = self.qreader.detect_and_decode(image=image)
            results = []
            
            if decoded_texts:
                for text in decoded_texts:
                    if text is not None:
                        results.append(text)
            
            logger.info(f"QReader found {len(results)} QR codes")
            return results
            
        except Exception as e:
            logger.error(f"QReader failed: {e}")
            return []
    
    def read_qr_with_pyzbar(self, image: np.ndarray) -> List[str]:
        """
        Read QR codes using pyzbar library.
        
        Args:
            image: Input image as numpy array
            
        Returns:
            List of decoded QR code strings
        """
        if not PYZBAR_AVAILABLE:
            return []
        
        try:
            # Convert to PIL Image for pyzbar
            pil_image = Image.fromarray(image)
            decoded_objects = pyzbar.decode(pil_image)
            
            results = []
            for obj in decoded_objects:
                if obj.type in ['QRCODE', 'DATAMATRIX']:
                    try:
                        decoded_text = obj.data.decode('utf-8')
                        results.append(decoded_text)
                    except UnicodeDecodeError:
                        # Try with latin-1 encoding
                        try:
                            decoded_text = obj.data.decode('latin-1')
                            results.append(decoded_text)
                        except Exception:
                            logger.warning("Failed to decode QR code data")
            
            logger.info(f"pyzbar found {len(results)} QR codes")
            return results
            
        except Exception as e:
            logger.error(f"pyzbar failed: {e}")
            return []
    
    def read_qr_with_opencv(self, image: np.ndarray) -> List[str]:
        """
        Read QR codes using OpenCV.
        
        Args:
            image: Input image as numpy array
            
        Returns:
            List of decoded QR code strings
        """
        if not self.opencv_detector:
            return []
        
        try:
            # Convert to grayscale for OpenCV
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image
            
            # Detect and decode QR code
            data, bbox, rectified_image = self.opencv_detector.detectAndDecode(gray)
            
            results = []
            if data:
                results.append(data)
            
            logger.info(f"OpenCV found {len(results)} QR codes")
            return results
            
        except Exception as e:
            logger.error(f"OpenCV QR detection failed: {e}")
            return []
    
    def preprocess_image(self, image: np.ndarray) -> List[np.ndarray]:
        """
        Apply various preprocessing techniques to improve QR code detection.
        
        Args:
            image: Input image as numpy array
            
        Returns:
            List of preprocessed images
        """
        preprocessed = [image]  # Original image
        
        try:
            # Convert to grayscale
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image
            
            # Apply different preprocessing techniques
            
            # 1. Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            preprocessed.append(cv2.cvtColor(blurred, cv2.COLOR_GRAY2RGB))
            
            # 2. Adaptive thresholding
            adaptive_thresh = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
            preprocessed.append(cv2.cvtColor(adaptive_thresh, cv2.COLOR_GRAY2RGB))
            
            # 3. Morphological operations
            kernel = np.ones((3, 3), np.uint8)
            morph = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
            preprocessed.append(cv2.cvtColor(morph, cv2.COLOR_GRAY2RGB))
            
            # 4. Histogram equalization
            equalized = cv2.equalizeHist(gray)
            preprocessed.append(cv2.cvtColor(equalized, cv2.COLOR_GRAY2RGB))
            
            # 5. Contrast enhancement
            enhanced = cv2.convertScaleAbs(gray, alpha=1.2, beta=10)
            preprocessed.append(cv2.cvtColor(enhanced, cv2.COLOR_GRAY2RGB))
            
        except Exception as e:
            logger.warning(f"Preprocessing failed: {e}")
        
        return preprocessed
    
    def read_qr_codes(self, image_path: str) -> List[str]:
        """
        Read QR codes from an image using all available methods.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            List of unique decoded QR code strings
        """
        # Load the image
        image = self.load_image(image_path)
        if image is None:
            return []
        
        all_results = []
        
        # Try different preprocessing approaches
        preprocessed_images = self.preprocess_image(image)
        
        for i, proc_image in enumerate(preprocessed_images):
            logger.info(f"Processing image variant {i+1}/{len(preprocessed_images)}")
            
            # Try QReader
            qreader_results = self.read_qr_with_qreader(proc_image)
            all_results.extend(qreader_results)
            
            # Try pyzbar
            pyzbar_results = self.read_qr_with_pyzbar(proc_image)
            all_results.extend(pyzbar_results)
            
            # Try OpenCV
            opencv_results = self.read_qr_with_opencv(proc_image)
            all_results.extend(opencv_results)
        
        # Remove duplicates while preserving order
        unique_results = []
        seen = set()
        for result in all_results:
            if result not in seen:
                unique_results.append(result)
                seen.add(result)
        
        logger.info(f"Total unique QR codes found: {len(unique_results)}")
        return unique_results
    
    def extract_base64_data(self, qr_data: str) -> Optional[str]:
        """
        Extract base64 data from QR code content.
        
        Args:
            qr_data: Raw QR code data string
            
        Returns:
            Base64 encoded string if found, None otherwise
        """
        try:
            # Check if the entire string is base64
            if self.is_base64(qr_data):
                return qr_data
            
            # Look for base64 patterns in the string
            # Base64 strings are typically long and contain only valid base64 characters
            import re
            
            # Pattern for base64 strings (at least 50 characters)
            base64_pattern = r'[A-Za-z0-9+/]{50,}={0,2}'
            matches = re.findall(base64_pattern, qr_data)
            
            for match in matches:
                if self.is_base64(match):
                    return match
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to extract base64 data: {e}")
            return None
    
    def is_base64(self, s: str) -> bool:
        """
        Check if a string is valid base64.
        
        Args:
            s: String to check
            
        Returns:
            True if valid base64, False otherwise
        """
        try:
            # Remove any whitespace
            s = s.strip()
            
            # Check if length is multiple of 4 (after padding)
            if len(s) % 4 != 0:
                return False
            
            # Try to decode
            decoded = base64.b64decode(s, validate=True)
            
            # Check if it contains reasonable data (not just random bytes)
            if len(decoded) < 10:
                return False
            
            return True
            
        except Exception:
            return False


def main():
    """
    Main function for testing the QR code reader.
    """
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python qr_reader.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    # Create QR reader instance
    reader = QRCodeReader()
    
    # Read QR codes
    qr_codes = reader.read_qr_codes(image_path)
    
    if not qr_codes:
        print("No QR codes found in the image.")
        return
    
    print(f"Found {len(qr_codes)} QR code(s):")
    
    for i, qr_data in enumerate(qr_codes, 1):
        print(f"\nQR Code {i}:")
        print(f"Raw data: {qr_data[:100]}..." if len(qr_data) > 100 else f"Raw data: {qr_data}")
        
        # Try to extract base64 data
        base64_data = reader.extract_base64_data(qr_data)
        if base64_data:
            print(f"Base64 data found: {base64_data[:100]}...")
            print(f"Base64 data length: {len(base64_data)} characters")
        else:
            print("No base64 data detected in this QR code")


if __name__ == "__main__":
    main()