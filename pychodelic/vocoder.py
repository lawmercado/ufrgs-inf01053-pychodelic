from scipy.signal import stft, istft, butter, filtfilt

import numpy as np

def butter_low_pass_filter(data, cutoff, fs, order):
    nyq = fs * 0.5
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

def vocode(modulator: np.ndarray, carrier: np.ndarray, sampling_rate: int, volume: float, num_bands: int, window_size: int, window_overlap_size: int) -> np.ndarray:
    m_f, m_t, m_Zxx = stft(modulator, fs=sampling_rate, nperseg=window_size, noverlap=window_overlap_size)
    c_f, c_t, c_Zxx = stft(carrier, fs=sampling_rate, nperseg=window_size, noverlap=window_overlap_size)

    if num_bands > (window_size / 2):
        raise ValueError("The number of bands should not be greater than the half of the window size.")

    if num_bands > 0:
        num_freq_per_band = np.int(np.floor(len(m_f)/num_bands))

        for t in range(0, len(m_t)):
            for b in range(0, num_bands):
                mod = 0

                for f in range(b * num_freq_per_band, (b+1) * num_freq_per_band):
                    # Gets the magnitude of the frequency f at time t
                    mod += np.abs(m_Zxx[f, t])
                
                # Computes the average magnitude
                mod = mod / num_freq_per_band

                # Computes normalization factor with respect to the carrier
                car = np.sqrt(np.sum(np.abs(carrier[int(m_t[t] * sampling_rate) : int(m_t[t] * sampling_rate) + window_size] ** 2)) / sampling_rate)

                if car == 0:
                    car = 0.0001

                for f in range(b * num_freq_per_band, (b+1) * num_freq_per_band):
                    # Amplifies the same frequency band at time t in the carrier
                    c_Zxx[f, t] = c_Zxx[f, t] * mod / car

    else:
        for f in range(0, len(m_f)):
            for t in range(0, len(m_t)):
                # Gets the magnitude of the frequency f at time t
                mod = np.abs(m_Zxx[f, t])

                # Computes normalization factor with respect to the carrier
                car = np.sqrt(np.sum(np.abs(carrier[int(m_t[t] * sampling_rate) : int(m_t[t] * sampling_rate) + window_size] ** 2)) / sampling_rate)

                if car == 0:
                    car = 0.0001

                # Amplifies the same frequency f at time t in the carrier
                c_Zxx[f, t] = c_Zxx[f, t] * mod/car

    _, wave = istft(c_Zxx, fs=sampling_rate, nperseg=window_size, noverlap=window_overlap_size)

    # Normalizes the audio
    wave = wave/np.sqrt(np.sum(np.abs(wave ** 2)) / sampling_rate)

    return volume * wave