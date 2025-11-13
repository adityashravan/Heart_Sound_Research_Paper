#!/usr/bin/env python3
"""
Heart Sound Classifier GUI for Raspberry Pi 5
Optimized for MHS 35 LCD Display (320x480)
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pickle
import numpy as np
import os
from pathlib import Path
from scipy.io import wavfile
from scipy import signal
import pywt
import matplotlib
matplotlib.use('TkAgg')  # Use Tkinter backend
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class HeartSoundClassifier:
    def __init__(self, root):
        self.root = root
        self.root.title("Heart Sound Classifier")
        
        # Optimize for MHS 35 LCD (320x480)
        self.root.geometry("320x480")
        self.root.resizable(False, False)
        
        # Color scheme
        self.bg_color = "#f0f0f0"
        self.primary_color = "#2196F3"
        self.success_color = "#4CAF50"
        self.danger_color = "#f44336"
        
        self.root.configure(bg=self.bg_color)
        
        # Load ML model
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.feature_shape = None
        self.load_model()
        
        # Dataset path
        self.dataset_path = Path(__file__).parent / "Yaseen_Khan"
        
        # Class labels (based on folder structure)
        self.class_labels = {
            'AS': 'Aortic Stenosis',
            'MR': 'Mitral Regurgitation',
            'MS': 'Mitral Stenosis',
            'MVP': 'Mitral Valve Prolapse',
            'N': 'Normal'
        }
        
        # Create GUI
        self.create_widgets()
        
    def load_model(self):
        """Load the pickled Random Forest model"""
        try:
            model_path = Path(__file__).parent / "heart_sound_rf_model.pkl"
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            # Check if it's a dictionary with multiple components
            if isinstance(model_data, dict):
                self.model = model_data.get('classifier')
                self.scaler = model_data.get('scaler')
                self.label_encoder = model_data.get('label_encoder')
                self.feature_shape = model_data.get('feature_shape')
                print(f"Model loaded successfully! (Accuracy: {model_data.get('accuracy', 'N/A')})")
            else:
                # If it's just the model directly
                self.model = model_data
                self.scaler = None
                self.label_encoder = None
                self.feature_shape = None
                print("Model loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load model:\n{str(e)}")
            
    def create_widgets(self):
        """Create GUI components optimized for small screen"""
        
        # Title
        title = tk.Label(
            self.root,
            text="Heart Sound\nClassifier",
            font=("Arial", 16, "bold"),
            bg=self.bg_color,
            fg=self.primary_color
        )
        title.pack(pady=10)
        
        # File info frame
        info_frame = tk.Frame(self.root, bg=self.bg_color)
        info_frame.pack(pady=5, padx=10, fill='x')
        
        tk.Label(
            info_frame,
            text="Selected File:",
            font=("Arial", 9, "bold"),
            bg=self.bg_color
        ).pack(anchor='w')
        
        self.file_label = tk.Label(
            info_frame,
            text="No file selected",
            font=("Arial", 8),
            bg=self.bg_color,
            fg="#666",
            wraplength=280,
            justify='left'
        )
        self.file_label.pack(anchor='w')
        
        # Buttons frame
        btn_frame = tk.Frame(self.root, bg=self.bg_color)
        btn_frame.pack(pady=10)
        
        # Browse file button
        self.browse_btn = tk.Button(
            btn_frame,
            text="📁 Browse\nFile",
            font=("Arial", 10, "bold"),
            bg=self.primary_color,
            fg="white",
            activebackground="#1976D2",
            activeforeground="white",
            width=13,
            height=2,
            relief=tk.RAISED,
            bd=2,
            command=self.browse_file
        )
        self.browse_btn.pack(pady=5)
        
        # Dataset selection button
        self.dataset_btn = tk.Button(
            btn_frame,
            text="📂 Pick from\nDataset",
            font=("Arial", 10, "bold"),
            bg=self.primary_color,
            fg="white",
            activebackground="#1976D2",
            activeforeground="white",
            width=13,
            height=2,
            relief=tk.RAISED,
            bd=2,
            command=self.pick_from_dataset
        )
        self.dataset_btn.pack(pady=5)
        
        # Classify button
        self.classify_btn = tk.Button(
            btn_frame,
            text="🔍 Classify",
            font=("Arial", 12, "bold"),
            bg=self.success_color,
            fg="white",
            activebackground="#45a049",
            activeforeground="white",
            width=13,
            height=2,
            relief=tk.RAISED,
            bd=2,
            state=tk.DISABLED,
            command=self.classify_audio
        )
        self.classify_btn.pack(pady=10)
        
        # Visualize waveform button
        self.visualize_btn = tk.Button(
            btn_frame,
            text="📊 Show\nWaveform",
            font=("Arial", 10, "bold"),
            bg="#FF9800",
            fg="white",
            activebackground="#F57C00",
            activeforeground="white",
            width=13,
            height=2,
            relief=tk.RAISED,
            bd=2,
            state=tk.DISABLED,
            command=self.show_waveform
        )
        self.visualize_btn.pack(pady=5)
        
        # Result frame
        result_frame = tk.Frame(self.root, bg="white", relief=tk.RIDGE, bd=2)
        result_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        tk.Label(
            result_frame,
            text="Classification Result",
            font=("Arial", 11, "bold"),
            bg="white",
            fg=self.primary_color
        ).pack(pady=5)
        
        self.result_label = tk.Label(
            result_frame,
            text="No prediction yet",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#666",
            wraplength=280
        )
        self.result_label.pack(pady=10)
        
        # Confidence label
        self.confidence_label = tk.Label(
            result_frame,
            text="",
            font=("Arial", 9),
            bg="white",
            fg="#666"
        )
        self.confidence_label.pack(pady=5)
        
        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            font=("Arial", 8),
            bg="#ddd",
            fg="#333",
            anchor='w',
            relief=tk.SUNKEN
        )
        self.status_bar.pack(side=tk.BOTTOM, fill='x')
        
        # Store current file path
        self.current_file = None
        
    def browse_file(self):
        """Open file dialog to select WAV file"""
        filename = filedialog.askopenfilename(
            title="Select WAV File",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )
        if filename:
            self.load_audio_file(filename)
            
    def pick_from_dataset(self):
        """Show dialog to pick file from dataset"""
        if not self.dataset_path.exists():
            messagebox.showerror("Error", "Dataset folder not found!")
            return
            
        # Create selection window
        picker = tk.Toplevel(self.root)
        picker.title("Select from Dataset")
        picker.geometry("300x400")
        picker.transient(self.root)
        picker.grab_set()
        
        tk.Label(
            picker,
            text="Select Category:",
            font=("Arial", 10, "bold")
        ).pack(pady=5)
        
        # Category selection
        category_var = tk.StringVar()
        category_frame = tk.Frame(picker)
        category_frame.pack(pady=5)
        
        for cat, label in self.class_labels.items():
            tk.Radiobutton(
                category_frame,
                text=f"{cat} - {label}",
                variable=category_var,
                value=cat,
                font=("Arial", 9)
            ).pack(anchor='w')
        
        category_var.set('N')  # Default selection
        
        # File listbox
        tk.Label(picker, text="Select File:", font=("Arial", 10, "bold")).pack(pady=5)
        
        listbox_frame = tk.Frame(picker)
        listbox_frame.pack(pady=5, padx=10, fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
        file_listbox = tk.Listbox(
            listbox_frame,
            yscrollcommand=scrollbar.set,
            font=("Arial", 8)
        )
        file_listbox.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.config(command=file_listbox.yview)
        
        def update_files(*args):
            """Update file list when category changes"""
            file_listbox.delete(0, tk.END)
            cat = category_var.get()
            cat_path = self.dataset_path / cat
            if cat_path.exists():
                files = sorted([f.name for f in cat_path.glob("*.wav")])
                for f in files:
                    file_listbox.insert(tk.END, f)
        
        category_var.trace('w', update_files)
        update_files()  # Initial load
        
        def select_file():
            """Load selected file"""
            selection = file_listbox.curselection()
            if selection:
                filename = file_listbox.get(selection[0])
                cat = category_var.get()
                filepath = self.dataset_path / cat / filename
                self.load_audio_file(str(filepath))
                picker.destroy()
            else:
                messagebox.showwarning("Warning", "Please select a file!")
        
        tk.Button(
            picker,
            text="Select",
            command=select_file,
            bg=self.primary_color,
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(pady=10)
        
    def load_audio_file(self, filepath):
        """Load and display audio file info"""
        self.current_file = filepath
        filename = os.path.basename(filepath)
        self.file_label.config(text=filename, fg="black")
        self.classify_btn.config(state=tk.NORMAL)
        self.visualize_btn.config(state=tk.NORMAL)
        self.result_label.config(text="No prediction yet", fg="#666")
        self.confidence_label.config(text="")
        self.status_bar.config(text=f"Loaded: {filename}")
        
    def extract_features(self, audio_path):
        """
        Extract features using the EXACT same preprocessing as training:
        1. Load WAV file
        2. Downsample to 1 kHz
        3. High-pass filter (Butterworth, 20 Hz)
        4. Z-score normalization
        5. Pad/trim to 3 seconds
        6. DWT decomposition (coif5, level 5) - or db4 if updated
        """
        try:
            # Step 1: Load audio file
            sr, audio = wavfile.read(audio_path)
            
            # Convert to float32 if needed
            if audio.dtype == np.int16:
                audio = audio.astype(np.float32) / 32768.0
            elif audio.dtype == np.int32:
                audio = audio.astype(np.float32) / 2147483648.0
            
            # Handle stereo (take first channel)
            if len(audio.shape) > 1:
                audio = audio[:, 0]
            
            # Step 2: Downsample to 1 kHz
            target_sr = 1000
            if sr != target_sr:
                num_samples = int(len(audio) * target_sr / sr)
                audio = signal.resample(audio, num_samples)
            
            # Step 3: High-pass filter (Butterworth, 20 Hz cutoff, 4th order)
            nyquist = target_sr / 2
            normalized_cutoff = 20 / nyquist
            b, a = signal.butter(4, normalized_cutoff, btype='high')
            audio = signal.filtfilt(b, a, audio)
            
            # Step 4: Z-score normalization
            mean = np.mean(audio)
            std = np.std(audio)
            if std > 0:
                audio = (audio - mean) / std
            
            # Step 5: Pad or trim to 3 seconds (3000 samples at 1 kHz)
            target_length = 3000
            if len(audio) > target_length:
                audio = audio[:target_length]
            elif len(audio) < target_length:
                padding = target_length - len(audio)
                audio = np.pad(audio, (0, padding), mode='constant')
            
            # Step 6: DWT feature extraction
            # Using coif5 (or change to 'db4' to match paper exactly)
            wavelet = 'coif5'  # Change to 'db4' or 'db8' if you retrain with Daubechies
            level = 5
            
            coeffs = pywt.wavedec(audio, wavelet, level=level)
            
            # Extract detail coefficients only (discard approximation)
            dwt_features = np.concatenate(coeffs[1:])
            
            # Ensure we have the expected number of features
            expected_features = self.feature_shape if self.feature_shape else 3020
            
            if len(dwt_features) > expected_features:
                dwt_features = dwt_features[:expected_features]
            elif len(dwt_features) < expected_features:
                # Pad with zeros if needed
                padding = expected_features - len(dwt_features)
                dwt_features = np.pad(dwt_features, (0, padding), mode='constant')
            
            return dwt_features.reshape(1, -1)
            
        except Exception as e:
            raise Exception(f"Feature extraction failed: {str(e)}")
            
    def classify_audio(self):
        """Classify the selected audio file"""
        if not self.current_file:
            messagebox.showwarning("Warning", "Please select a file first!")
            return
            
        if self.model is None:
            messagebox.showerror("Error", "Model not loaded!")
            return
            
        try:
            self.status_bar.config(text="Processing...")
            self.root.update()
            
            # Extract features
            features = self.extract_features(self.current_file)
            
            # Apply scaler if available
            if self.scaler is not None:
                features = self.scaler.transform(features)
            
            # Make prediction
            prediction = self.model.predict(features)[0]
            
            # Decode label if label encoder is available
            if self.label_encoder is not None:
                prediction = self.label_encoder.inverse_transform([prediction])[0]
            
            # Get probability if available
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba(features)[0]
                confidence = np.max(probabilities) * 100
                self.confidence_label.config(
                    text=f"Confidence: {confidence:.1f}%"
                )
            
            # Display result
            result_text = self.class_labels.get(str(prediction), str(prediction))
            self.result_label.config(
                text=result_text,
                fg=self.danger_color if str(prediction) != 'N' else self.success_color
            )
            
            self.status_bar.config(text=f"Classification complete: {result_text}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Classification failed:\n{str(e)}")
            self.status_bar.config(text="Classification failed")
    
    def show_waveform(self):
        """Display waveform visualization in a new window"""
        if not self.current_file:
            messagebox.showwarning("Warning", "Please select a file first!")
            return
        
        try:
            self.status_bar.config(text="Loading waveform...")
            self.root.update()
            
            # Load raw audio
            sr, audio = wavfile.read(self.current_file)
            
            # Convert to float32 if needed
            if audio.dtype == np.int16:
                audio = audio.astype(np.float32) / 32768.0
            elif audio.dtype == np.int32:
                audio = audio.astype(np.float32) / 2147483648.0
            
            # Handle stereo
            if len(audio.shape) > 1:
                audio = audio[:, 0]
            
            # Create time axis
            duration = len(audio) / sr
            time = np.linspace(0, duration, len(audio))
            
            # Also load preprocessed version
            # Downsample to 1 kHz
            target_sr = 1000
            if sr != target_sr:
                num_samples = int(len(audio) * target_sr / sr)
                audio_processed = signal.resample(audio, num_samples)
            else:
                audio_processed = audio.copy()
            
            # High-pass filter
            nyquist = target_sr / 2
            normalized_cutoff = 20 / nyquist
            b, a = signal.butter(4, normalized_cutoff, btype='high')
            audio_filtered = signal.filtfilt(b, a, audio_processed)
            
            # Z-score normalization
            mean = np.mean(audio_filtered)
            std = np.std(audio_filtered)
            if std > 0:
                audio_normalized = (audio_filtered - mean) / std
            else:
                audio_normalized = audio_filtered
            
            # Trim to 3 seconds for processed version
            target_length = 3000
            if len(audio_normalized) > target_length:
                audio_normalized = audio_normalized[:target_length]
            
            time_processed = np.linspace(0, len(audio_normalized) / target_sr, len(audio_normalized))
            
            # Create visualization window - sized for 320x480 LCD
            viz_window = tk.Toplevel(self.root)
            viz_window.title("Heart Sound")
            viz_window.geometry("320x400")  # Fit within LCD display
            viz_window.resizable(False, False)
            
            # Create figure with single plot - preprocessed signal only
            fig = Figure(figsize=(3.2, 3.5), dpi=100)
            
            # Plot: Preprocessed Signal (what the model uses)
            ax = fig.add_subplot(1, 1, 1)
            ax.plot(time_processed, audio_normalized, color='#4CAF50', linewidth=1.2)
            ax.set_title('Heart Sound (PCG)', fontsize=10, fontweight='bold')
            ax.set_xlabel('Time (s)', fontsize=8)
            ax.set_ylabel('Amplitude', fontsize=8)
            ax.grid(True, alpha=0.3, linewidth=0.5)
            ax.set_xlim([0, 3])
            ax.tick_params(labelsize=7)
            
            fig.tight_layout(pad=0.5)
            
            # Embed plot in Tkinter window
            canvas = FigureCanvasTkAgg(fig, master=viz_window)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            
            # Add info label - compact for small screen
            info_frame = tk.Frame(viz_window, bg='#f0f0f0', pady=2)
            info_frame.pack(side=tk.BOTTOM, fill='x')
            
            filename = os.path.basename(self.current_file)
            # Truncate long filenames
            if len(filename) > 25:
                filename = filename[:22] + "..."
            
            info_text = f"{filename}\n{duration:.1f}s | {sr}Hz"
            
            info_label = tk.Label(
                info_frame,
                text=info_text,
                font=("Arial", 7),
                bg='#f0f0f0',
                justify='center'
            )
            info_label.pack()
            
            # Add close button
            close_btn = tk.Button(
                viz_window,
                text="Close",
                command=viz_window.destroy,
                font=("Arial", 9, "bold"),
                bg="#f44336",
                fg="white",
                width=10,
                height=1
            )
            close_btn.pack(side=tk.BOTTOM, pady=3)
            
            self.status_bar.config(text="Waveform displayed")
            
        except Exception as e:
            messagebox.showerror("Error", f"Visualization failed:\n{str(e)}")
            self.status_bar.config(text="Visualization failed")

def main():
    root = tk.Tk()
    app = HeartSoundClassifier(root)
    root.mainloop()

if __name__ == "__main__":
    main()
