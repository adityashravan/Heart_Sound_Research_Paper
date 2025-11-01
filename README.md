# Heart Sound Classifier GUI for Raspberry Pi 5

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi%205-red)](https://www.raspberrypi.com/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/status-Active-success)](https://github.com/adityashravan/Heart_Sound_Research_Paper)

A lightweight Tkinter-based GUI application for classifying heart sounds using a Random Forest model with wavelet-based feature extraction. Optimized for Raspberry Pi 5 with MHS 35 LCD display (320x480), but works on any platform.

## 📸 Screenshots

![Heart Sound Classifier GUI](docs/gui_screenshot.png)
*Main interface optimized for 320x480 touchscreen displays*

## 🎯 Key Features

- 🎯 Simple, touch-friendly interface for small displays
- 📁 Browse WAV files from filesystem
- 📂 Quick selection from organized dataset
- 🔍 Real-time heart sound classification
- 💚 Minimal resource usage (perfect for Raspberry Pi)
- 🎨 Clean, readable UI optimized for 320x480 resolution

## 📋 Classified Conditions

| Code | Condition | Description |
|------|-----------|-------------|
| **N** | Normal | Healthy heart sounds |
| **AS** | Aortic Stenosis | Narrowing of the aortic valve |
| **MR** | Mitral Regurgitation | Leaky mitral valve |
| **MS** | Mitral Stenosis | Narrowing of the mitral valve |
| **MVP** | Mitral Valve Prolapse | Improper closure of mitral valve |

## 🔬 Technical Details

### Signal Preprocessing Pipeline
1. **Load WAV file** (any sample rate)
2. **Downsample** to 1 kHz
3. **High-pass filter** - Butterworth (4th order, 20 Hz cutoff)
4. **Z-score normalization** - Mean=0, Std=1
5. **Pad/trim** to 3 seconds (3000 samples)
6. **DWT feature extraction** - Coiflet-5 wavelet, 5-level decomposition
7. **Extract detail coefficients** → 3020 features
8. **StandardScaler** transformation
9. **Random Forest** classification

### Model Specifications
- **Algorithm**: Random Forest Classifier
- **Features**: 3020 (DWT coefficients)
- **Wavelet**: Coiflet-5 (`coif5`)
- **Decomposition Level**: 5
- **Preprocessing**: StandardScaler + LabelEncoder
- **Accuracy**: ~88-99% (dataset dependent)

## 🖥️ Hardware Requirements

## 🖥️ Hardware Requirements

### Minimum (Any PC/Laptop)
- **CPU**: Any x86/ARM processor
- **RAM**: 512 MB
- **Display**: Any resolution
- **OS**: Windows, Linux, macOS

### Recommended (Raspberry Pi 5)
- **CPU**: ARM Cortex-A76 (4 cores @ 2.4GHz)
- **RAM**: 4-16 GB
- **Display**: MHS 35 LCD (320x480) or any touchscreen
- **OS**: Raspberry Pi OS (Debian-based)

### Resource Usage
- **Idle**: 200 MB RAM, <5% CPU
- **Processing**: 370 MB RAM (peak), ~40% CPU (brief)
- **Per Classification**: 2-3 seconds

## 📦 Installation

### On Raspberry Pi 5 (Recommended)

### 1. Clone Repository

```bash
git clone https://github.com/adityashravan/Heart_Sound_Research_Paper.git
cd Heart_Sound_Research_Paper
```

### 2. Install System Dependencies

```bash
sudo apt-get update
sudo apt-get install -y python3-tk
```

### 3. Install Python Dependencies (Fast Method - Recommended)

```bash
# Use pre-compiled packages from apt (faster on Raspberry Pi)
sudo apt-get install -y python3-numpy python3-scipy python3-sklearn
pip3 install PyWavelets
```

**OR** use automated setup:

```bash
chmod +x setup.sh
./setup.sh
```

### 4. Run the Application

```bash
python3 heart_sound_classifier.py
```

### On Windows/Mac/Linux

```bash
# Clone repository
git clone https://github.com/adityashravan/Heart_Sound_Research_Paper.git
cd Heart_Sound_Research_Paper

# Install dependencies
pip install -r requirements.txt

# Run application
python heart_sound_classifier.py
```

## 🚀 Usage

1. **Launch the app** - The GUI will open in a 320x480 window
2. **Select a WAV file:**
   - Click "📁 Browse File" to select any WAV file from your system
   - OR click "📂 Pick from Dataset" to choose from the organized dataset
3. **Classify** - Click "🔍 Classify" to get the prediction
4. **View Results** - The classification and confidence score will be displayed

## 📁 Project Structure

```
Heart_Sound_Research_Paper/
├── heart_sound_classifier.py       # Main GUI application
├── heart_sound_rf_model.pkl        # Trained Random Forest model
├── requirements.txt                # Python dependencies
├── setup.sh                        # Automated installation script (Linux/RPi)
├── launch.sh                       # Auto-start launcher
├── test_system.py                  # System verification script
├── inspect_model.py                # Model inspection tool
├── hardware_compatibility_check.py # Hardware compatibility analyzer
├── .gitignore                      # Git ignore rules
│
├── docs/                           # Documentation
│   ├── README.md                   # Main documentation
│   ├── DEPLOYMENT.md               # Deployment guide
│   ├── COMPATIBILITY.md            # Hardware compatibility details
│   ├── ARCHITECTURE.md             # System architecture
│   ├── AUTOSTART.md                # Auto-start configuration
│   └── QUICK_REFERENCE.md          # Quick reference card
│
└── Yaseen_Khan/                    # Dataset (organized by condition)
    ├── AS/                         # Aortic Stenosis samples
    ├── MR/                         # Mitral Regurgitation samples
    ├── MS/                         # Mitral Stenosis samples
    ├── MVP/                        # Mitral Valve Prolapse samples
    └── N/                          # Normal samples
```

## 🧪 Testing

### Run System Test
```bash
python3 test_system.py
```

This will verify:
- ✅ All dependencies installed
- ✅ Model file exists and loads correctly
- ✅ Dataset folder structure
- ✅ Audio processing pipeline

### Check Hardware Compatibility
```bash
python3 hardware_compatibility_check.py
```

## 🔧 Configuration

- **Lightweight GUI:** Tkinter (built-in, no web server needed)
- **Minimal dependencies:** Only 3 core packages (numpy, librosa, scikit-learn)
- **Efficient processing:** Features extracted on-demand, not pre-loaded
- **Small display optimized:** 320x480 resolution with touch-friendly buttons
- **Low memory usage:** Loads one audio file at a time

## Feature Extraction

The application extracts the following features from audio files:
- MFCCs (Mel-frequency cepstral coefficients)
- Spectral Centroid & Rolloff
- Zero Crossing Rate
- Chroma Features

**Note:** If your model was trained with different features, modify the `extract_features()` method accordingly.

## Troubleshooting

### Error: "Failed to load model"
- Ensure `heart_sound_rf_model.pkl` is in the same directory as the script

### Error: "Dataset folder not found"
- Ensure the `Yaseen_Khan` folder is in the same directory

### Slow performance
- Reduce sample rate in feature extraction (modify `librosa.load(sr=22050)`)
- Consider converting model to a lighter format

### Display issues on MHS 35 LCD
- The GUI is sized at 320x480 by default
- If text appears too small, increase font sizes in the code
- For touchscreen, buttons are sized at minimum 40x40 pixels for easy tapping

## License

Free to use for educational and research purposes.

## Credits

Model trained on heart sound dataset for cardiovascular condition detection.
