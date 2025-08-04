#!/usr/bin/env python3
"""
Polish Vehicle Registration Certificate QR Code Reader and Decoder
Main script that combines QR code reading from images with certificate decoding.
"""

import os
import sys
import argparse
import logging
from typing import List, Optional
import json

from qr_reader import QRCodeReader
from polish_decoder import PolishVehicleDecoder, VehicleData

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PolishVehicleCertificateProcessor:
    """
    Main processor class that combines QR code reading and certificate decoding.
    """
    
    def __init__(self):
        """Initialize the processor with QR reader and decoder."""
        self.qr_reader = QRCodeReader()
        self.decoder = PolishVehicleDecoder()
        logger.info("Polish Vehicle Certificate Processor initialized")
    
    def process_image(self, image_path: str, output_format: str = 'json') -> Optional[str]:
        """
        Process an image containing Polish vehicle registration certificate QR code.
        
        Args:
            image_path: Path to the image file
            output_format: Output format ('json', 'text', 'dict')
            
        Returns:
            Formatted vehicle data or None if processing failed
        """
        try:
            logger.info(f"Processing image: {image_path}")
            
            # Step 1: Read QR codes from the image
            qr_codes = self.qr_reader.read_qr_codes(image_path)
            
            if not qr_codes:
                logger.error("No QR codes found in the image")
                return None
            
            logger.info(f"Found {len(qr_codes)} QR code(s)")
            
            # Step 2: Process each QR code to find vehicle certificate data
            for i, qr_data in enumerate(qr_codes, 1):
                logger.info(f"Processing QR code {i}/{len(qr_codes)}")
                
                # Try to extract base64 data
                base64_data = self.qr_reader.extract_base64_data(qr_data)
                
                if base64_data:
                    logger.info(f"Found base64 data in QR code {i}")
                    
                    # Step 3: Decode the certificate
                    vehicle_data = self.decoder.decode_certificate(base64_data)
                    
                    if vehicle_data:
                        logger.info("Successfully decoded vehicle certificate")
                        return self.decoder.format_output(vehicle_data, output_format)
                    else:
                        logger.warning(f"Failed to decode certificate from QR code {i}")
                else:
                    logger.info(f"No base64 data found in QR code {i}")
                    logger.debug(f"QR code {i} content: {qr_data[:100]}...")
            
            logger.error("No valid Polish vehicle certificate found in any QR code")
            return None
            
        except Exception as e:
            logger.error(f"Failed to process image: {e}")
            return None
    
    def process_multiple_images(self, image_paths: List[str], output_format: str = 'json') -> List[dict]:
        """
        Process multiple images and return results.
        
        Args:
            image_paths: List of image file paths
            output_format: Output format ('json', 'text', 'dict')
            
        Returns:
            List of results with image path and decoded data
        """
        results = []
        
        for image_path in image_paths:
            try:
                result = {
                    'image_path': image_path,
                    'success': False,
                    'data': None,
                    'error': None
                }
                
                decoded_data = self.process_image(image_path, output_format)
                
                if decoded_data:
                    result['success'] = True
                    result['data'] = decoded_data
                else:
                    result['error'] = "Failed to decode certificate from image"
                
                results.append(result)
                
            except Exception as e:
                results.append({
                    'image_path': image_path,
                    'success': False,
                    'data': None,
                    'error': str(e)
                })
        
        return results
    
    def save_results_to_file(self, results: str, output_file: str) -> bool:
        """
        Save results to a file.
        
        Args:
            results: Results string to save
            output_file: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(results)
            logger.info(f"Results saved to: {output_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to save results to file: {e}")
            return False


def main():
    """
    Main function with command-line interface.
    """
    parser = argparse.ArgumentParser(
        description='Polish Vehicle Registration Certificate QR Code Reader and Decoder',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py image.jpg
  python main.py image.jpg --format text
  python main.py image1.jpg image2.jpg --output results.json
  python main.py *.jpg --format text --output results.txt
        """
    )
    
    parser.add_argument(
        'images',
        nargs='+',
        help='Path(s) to image file(s) containing QR codes'
    )
    
    parser.add_argument(
        '--format', '-f',
        choices=['json', 'text', 'dict'],
        default='json',
        help='Output format (default: json)'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output file path (if not specified, prints to stdout)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress all logging except errors'
    )
    
    args = parser.parse_args()
    
    # Configure logging based on arguments
    if args.quiet:
        logging.getLogger().setLevel(logging.ERROR)
    elif args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Validate input files
    valid_images = []
    for image_path in args.images:
        if os.path.exists(image_path):
            valid_images.append(image_path)
        else:
            logger.error(f"Image file not found: {image_path}")
    
    if not valid_images:
        logger.error("No valid image files found")
        sys.exit(1)
    
    # Create processor
    processor = PolishVehicleCertificateProcessor()
    
    try:
        if len(valid_images) == 1:
            # Single image processing
            result = processor.process_image(valid_images[0], args.format)
            
            if result:
                if args.output:
                    processor.save_results_to_file(result, args.output)
                else:
                    print(result)
            else:
                logger.error("Failed to process the image")
                sys.exit(1)
        
        else:
            # Multiple images processing
            results = processor.process_multiple_images(valid_images, args.format)
            
            # Format results for output
            if args.format == 'json':
                output = json.dumps(results, indent=2, ensure_ascii=False)
            else:
                output_lines = []
                for result in results:
                    output_lines.append(f"=== {result['image_path']} ===")
                    if result['success']:
                        output_lines.append(result['data'])
                    else:
                        output_lines.append(f"Error: {result['error']}")
                    output_lines.append("")
                output = '\n'.join(output_lines)
            
            if args.output:
                processor.save_results_to_file(output, args.output)
            else:
                print(output)
    
    except KeyboardInterrupt:
        logger.info("Processing interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()