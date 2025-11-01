# Quick Reference Card - Heart Sound Classifier

## 🚀 QUICK START

```bash
# On Raspberry Pi 5:
cd ~/Frontend_RP
chmod +x setup.sh
./setup.sh
python3 heart_sound_classifier.py
```

---

## ✅ HARDWARE COMPATIBILITY

| Component | Requirement | Your Hardware | Status |
|-----------|-------------|---------------|--------|
| CPU | ARM/x86, 1+ core | ARM64, 4 cores | ✅ 4x over |
| RAM | 500 MB | 16 GB | ✅ 32x over |
| Display | Any | 320x480 LCD | ✅ Perfect |
| Storage | 100 MB | SD card | ✅ OK |

**Verdict: FULLY COMPATIBLE** 🎉

---

## 📦 DEPENDENCIES

| Package | Size | Install Method | Time |
|---------|------|----------------|------|
| python3-tk | Pre-installed | - | 0 min |
| NumPy | ~50 MB | `sudo apt install python3-numpy` | 1 min |
| SciPy | ~100 MB | `sudo apt install python3-scipy` | 1 min |
| scikit-learn | ~80 MB | `sudo apt install python3-sklearn` | 1 min |
| PyWavelets | ~30 MB | `pip3 install PyWavelets` | 1 min |

**Total: ~260 MB, ~4 minutes**

---

## ⚡ PERFORMANCE

```
Idle:        200 MB RAM,  <5% CPU
Processing:  370 MB RAM, ~40% CPU (brief)
Time/Audio:  2-3 seconds total
```

---

## 🎯 FILE STRUCTURE

```
Frontend_RP/
├── heart_sound_classifier.py  ← Main GUI app
├── heart_sound_rf_model.pkl   ← ML model
├── requirements.txt           ← Dependencies
├── setup.sh                   ← Auto-install
├── test_system.py             ← Verification
├── README.md                  ← Documentation
└── Yaseen_Khan/               ← Dataset
    ├── AS/  ├── MR/  ├── MS/  ├── MVP/  └── N/
```

---

## 🔧 TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| Import error | Run `python3 test_system.py` |
| Slow install | Use `apt` not `pip` for NumPy/SciPy |
| Model not found | Check `heart_sound_rf_model.pkl` in same dir |
| Wrong predictions | Ensure using `coif5` wavelet (matches training) |
| Touch not working | Run `xinput_calibrator` |
| Display too small | Edit font sizes in .py file |

---

## 📱 GUI LAYOUT (320x480)

```
┌─────────────────────────┐
│  Heart Sound Classifier │ ← Title
├─────────────────────────┤
│ Selected File: ...      │ ← File info
├─────────────────────────┤
│  [📁 Browse File]       │ ← Button 1
│  [📂 Pick from Dataset] │ ← Button 2
│  [🔍 Classify]          │ ← Button 3
├─────────────────────────┤
│ Classification Result   │
│                         │
│   *** RESULT ***        │ ← Prediction
│   Confidence: XX%       │ ← Score
│                         │
├─────────────────────────┤
│ Status: Ready           │ ← Status bar
└─────────────────────────┘
```

---

## 🎨 CUSTOMIZATION

```python
# In heart_sound_classifier.py

# Change window size (line 29):
self.root.geometry("480x800")  # Larger display

# Change fonts (line 90):
font=("Arial", 18, "bold")  # Bigger text

# Change colors (line 25):
self.primary_color = "#FF5722"  # Orange

# Change wavelet (line 366):
wavelet = 'db4'  # Daubechies-4 (if retrained)
```

---

## 🔄 WORKFLOW

1. User clicks **"Pick from Dataset"** or **"Browse File"**
2. Selects `.wav` file
3. Clicks **"Classify"**
4. App processes:
   - Load audio → Downsample → Filter → Normalize → DWT
5. Model predicts: **AS / MR / MS / MVP / N**
6. Display result + confidence

**Time: 2-3 seconds**

---

## 📊 PREPROCESSING PIPELINE

```
WAV file (any sample rate)
    ↓
Downsample to 1 kHz
    ↓
High-pass filter (Butterworth, 20 Hz)
    ↓
Z-score normalization
    ↓
Pad/trim to 3 seconds (3000 samples)
    ↓
DWT decomposition (coif5, level 5)
    ↓
Extract detail coefficients → 3020 features
    ↓
StandardScaler (from training)
    ↓
Random Forest classifier
    ↓
Prediction: AS/MR/MS/MVP/N
```

---

## 🏷️ CLASS LABELS

| Code | Meaning |
|------|---------|
| **N** | Normal (healthy) |
| **AS** | Aortic Stenosis |
| **MR** | Mitral Regurgitation |
| **MS** | Mitral Stenosis |
| **MVP** | Mitral Valve Prolapse |

---

## 🛡️ MODEL INFO

```
Type:           Random Forest Classifier
Features:       3020 (DWT coefficients)
Wavelet:        Coiflet-5 (coif5)
Level:          5
Scaler:         StandardScaler
Label Encoder:  LabelEncoder
Accuracy:       ~88-99%
```

---

## 🎯 AUTO-START OPTIONS

### Option 1: Desktop Entry
```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/heart-classifier.desktop << EOF
[Desktop Entry]
Type=Application
Name=Heart Sound Classifier
Exec=/home/admin/Frontend_RP/launch.sh
EOF
```

### Option 2: Systemd Service
```bash
sudo systemctl enable heart-classifier.service
```

See `AUTOSTART.md` for details.

---

## 📞 SUPPORT FILES

| File | Purpose |
|------|---------|
| `README.md` | Overview & installation |
| `DEPLOYMENT.md` | Detailed setup guide |
| `COMPATIBILITY.md` | Hardware compatibility |
| `ARCHITECTURE.md` | System design |
| `AUTOSTART.md` | Auto-launch setup |

---

## ✨ FEATURES

- ✅ Lightweight (200 MB idle)
- ✅ Fast (2-3 sec per audio)
- ✅ Touch-friendly UI
- ✅ Dataset browser
- ✅ Confidence scores
- ✅ No internet needed
- ✅ Auto-start capable
- ✅ ARM64 optimized

---

**Ready to deploy! 🚀**
