# System Architecture

## Component Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Raspberry Pi 5                           │
│                  (ARM64, 4-core, 16GB RAM)                  │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  MHS 35 LCD  │   │   Tkinter    │   │  File System │
│   320x480    │   │     GUI      │   │              │
│  Touchscreen │   │  (Python 3)  │   │  Dataset     │
└──────────────┘   └──────────────┘   └──────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │         Audio Processing              │
        │                                       │
        │  ┌─────────────────────────────┐    │
        │  │   1. Load WAV file          │    │
        │  │   2. Extract features       │    │
        │  │      - MFCCs                │    │
        │  │      - Spectral features    │    │
        │  │      - Chroma               │    │
        │  │      - ZCR                  │    │
        │  └─────────────────────────────┘    │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │     ML Model (Random Forest)          │
        │   heart_sound_rf_model.pkl            │
        │                                       │
        │   Input: Feature vector               │
        │   Output: Class prediction            │
        │           + Confidence score          │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │         Classification Result         │
        │                                       │
        │   AS  - Aortic Stenosis              │
        │   MR  - Mitral Regurgitation         │
        │   MS  - Mitral Stenosis              │
        │   MVP - Mitral Valve Prolapse        │
        │   N   - Normal                        │
        └───────────────────────────────────────┘
```

## Data Flow

```
User Action
    │
    ├─► Browse File ───────────────┐
    │                              │
    └─► Pick from Dataset ─────────┤
                                   │
                                   ▼
                         Load WAV file
                                   │
                                   ▼
                         Extract Features
                         (librosa library)
                                   │
                                   ▼
                         Normalize/Reshape
                                   │
                                   ▼
                         ML Model Prediction
                         (Random Forest)
                                   │
                                   ▼
                         Display Results
                         (GUI Update)
```

## Resource Usage (Estimated)

| Component | Memory | CPU | Notes |
|-----------|--------|-----|-------|
| Python Runtime | ~50MB | Idle | Base interpreter |
| Tkinter GUI | ~20MB | <5% | Lightweight UI |
| librosa | ~100MB | Varies | Feature extraction |
| scikit-learn | ~30MB | <10% | Model inference |
| **Total** | **~200MB** | **<20%** | Per classification |

## Dependencies

```
System Level:
├── python3-tk       (GUI framework - pre-installed)
├── portaudio19-dev  (Audio support)
└── libsndfile1      (Sound file handling)

Python Level:
├── numpy            (Numerical operations)
├── librosa          (Audio feature extraction)
└── scikit-learn     (ML model loading)
```

## Optimization Features

1. **Lazy Loading**: Audio files loaded only when selected
2. **On-Demand Processing**: Features extracted during classification
3. **Minimal GUI**: No heavy frameworks (no web server, no Qt)
4. **Small Display Support**: Fixed 320x480 layout
5. **Touch-Friendly**: Large buttons (recommended >40px)

## Compatibility Notes

- **OS**: Raspberry Pi OS (Debian-based)
- **Python**: 3.7+ (tested on 3.9+)
- **Display**: MHS 35 LCD (320x480) or any small touchscreen
- **Architecture**: ARM64 (aarch64)
