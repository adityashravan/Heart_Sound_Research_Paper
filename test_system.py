#!/usr/bin/env python3
"""
Test script to verify model and dependencies
Run this before deploying to Raspberry Pi
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required packages are available"""
    print("Testing imports...")
    errors = []
    
    try:
        import numpy as np
        print("✓ numpy:", np.__version__)
    except ImportError as e:
        errors.append(f"✗ numpy: {e}")
    
    try:
        import librosa
        print("✓ librosa:", librosa.__version__)
    except ImportError as e:
        errors.append(f"✗ librosa: {e}")
    
    try:
        import sklearn
        print("✓ scikit-learn:", sklearn.__version__)
    except ImportError as e:
        errors.append(f"✗ scikit-learn: {e}")
    
    try:
        import tkinter
        print("✓ tkinter: available")
    except ImportError as e:
        errors.append(f"✗ tkinter: {e}")
    
    return errors

def test_model():
    """Test if model file exists and can be loaded"""
    print("\nTesting model...")
    model_path = Path(__file__).parent / "heart_sound_rf_model.pkl"
    
    if not model_path.exists():
        return [f"✗ Model file not found: {model_path}"]
    
    print(f"✓ Model file found: {model_path}")
    
    try:
        import pickle
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        print(f"✓ Model loaded successfully (type: {type(model).__name__})")
        
        # Check if it has predict method
        if hasattr(model, 'predict'):
            print("✓ Model has predict method")
        else:
            return ["✗ Model doesn't have predict method"]
            
        if hasattr(model, 'predict_proba'):
            print("✓ Model has predict_proba method (confidence scores available)")
        else:
            print("⚠ Model doesn't have predict_proba (no confidence scores)")
            
        return []
    except Exception as e:
        return [f"✗ Failed to load model: {e}"]

def test_dataset():
    """Test if dataset folder exists"""
    print("\nTesting dataset...")
    dataset_path = Path(__file__).parent / "Yaseen_Khan"
    
    if not dataset_path.exists():
        return [f"✗ Dataset folder not found: {dataset_path}"]
    
    print(f"✓ Dataset folder found: {dataset_path}")
    
    categories = ['AS', 'MR', 'MS', 'MVP', 'N']
    errors = []
    
    for cat in categories:
        cat_path = dataset_path / cat
        if cat_path.exists():
            wav_files = list(cat_path.glob("*.wav"))
            print(f"✓ {cat}: {len(wav_files)} WAV files")
        else:
            errors.append(f"✗ Category folder missing: {cat}")
    
    return errors

def test_audio_processing():
    """Test audio file processing"""
    print("\nTesting audio processing...")
    dataset_path = Path(__file__).parent / "Yaseen_Khan"
    
    # Find first WAV file
    test_file = None
    for cat in ['N', 'AS', 'MR', 'MS', 'MVP']:
        cat_path = dataset_path / cat
        if cat_path.exists():
            wav_files = list(cat_path.glob("*.wav"))
            if wav_files:
                test_file = wav_files[0]
                break
    
    if not test_file:
        return ["⚠ No WAV files found for testing"]
    
    print(f"Testing with: {test_file.name}")
    
    try:
        import librosa
        import numpy as np
        
        # Load audio
        y, sr = librosa.load(str(test_file), sr=None)
        print(f"✓ Audio loaded: {len(y)} samples at {sr} Hz ({len(y)/sr:.2f} seconds)")
        
        # Extract basic features
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        print(f"✓ MFCCs extracted: shape {mfccs.shape}")
        
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        print(f"✓ Spectral centroid extracted: shape {spectral_centroid.shape}")
        
        return []
    except Exception as e:
        return [f"✗ Audio processing failed: {e}"]

def main():
    """Run all tests"""
    print("="*60)
    print("Heart Sound Classifier - System Test")
    print("="*60)
    print()
    
    all_errors = []
    
    # Run tests
    all_errors.extend(test_imports())
    all_errors.extend(test_model())
    all_errors.extend(test_dataset())
    all_errors.extend(test_audio_processing())
    
    # Summary
    print("\n" + "="*60)
    if all_errors:
        print("❌ TESTS FAILED")
        print("="*60)
        for error in all_errors:
            print(error)
        print("\nPlease fix the above errors before running the application.")
        sys.exit(1)
    else:
        print("✅ ALL TESTS PASSED")
        print("="*60)
        print("\nSystem is ready! You can now run:")
        print("  python3 heart_sound_classifier.py")
        sys.exit(0)

if __name__ == "__main__":
    main()
