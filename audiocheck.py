import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from pydub import AudioSegment

# LOAD FILE

def load_audio(file_path):
    try:
        audio = AudioSegment.from_file(file_path)
        audio = audio.set_channels(1)  # Mono audio
        audio = audio.set_frame_rate(44100)  # Sample rate of 44.1 kHz (standard)
        audio = audio.set_sample_width(2)  # 16-bit samples
        samples = np.array(audio.get_array_of_samples())
        return samples, audio.frame_rate
    except Exception as e:
        print(f"Error loading audio file: {e}")
        return None, None

# CALCULATE THE ROOT MEAN SQUARE OF SOUND SECTION

def calculate_rms(window):
    return np.sqrt(np.mean(window ** 2))

# CREATE AMPLITUDE ENVELOPE (not really sure why this works, but it does)

def create_envelope(samples, window_size=8820, overlap=0.5):
    total_samples = len(samples)
    window_step = int(window_size * (1 - overlap))
    envelope = []

    for start in range(0, total_samples - window_size, window_step):
        window_samples = samples[start:start + window_size]
        rms_value = calculate_rms(window_samples)
        envelope.append(rms_value)
    
    return np.array(envelope)

# FIND IRREGULARITIES

def analyze_audio_irregularities(file_path, window_size=8820, overlap=0.5, rms_threshold=0.1):
    samples, sample_rate = load_audio(file_path)
    if samples is None:
        return

    total_samples = len(samples)
    
    envelope = create_envelope(samples, window_size, overlap)
    
    # Find peaks here
    peaks, _ = find_peaks(envelope, height=rms_threshold)
    
    return envelope, peaks, total_samples / sample_rate

# PLOT

def plot_envelope_with_irregularities(envelope, peaks, total_duration):
    time = np.linspace(0, total_duration, len(envelope))
    
    plt.figure(figsize=(12, 6))
    plt.plot(time, envelope, label='Amplitude Envelope', color='blue')
    plt.plot(time[peaks], envelope[peaks], "x", label='Irregularities (Peaks)', color='red')
    plt.title('Engine Amplitude Envelope with Irregularities')
    plt.xlabel('Time (s)')
    plt.ylabel('RMS Amplitude')
    plt.legend()
    plt.grid(True)
    plt.show()

# MAIN ANALYSIS

def analyze_engine_sound(file_path):
    window_size = 8820                  # 0.2 seconds of audio (8820 samples for 44.1kHz sample rate)
    overlap = 0.5                       # 50% overlap between windows
    rms_threshold = 0.1                 # RMS threshold to detect irregularities
    
    envelope, peaks, total_duration = analyze_audio_irregularities(file_path, window_size, overlap, rms_threshold)
    
    plot_envelope_with_irregularities(envelope, peaks, total_duration)


if __name__ == "__main__":
    audio_file = './samples/engine_sound.mp3'
    
    analyze_engine_sound(audio_file)
