#!/usr/bin/env python3
"""
Polish Vehicle Registration Certificate Decoder
This module provides functionality to decode Polish vehicle registration certificate data from base64 encoded QR codes.
"""

import base64
import struct
import json
import logging
from typing import Dict, Optional, Any, List
from dataclasses import dataclass
import requests

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class VehicleData:
    """Data class to hold decoded vehicle information."""
    format_id: Optional[str] = None
    series_dr: Optional[str] = None
    territorial_code: Optional[str] = None
    issuing_authority: Optional[List[str]] = None
    registration_number: Optional[str] = None
    vehicle_brand: Optional[str] = None
    vehicle_type: Optional[str] = None
    vehicle_variant: Optional[str] = None
    vehicle_version: Optional[str] = None
    vehicle_model: Optional[str] = None
    vin_number: Optional[str] = None
    issue_date: Optional[str] = None
    validity_period: Optional[str] = None
    owner_full_name: Optional[str] = None
    owner_first_name: Optional[str] = None
    owner_last_name: Optional[str] = None
    owner_company_name: Optional[str] = None
    owner_pesel_regon: Optional[str] = None
    owner_postal_code: Optional[str] = None
    owner_city: Optional[str] = None
    owner_commune: Optional[str] = None
    owner_street: Optional[str] = None
    owner_house_number: Optional[str] = None
    owner_apartment_number: Optional[str] = None
    vehicle_owner_full_name: Optional[str] = None
    vehicle_owner_first_name: Optional[str] = None
    vehicle_owner_last_name: Optional[str] = None
    vehicle_owner_company_name: Optional[str] = None
    vehicle_owner_pesel_regon: Optional[str] = None
    vehicle_owner_postal_code: Optional[str] = None
    vehicle_owner_city: Optional[str] = None
    vehicle_owner_commune: Optional[str] = None
    vehicle_owner_street: Optional[str] = None
    vehicle_owner_house_number: Optional[str] = None
    vehicle_owner_apartment_number: Optional[str] = None
    max_total_weight: Optional[str] = None
    permissible_total_weight: Optional[str] = None
    permissible_total_weight_combination: Optional[str] = None
    vehicle_weight: Optional[str] = None
    vehicle_category: Optional[str] = None
    type_approval_number: Optional[str] = None
    number_of_axles: Optional[str] = None
    max_trailer_weight_with_brakes: Optional[str] = None
    max_trailer_weight_without_brakes: Optional[str] = None
    power_to_weight_ratio: Optional[str] = None
    engine_capacity: Optional[str] = None
    max_net_power: Optional[str] = None
    fuel_type: Optional[str] = None
    fuel_type_description: Optional[str] = None
    first_registration_date: Optional[str] = None
    seating_capacity: Optional[str] = None
    standing_capacity: Optional[str] = None
    vehicle_type_description: Optional[str] = None
    purpose: Optional[str] = None
    production_year: Optional[str] = None
    permissible_load: Optional[str] = None
    max_axle_load: Optional[str] = None
    vehicle_card_number: Optional[str] = None
    identification_code: Optional[str] = None
    type_code: Optional[str] = None
    subtype_code: Optional[str] = None
    purpose_code: Optional[str] = None
    unknown_field_1: Optional[str] = None
    unknown_field_2: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass to a dictionary."""
        return {k: v for k, v in self.__dict__.items() if v is not None}


class PolishVehicleDecoder:
    """
    Decoder for Polish Vehicle Registration Certificate data.
    """
    
    # Fuel type mappings
    FUEL_TYPES = {
        'P': 'benzyna',
        'D': 'olej napędowy',
        'M': 'mieszanka (paliwo-olej)',
        'LPG': 'gaz płynny (propan-butan)',
        'CNG': 'gaz ziemny sprężony (metan)',
        'H': 'wodór',
        'LNG': 'gaz ziemny skroplony (metan)',
        'BD': 'biodiesel',
        'E85': 'etanol',
        'EE': 'energia elektryczna',
        '999': 'inne'
    }
    
    def __init__(self):
        """Initialize the decoder."""
        pass
    
    def decode_base64_data(self, base64_data: str) -> Optional[bytes]:
        """
        Decode base64 data to bytes.
        
        Args:
            base64_data: Base64 encoded string
            
        Returns:
            Decoded bytes or None if decoding failed
        """
        try:
            # Clean the base64 data
            cleaned_data = base64_data.strip()
            
            # Add padding if necessary
            missing_padding = len(cleaned_data) % 4
            if missing_padding:
                cleaned_data += '=' * (4 - missing_padding)
            
            # Decode base64
            decoded_bytes = base64.b64decode(cleaned_data)
            logger.info(f"Successfully decoded {len(decoded_bytes)} bytes from base64")
            return decoded_bytes
            
        except Exception as e:
            logger.error(f"Failed to decode base64 data: {e}")
            return None
    
    def decompress_data(self, compressed_data: bytes) -> Optional[str]:
        """
        Decompress the data using various methods.
        This is a simplified implementation - the actual Polish certificates use NRV2E compression.
        
        Args:
            compressed_data: Compressed binary data
            
        Returns:
            Decompressed string or None if decompression failed
        """
        try:
            # Try different decompression methods
            
            # Method 1: Try to decode as UTF-16LE (common for Polish certificates)
            try:
                decompressed = compressed_data.decode('utf-16le')
                if len(decompressed) > 10:  # Reasonable length check
                    logger.info("Successfully decompressed using UTF-16LE")
                    return decompressed
            except UnicodeDecodeError:
                pass
            
            # Method 2: Try UTF-8
            try:
                decompressed = compressed_data.decode('utf-8')
                if len(decompressed) > 10:
                    logger.info("Successfully decompressed using UTF-8")
                    return decompressed
            except UnicodeDecodeError:
                pass
            
            # Method 3: Try latin-1
            try:
                decompressed = compressed_data.decode('latin-1')
                if len(decompressed) > 10:
                    logger.info("Successfully decompressed using latin-1")
                    return decompressed
            except UnicodeDecodeError:
                pass
            
            # Method 4: Check if it's already text data
            if all(32 <= b <= 126 or b in [9, 10, 13] for b in compressed_data[:100]):
                decompressed = compressed_data.decode('ascii', errors='ignore')
                logger.info("Data appears to be uncompressed ASCII")
                return decompressed
            
            # If all methods fail, return hex representation for debugging
            logger.warning("Could not decompress data, returning hex representation")
            return compressed_data.hex()
            
        except Exception as e:
            logger.error(f"Failed to decompress data: {e}")
            return None
    
    def parse_decompressed_data(self, decompressed_data: str) -> VehicleData:
        """
        Parse the decompressed data into structured vehicle information.
        
        Args:
            decompressed_data: Decompressed string data
            
        Returns:
            VehicleData object with parsed information
        """
        vehicle_data = VehicleData()
        
        try:
            # Check if data is pipe-separated (common format for Polish certificates)
            if '|' in decompressed_data:
                fields = decompressed_data.split('|')
                logger.info(f"Found {len(fields)} pipe-separated fields")
                
                # Map fields based on known structure
                # This mapping is based on the research from GitHub repositories
                if len(fields) >= 66:  # Expected number of fields for new format
                    vehicle_data.format_id = fields[0] if len(fields) > 0 else None
                    vehicle_data.series_dr = fields[1] if len(fields) > 1 else None
                    vehicle_data.territorial_code = fields[2] if len(fields) > 2 else None
                    
                    # Issuing authority (multiple lines)
                    issuing_authority = []
                    for i in range(3, 7):
                        if i < len(fields) and fields[i].strip():
                            issuing_authority.append(fields[i].strip())
                    vehicle_data.issuing_authority = issuing_authority if issuing_authority else None
                    
                    vehicle_data.registration_number = fields[7] if len(fields) > 7 else None
                    vehicle_data.vehicle_brand = fields[8] if len(fields) > 8 else None
                    vehicle_data.vehicle_type = fields[9] if len(fields) > 9 else None
                    vehicle_data.vehicle_variant = fields[10] if len(fields) > 10 else None
                    vehicle_data.vehicle_version = fields[11] if len(fields) > 11 else None
                    vehicle_data.vehicle_model = fields[12] if len(fields) > 12 else None
                    vehicle_data.vin_number = fields[13] if len(fields) > 13 else None
                    vehicle_data.issue_date = fields[14] if len(fields) > 14 else None
                    vehicle_data.validity_period = fields[15] if len(fields) > 15 else None
                    
                    # Owner information
                    vehicle_data.owner_full_name = fields[16] if len(fields) > 16 else None
                    vehicle_data.owner_first_name = fields[17] if len(fields) > 17 else None
                    vehicle_data.owner_last_name = fields[18] if len(fields) > 18 else None
                    vehicle_data.owner_company_name = fields[19] if len(fields) > 19 else None
                    vehicle_data.owner_pesel_regon = fields[20] if len(fields) > 20 else None
                    vehicle_data.owner_postal_code = fields[21] if len(fields) > 21 else None
                    vehicle_data.owner_city = fields[22] if len(fields) > 22 else None
                    vehicle_data.owner_commune = fields[23] if len(fields) > 23 else None
                    vehicle_data.owner_street = fields[24] if len(fields) > 24 else None
                    vehicle_data.owner_house_number = fields[25] if len(fields) > 25 else None
                    vehicle_data.owner_apartment_number = fields[26] if len(fields) > 26 else None
                    
                    # Vehicle owner information (if different from owner)
                    vehicle_data.vehicle_owner_full_name = fields[27] if len(fields) > 27 else None
                    vehicle_data.vehicle_owner_first_name = fields[28] if len(fields) > 28 else None
                    vehicle_data.vehicle_owner_last_name = fields[29] if len(fields) > 29 else None
                    vehicle_data.vehicle_owner_company_name = fields[30] if len(fields) > 30 else None
                    vehicle_data.vehicle_owner_pesel_regon = fields[31] if len(fields) > 31 else None
                    vehicle_data.vehicle_owner_postal_code = fields[32] if len(fields) > 32 else None
                    vehicle_data.vehicle_owner_city = fields[33] if len(fields) > 33 else None
                    vehicle_data.vehicle_owner_commune = fields[34] if len(fields) > 34 else None
                    vehicle_data.vehicle_owner_street = fields[35] if len(fields) > 35 else None
                    vehicle_data.vehicle_owner_house_number = fields[36] if len(fields) > 36 else None
                    vehicle_data.vehicle_owner_apartment_number = fields[37] if len(fields) > 37 else None
                    
                    # Technical data
                    vehicle_data.max_total_weight = fields[38] if len(fields) > 38 else None
                    vehicle_data.permissible_total_weight = fields[39] if len(fields) > 39 else None
                    vehicle_data.permissible_total_weight_combination = fields[40] if len(fields) > 40 else None
                    vehicle_data.vehicle_weight = fields[41] if len(fields) > 41 else None
                    vehicle_data.vehicle_category = fields[42] if len(fields) > 42 else None
                    vehicle_data.type_approval_number = fields[43] if len(fields) > 43 else None
                    vehicle_data.number_of_axles = fields[44] if len(fields) > 44 else None
                    vehicle_data.max_trailer_weight_with_brakes = fields[45] if len(fields) > 45 else None
                    vehicle_data.max_trailer_weight_without_brakes = fields[46] if len(fields) > 46 else None
                    vehicle_data.power_to_weight_ratio = fields[47] if len(fields) > 47 else None
                    vehicle_data.engine_capacity = fields[48] if len(fields) > 48 else None
                    vehicle_data.max_net_power = fields[49] if len(fields) > 49 else None
                    
                    # Fuel type with description
                    fuel_type = fields[50] if len(fields) > 50 else None
                    if fuel_type:
                        vehicle_data.fuel_type = fuel_type.strip()
                        vehicle_data.fuel_type_description = self.FUEL_TYPES.get(fuel_type.strip(), fuel_type.strip())
                    
                    vehicle_data.first_registration_date = fields[51] if len(fields) > 51 else None
                    vehicle_data.seating_capacity = fields[52] if len(fields) > 52 else None
                    vehicle_data.standing_capacity = fields[53] if len(fields) > 53 else None
                    vehicle_data.vehicle_type_description = fields[54] if len(fields) > 54 else None
                    vehicle_data.purpose = fields[55] if len(fields) > 55 else None
                    vehicle_data.production_year = fields[56] if len(fields) > 56 else None
                    vehicle_data.permissible_load = fields[57] if len(fields) > 57 else None
                    vehicle_data.max_axle_load = fields[58] if len(fields) > 58 else None
                    vehicle_data.vehicle_card_number = fields[59] if len(fields) > 59 else None
                    vehicle_data.identification_code = fields[60] if len(fields) > 60 else None
                    vehicle_data.type_code = fields[61] if len(fields) > 61 else None
                    vehicle_data.subtype_code = fields[62] if len(fields) > 62 else None
                    vehicle_data.purpose_code = fields[63] if len(fields) > 63 else None
                    vehicle_data.unknown_field_1 = fields[64] if len(fields) > 64 else None
                    vehicle_data.unknown_field_2 = fields[65] if len(fields) > 65 else None
                    
                else:
                    logger.warning(f"Unexpected number of fields: {len(fields)}, expected 66+")
                    # Store raw data for debugging
                    vehicle_data.format_id = f"RAW_DATA_{len(fields)}_FIELDS"
                    
            else:
                # Try to parse other formats or store as raw data
                logger.info("Data doesn't appear to be pipe-separated, storing as raw")
                vehicle_data.format_id = "RAW_DATA"
                
        except Exception as e:
            logger.error(f"Failed to parse decompressed data: {e}")
            vehicle_data.format_id = "PARSE_ERROR"
        
        return vehicle_data
    
    def decode_certificate(self, base64_data: str) -> Optional[VehicleData]:
        """
        Decode a Polish vehicle registration certificate from base64 data.
        
        Args:
            base64_data: Base64 encoded certificate data
            
        Returns:
            VehicleData object with decoded information or None if decoding failed
        """
        try:
            # Step 1: Decode base64
            compressed_data = self.decode_base64_data(base64_data)
            if compressed_data is None:
                return None
            
            # Step 2: Decompress data
            decompressed_data = self.decompress_data(compressed_data)
            if decompressed_data is None:
                return None
            
            # Step 3: Parse the decompressed data
            vehicle_data = self.parse_decompressed_data(decompressed_data)
            
            logger.info("Successfully decoded Polish vehicle registration certificate")
            return vehicle_data
            
        except Exception as e:
            logger.error(f"Failed to decode certificate: {e}")
            return None
    
    def format_output(self, vehicle_data: VehicleData, output_format: str = 'json') -> str:
        """
        Format the vehicle data for output.
        
        Args:
            vehicle_data: VehicleData object
            output_format: Output format ('json', 'text', 'dict')
            
        Returns:
            Formatted string representation
        """
        try:
            if output_format.lower() == 'json':
                return json.dumps(vehicle_data.to_dict(), indent=2, ensure_ascii=False)
            
            elif output_format.lower() == 'text':
                output = []
                output.append("=== Polish Vehicle Registration Certificate ===")
                output.append("")
                
                data_dict = vehicle_data.to_dict()
                for key, value in data_dict.items():
                    if value is not None:
                        # Format key name
                        formatted_key = key.replace('_', ' ').title()
                        if isinstance(value, list):
                            output.append(f"{formatted_key}: {', '.join(value)}")
                        else:
                            output.append(f"{formatted_key}: {value}")
                
                return '\n'.join(output)
            
            elif output_format.lower() == 'dict':
                return str(vehicle_data.to_dict())
            
            else:
                return json.dumps(vehicle_data.to_dict(), indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Failed to format output: {e}")
            return f"Error formatting output: {e}"


def main():
    """
    Main function for testing the decoder.
    """
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python polish_decoder.py <base64_data>")
        sys.exit(1)
    
    base64_data = sys.argv[1]
    
    # Create decoder instance
    decoder = PolishVehicleDecoder()
    
    # Decode the certificate
    vehicle_data = decoder.decode_certificate(base64_data)
    
    if vehicle_data is None:
        print("Failed to decode the certificate data.")
        return
    
    # Format and print the output
    print(decoder.format_output(vehicle_data, 'text'))
    print("\n" + "="*50 + "\n")
    print("JSON Format:")
    print(decoder.format_output(vehicle_data, 'json'))


if __name__ == "__main__":
    main()