from scipy.signal import stft, istft

import numpy as np

import matplotlib      # Remove this line if you don't need them
matplotlib.use('Agg')  # Remove this line if you don't need them
import matplotlib.pyplot as plt

def savefig(filename, figlist, log=True):
    n = len(figlist)

    plt.figure()
    for i, f in enumerate(figlist):
        plt.subplot(n, 1, i+1)
        if len(f.shape) == 1:
            plt.plot(f)
            plt.xlim([0, len(f)])
            
    plt.savefig(filename)

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