from scipy.signal import stft, istft, butter, filtfilt

import numpy as np
import math

def butter_low_pass_filter(data, cutoff, fs, order):
    nyq = fs * 0.5
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

def vocode(modulator: np.ndarray, carrier: np.ndarray, sampling_rate: int, window_size: int, window_overlap_size: int, bands: int) -> np.ndarray:
    m_f, m_t, m_Zxx = stft(modulator, fs=sampling_rate, nperseg=window_size, noverlap=window_overlap_size)
    c_f, c_t, c_Zxx = stft(carrier, fs=sampling_rate, nperseg=window_size, noverlap=window_overlap_size)

    n_freq_per_band = math.floor(len(m_f)/bands) 

    for b in range(0, bands):
        freq_sum = 0

        for t in range(0, len(m_t)):
            sum = 0

            for f in range(b*n_freq_per_band, (b+1)*n_freq_per_band):
                # Gets the magnitude of the frequency f at time t
                mod = np.abs(m_Zxx[f, t])
                sum += mod

            # Gets the average magnitude of the frequency f 
            avg = sum/n_freq_per_band

            for f in range(b*n_freq_per_band, (b+1)*n_freq_per_band):
                mod = np.abs(m_Zxx[f, t])
                car = np.sqrt(np.sum(np.abs(carrier[int(m_t[t] * sampling_rate) : int(m_t[t] * sampling_rate) + window_size] ** 2)) / sampling_rate)
                
                if car == 0:
                    car = 0.0001

                # Amplifies the same frequency band at time t in the carrier
                c_Zxx[f, t] = c_Zxx[f, t] * avg / car

        # TODO: apply low pass filter on each frequency band
        # cutoff = freq_sum/n_freq_per_band
        # c_Zxx[b*n_freq_per_band: (b+1)*n_freq_per_band] = butter_low_pass_filter(c_Zxx[b*n_freq_per_band: (b+1)*n_freq_per_band], cutoff, sampling_rate, 2)

    _, wave = istft(c_Zxx, fs=sampling_rate, nperseg=window_size, noverlap=window_overlap_size)

    # Normalizes the audio
    wave = wave/np.sqrt(np.sum(np.abs(wave ** 2)) / sampling_rate)

    return wave