# High Performance Weapon Detection System

A real-time computer vision system for detecting potentially dangerous objects like knives, guns , and other weapons using webcams or video feeds.

## Overview

This weapon detection system uses YOLOv5 and computer vision to identify potentially dangerous objects in real-time video. When a weapon is detected, the system triggers an alarm and saves images of the detected weapons for later review.

## Features

- **Real-time Detection**: Monitors video feed for weapons with minimal latency
- **High FPS Performance**: Optimized for maximum frames-per-second on consumer hardware
- **Multiple Weapon Classes**: Detects knives, scissors, guns, and other potential weapons
- **Audio Alarm**: Sounds an alert when weapons are detected
- **Image Capture**: Automatically saves timestamped images of detected weapons
- **GPU Acceleration**: CUDA support for faster processing on NVIDIA GPUs
- **Adjustable Sensitivity**: Toggle between normal and high sensitivity modes
- **Detection History**: Uses temporal information to reduce false positives and negatives

## Requirements

- Python 3.7+
- OpenCV
- PyTorch
- NumPy
- PyGame
- CUDA-compatible GPU (recommended but not required)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/weapon-detection-system.git
   cd weapon-detection-system
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Make sure you have a working webcam connected to your system.

## Usage

Run the main script to start the weapon detection system:

```
python weapon_detection.py
```

### Controls

- **Q**: Quit the application
- **S**: Toggle between normal and high sensitivity detection modes

## Configuration

You can modify various parameters in the `WeaponDetectionSystem` class initialization:

- `model.conf`: Change the confidence threshold (lower = more sensitive)
- `process_every_n_frames`: Adjust how many frames to skip between processing (higher = more FPS, less accuracy)
- `self.weapon_classes`: Customize which objects to detect as weapons

## Performance Optimization

The system includes several optimizations for maximum performance:

- Half-precision (FP16) inference on CUDA devices
- Pre-allocated memory buffers
- Selective frame processing
- CUDNN benchmark mode
- Reduced inference resolution
- Optimized rendering

## Troubleshooting

**Low FPS**:
- Reduce resolution by changing the resize parameters
- Process fewer frames by increasing `process_every_n_frames`
- Use a GPU if available

**False Positives**:
- Increase the confidence threshold (`model.conf`)
- Add problematic objects to an ignore list

**False Negatives**:
- Decrease the confidence threshold
- Add missing weapon types to the `weapon_classes` list
- Use high sensitivity mode by pressing 'S'

## Disclaimer

This system is intended for educational and security purposes only. It is not guaranteed to detect all weapons in all circumstances and should not be solely relied upon for critical security applications. Always combine automated systems with human supervision for best results.

## License

MIT License

## Acknowledgements

- YOLOv5 by Ultralytics
- OpenCV community
- PyTorch team