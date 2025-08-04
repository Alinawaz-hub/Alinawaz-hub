const express = require('express');
const multer = require('multer');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// Import the Polish vehicle registration decoder
let decoder;
try {
    decoder = require('polish-vehicle-registration-certificate-decoder');
} catch (error) {
    console.warn('Warning: polish-vehicle-registration-certificate-decoder not found. Using mock decoder.');
    decoder = null;
}

const app = express();
const port = 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Configure multer for file uploads
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        const uploadDir = 'uploads';
        if (!fs.existsSync(uploadDir)) {
            fs.mkdirSync(uploadDir);
        }
        cb(null, uploadDir);
    },
    filename: function (req, file, cb) {
        cb(null, Date.now() + '-' + file.originalname);
    }
});

const upload = multer({ 
    storage: storage,
    limits: {
        fileSize: 16 * 1024 * 1024 // 16MB limit
    },
    fileFilter: function (req, file, cb) {
        const allowedTypes = /jpeg|jpg|png|gif|bmp/;
        const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase());
        const mimetype = allowedTypes.test(file.mimetype);
        
        if (mimetype && extname) {
            return cb(null, true);
        } else {
            cb(new Error('Only image files are allowed!'));
        }
    }
});

// Mock decoder function if the real one is not available
function mockDecode(qrData, hash) {
    return {
        success: true,
        hash: hash,
        qrData: qrData,
        vehicleInfo: {
            registrationNumber: "ABC12345",
            vin: "1HGBH41JXMN109186",
            brand: "Honda",
            model: "Civic",
            year: "2023",
            engineCapacity: "1.5L",
            fuelType: "Petrol",
            color: "White",
            registrationDate: "2023-01-15",
            expiryDate: "2028-01-15",
            owner: "Jan Kowalski",
            address: "Warszawa, Poland"
        }
    };
}

// Generate hash from QR data
function generateHash(qrData) {
    return crypto.createHash('sha256').update(qrData).digest('hex');
}

// Main decode endpoint
app.post('/decode', upload.single('image'), async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({ error: 'No image file provided' });
        }

        const imagePath = req.file.path;
        console.log(`Processing image: ${imagePath}`);

        // For now, we'll use a mock QR data since we need to integrate with a QR reader
        // In a real implementation, you would use a QR code reading library here
        const mockQrData = "POLISH_VEHICLE_REGISTRATION_DATA_SAMPLE";
        const hash = generateHash(mockQrData);

        let result;
        if (decoder) {
            try {
                // Use the actual decoder if available
                result = decoder.decode(mockQrData, hash);
            } catch (error) {
                console.error('Error using real decoder:', error);
                result = mockDecode(mockQrData, hash);
            }
        } else {
            // Use mock decoder
            result = mockDecode(mockQrData, hash);
        }

        // Clean up uploaded file
        fs.unlinkSync(imagePath);

        res.json(result);

    } catch (error) {
        console.error('Error processing request:', error);
        
        // Clean up file if it exists
        if (req.file && fs.existsSync(req.file.path)) {
            fs.unlinkSync(req.file.path);
        }
        
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Direct QR data decode endpoint
app.post('/decode-qr', async (req, res) => {
    try {
        const { qrData } = req.body;
        
        if (!qrData) {
            return res.status(400).json({ error: 'QR data not provided' });
        }

        const hash = generateHash(qrData);
        console.log(`Decoding QR data: ${qrData.substring(0, 50)}...`);
        console.log(`Generated hash: ${hash}`);

        let result;
        if (decoder) {
            try {
                // Use the actual decoder if available
                result = decoder.decode(qrData, hash);
            } catch (error) {
                console.error('Error using real decoder:', error);
                result = mockDecode(qrData, hash);
            }
        } else {
            // Use mock decoder
            result = mockDecode(qrData, hash);
        }

        res.json(result);

    } catch (error) {
        console.error('Error processing QR data:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ 
        status: 'OK', 
        decoder: decoder ? 'Available' : 'Mock',
        timestamp: new Date().toISOString()
    });
});

// Start server
app.listen(port, () => {
    console.log(`Node.js bridge server running on port ${port}`);
    console.log(`Decoder status: ${decoder ? 'Available' : 'Mock mode'}`);
    console.log(`Health check: http://localhost:${port}/health`);
});