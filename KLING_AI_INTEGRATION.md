# Kling AI Integration for Video Generation

This document describes the integration of Kling AI API for video generation in the JEG Design Extract application.

## Overview

The application has been updated to use Kling AI instead of Gemini for video generation functionality. Kling AI provides high-quality image-to-video generation capabilities.

## Changes Made

### 1. Video Gen Tab Unlocked
- Removed the lock on the Video Gen tab
- Users can now access video generation functionality

### 2. Kling AI Client (`kling_client.py`)
- New client module for Kling AI API integration
- Supports JWT authentication
- Image-to-video generation with customizable parameters
- Automatic video download and local storage

### 3. Account Tab Updates (`account_tab.py`)
- Added Kling AI API key configuration section
- Separate fields for Access Key and Secret Key
- Test, Save, and Clear functionality for Kling keys
- Status indicators for configuration state

### 4. Main Application Updates (`jeg_design_extract.py`)
- Added Kling API key variables and loading methods
- Replaced Gemini video generation with Kling AI implementation
- Updated video generation workflow to use Kling AI API

## API Configuration

### Kling AI API Keys
The application requires two API keys from Kling AI:

1. **Access Key**: `AQ3tr3gyBCkK8KKQaM9eH9DAL9hmnTAm`
2. **Secret Key**: `rkdCtNMdQFnGnPReQEaNbGGMTyKHJeyL`

### Setting Up API Keys

#### Method 1: Through the Application
1. Launch the JEG Design Studio application
2. Login with your credentials
3. Go to the Account tab
4. Scroll down to "API Key Configuration"
5. Find the "Kling AI API Keys (for Video Generation)" section
6. Enter the Access Key and Secret Key
7. Click "💾 Save Kling Keys"
8. Optionally click "🧪 Test Kling" to verify the connection

#### Method 2: Using Setup Script
```bash
python setup_kling_keys.py
```

## Video Generation Workflow

### New Kling AI Workflow
1. User uploads an image in the Video Gen tab
2. User clicks "Generate Script" to auto-create script from image analysis (NEW)
3. User reviews/edits the generated script or enters custom script/prompt
4. User clicks "🎬 Generate Video"
5. Application processes and sends request to Kling AI API with:
   - Image automatically cropped to 9:16 aspect ratio (vertical format)
   - Image converted to base64
   - Text prompt
   - Model: kling-v2-5-turbo
   - Mode: pro (professional)
   - Duration: 10 seconds
6. Kling AI processes the request (may take several minutes)
7. Application downloads the generated video
8. Video is displayed in the UI and available for saving

### Key Differences from Gemini
- **Single Video**: Generates one 10-second video (vs. dual 8-second videos)
- **Different Models**: Uses Kling AI v2.5 Turbo instead of Gemini Veo3
- **URL-based**: Videos are generated and provided via download URLs
- **Professional Quality**: Uses professional mode for higher quality output
- **Mobile Optimized**: Automatically crops images to 9:16 aspect ratio for vertical video
- **AI-Powered Scripts**: Uses Gemini AI to analyze images and generate contextual scripts

## Technical Details

### Kling AI API Specifications
- **Base URL**: `https://api-singapore.klingai.com`
- **Authentication**: JWT tokens with HS256 algorithm
- **Image Format**: Base64 encoded (JPEG/PNG)
- **Video Output**: MP4 format (9:16 aspect ratio)
- **Maximum Image Size**: 10MB
- **Minimum Dimensions**: 300px width/height
- **Aspect Ratio**: Automatically cropped to 9:16 (0.5625) for mobile optimization
- **Image Processing**: Smart center cropping preserves main subject

### Supported Parameters
- `model_name`: kling-v1, kling-v1-5, kling-v1-6, etc.
- `mode`: std (standard), pro (professional)
- `duration`: 5 or 10 seconds
- `cfg_scale`: 0.0 to 1.0 (flexibility control)
- `prompt`: Text description (max 2500 characters)

## File Structure

```
Clone_Design/
├── kling_client.py              # Kling AI API client
├── account_tab.py               # Updated with Kling API key fields
├── jeg_design_extract.py        # Main app with Kling integration
├── setup_kling_keys.py          # Setup utility script
├── test_kling_integration.py    # Integration test script
└── KLING_AI_INTEGRATION.md      # This documentation
```

## Dependencies

The Kling AI integration requires the following Python packages:
- `PyJWT` - For JWT token generation
- `requests` - For HTTP API calls
- `Pillow` - For image processing
- `base64` - For image encoding (built-in)

Install missing dependencies:
```bash
pip install PyJWT requests Pillow
```

## Testing

### Run Integration Tests
```bash
python test_kling_integration.py
```

This will test:
- Kling client functionality
- Image conversion capabilities
- User manager API key storage
- Connection to Kling AI API

### Manual Testing
1. Configure API keys in the Account tab
2. Go to Video Gen tab
3. Upload an image
4. Enter a prompt (or use default)
5. Click Generate Video
6. Wait for processing (typically 1-3 minutes)
7. Verify video is generated and playable

## Troubleshooting

### Common Issues

1. **"Kling AI API keys are required"**
   - Solution: Configure API keys in Account tab

2. **"Connection test failed"**
   - Check internet connection
   - Verify API keys are correct
   - Ensure Kling AI service is available

3. **"Video generation failed"**
   - Check image format and size
   - Verify prompt length (max 2500 characters)
   - Check API rate limits

4. **"Failed to download video"**
   - Check internet connection
   - Verify sufficient disk space
   - Check firewall/proxy settings

### Debug Information
- Check console output for detailed error messages
- Video generation logs are displayed in the Video Gen tab
- API responses include error codes and messages

## Cost Considerations

- **Current Configuration**: Professional mode (pro) with 10-second duration
- **Model**: kling-v2-5-turbo (latest and fastest model)
- **Quality**: Higher quality output but more expensive than standard mode
- **Duration**: 10-second videos cost more than 5-second videos
- Usage is tracked and recorded for billing purposes

## Security Notes

- API keys are stored securely using the existing user manager system
- Keys are masked in the UI (shown as asterisks)
- JWT tokens have 30-minute expiration for security
- Video URLs from Kling AI expire after 30 days

## Future Enhancements

Potential improvements for future versions:
- Support for professional mode toggle
- 10-second video option
- Advanced camera control features
- Motion brush functionality
- Batch video generation
- Custom model selection

## Support

For issues related to:
- **Kling AI API**: Check Kling AI documentation at https://app.klingai.com/global/dev/document-api
- **Application Integration**: Review this documentation and test scripts
- **General Application**: Refer to main application documentation
