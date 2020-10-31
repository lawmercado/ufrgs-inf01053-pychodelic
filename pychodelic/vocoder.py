from scipy.signal import stft, istft

import numpy as np

def vocode(modulator: np.ndarray, carrier: np.ndarray, sampling_rate: int, window_size: int, window_overlap_size: int) -> np.ndarray:
    m_f, m_t, m_Zxx = stft(modulator, fs=sampling_rate, nperseg=window_size, noverlap=window_overlap_size)
    c_f, c_t, c_Zxx = stft(carrier, fs=sampling_rate, nperseg=window_size, noverlap=window_overlap_size)

    for f in range(0, len(m_f)):
        for t in range(0, len(m_t)):
            # Gets the magnitude of the frequency band f at time t
            mod = np.abs(m_Zxx[f, t])

            # Amplifies the same frequency band at time t in the carrier
            c_Zxx[f, t] = c_Zxx[f, t] * mod

    _, wave = istft(c_Zxx, fs=sampling_rate, nperseg=window_size, noverlap=window_overlap_size)

    # Normalizes the audio
    wave = wave * (1.0/np.max(wave))

    return wave