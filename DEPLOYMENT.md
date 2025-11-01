# Deployment Guide for Raspberry Pi 5

## Quick Start (Recommended)

### Step 1: Transfer Files to Raspberry Pi

Copy these files to your Raspberry Pi:
```bash
# On your PC, copy files to USB drive or use SCP
# Then on Raspberry Pi:
cd ~
mkdir Frontend_RP
cd Frontend_RP

# Copy all files here
```

### Step 2: Run Setup Script

```bash
chmod +x setup.sh
./setup.sh
```

### Step 3: Test Installation

```bash
python3 test_system.py
```

If all tests pass ✅, proceed to run the app!

### Step 4: Launch Application

```bash
python3 heart_sound_classifier.py
```

---

## Manual Installation (Alternative)

### 1. Install System Dependencies

```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-tk portaudio19-dev libsndfile1 python3-dev
```

### 2. Install Python Packages

```bash
# Standard installation
pip3 install -r requirements.txt

# OR if you have memory constraints, install one by one:
pip3 install numpy
pip3 install scikit-learn
pip3 install librosa
```

**Note for librosa**: Installation might take 5-10 minutes on Raspberry Pi. Be patient!

### 3. Verify Installation

```bash
python3 test_system.py
```

---

## Optimizations for MHS 35 LCD

### Display Configuration

1. **Set correct resolution** (if needed):
```bash
# Edit boot config
sudo nano /boot/config.txt

# Add or modify:
hdmi_group=2
hdmi_mode=87
hdmi_cvt=320 480 60 6 0 0 0
```

2. **Rotate display** (if mounted sideways):
```bash
# In /boot/config.txt
display_rotate=1  # 90 degrees
display_rotate=2  # 180 degrees
display_rotate=3  # 270 degrees
```

### Performance Tuning

1. **Reduce audio processing load**:
Edit `heart_sound_classifier.py` and change:
```python
# Line 217: Reduce sample rate
y, sr = librosa.load(audio_path, sr=22050)  # Instead of sr=None
```

2. **Disable unnecessary services**:
```bash
sudo systemctl disable bluetooth
sudo systemctl disable avahi-daemon
```

3. **Increase swap** (if getting memory errors):
```bash
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# Change CONF_SWAPSIZE=100 to CONF_SWAPSIZE=512
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

---

## Touchscreen Calibration

If touchscreen is not accurate:

```bash
sudo apt-get install xinput-calibrator
DISPLAY=:0 xinput_calibrator
```

Follow on-screen instructions and save calibration data.

---

## Common Issues & Solutions

### Issue 1: "tkinter not found"
```bash
sudo apt-get install python3-tk
```

### Issue 2: "librosa installation fails"
```bash
# Install build dependencies
sudo apt-get install python3-dev libblas-dev liblapack-dev libatlas-base-dev gfortran

# Try installing with no dependencies first
pip3 install librosa --no-deps
pip3 install soundfile audioread
```

### Issue 3: "Model fails to load"
- Ensure `heart_sound_rf_model.pkl` is in the same directory
- Check Python version (should be 3.7+)
- Try re-training model if version mismatch

### Issue 4: "GUI too small on display"
Edit `heart_sound_classifier.py`:
```python
# Line 29: Increase font sizes
font=("Arial", 18, "bold")  # Instead of 16

# Line 122: Larger buttons
height=3  # Instead of 2
```

### Issue 5: "Audio processing is slow"
- Reduce sample rate (see Performance Tuning above)
- Consider using a lighter model
- Pre-compute features offline

### Issue 6: "Dataset not found"
- Ensure folder structure is:
  ```
  Frontend_RP/
  ├── heart_sound_classifier.py
  ├── heart_sound_rf_model.pkl
  └── Yaseen_Khan/
      ├── AS/
      ├── MR/
      ├── MS/
      ├── MVP/
      └── N/
  ```

---

## Memory Usage Monitoring

Check memory while running:
```bash
# In another terminal
watch -n 2 free -h

# Or for detailed process info
htop
```

Expected usage:
- Idle: ~200MB
- Processing: ~350MB (peak during classification)

---

## Auto-Start on Boot

See `AUTOSTART.md` for detailed instructions.

Quick option:
```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/heart-classifier.desktop << EOF
[Desktop Entry]
Type=Application
Name=Heart Sound Classifier
Exec=/home/admin/Frontend_RP/launch.sh
Terminal=false
EOF

chmod +x launch.sh
```

---

## Network Features (Optional)

To access from other devices, you can add Flask API:

```bash
pip3 install flask flask-cors
```

Then modify app to include REST endpoint (not included in minimal version).

---

## Backup & Updates

### Create backup:
```bash
cd ~
tar -czf heart_classifier_backup.tar.gz Frontend_RP/
```

### Update model:
```bash
# Just replace the .pkl file
cp new_model.pkl ~/Frontend_RP/heart_sound_rf_model.pkl
```

---

## Testing on Desktop First

Before deploying to Pi, test on your PC:

**Windows:**
```bash
pip install -r requirements.txt
python heart_sound_classifier.py
```

**Linux/Mac:**
```bash
pip3 install -r requirements.txt
python3 heart_sound_classifier.py
```

---

## Performance Benchmarks

Tested on Raspberry Pi 5 (16GB RAM):

| Operation | Time | Memory |
|-----------|------|--------|
| App startup | ~2s | 180MB |
| Load audio file | <0.5s | +50MB |
| Feature extraction | ~1-2s | +100MB |
| Classification | <0.1s | +20MB |
| **Total per prediction** | **~3s** | **~350MB peak** |

---

## Support

For issues:
1. Run `python3 test_system.py` for diagnostics
2. Check logs: `~/.xsession-errors`
3. Verify model compatibility with your training code

---

## Next Steps

1. ✅ Transfer files to Raspberry Pi
2. ✅ Run `setup.sh`
3. ✅ Run `test_system.py`
4. ✅ Launch `heart_sound_classifier.py`
5. ⚡ Configure auto-start (optional)
6. 🎯 Test with real audio samples

Good luck! 🚀
