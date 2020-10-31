import argparse
from typing import List

import librosa
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf

from pychodelic.vocoder import vocode

def save_waves_plot(path: str, waves: List[np.ndarray]) -> None:
    n = len(waves)

    plt.figure()
    for i, w in enumerate(waves):
        plt.subplot(n, 1, i+1)
        if len(w.shape) == 1:
            plt.plot(w)
            plt.xlim([0, len(w)])
            
    plt.savefig(path)

parser = argparse.ArgumentParser(
    description="Modulates a carrier with a given modulator (i.e. creates a vocoder effect)."
)

parser.add_argument("modulator", type=str, help="Path for the modulator audio file.")
parser.add_argument("carrier", type=str, help="Path for the carrier audio file.")
parser.add_argument("output", type=str, help="Path where to save the resulting audio file.")
parser.add_argument("--sampling_rate", type=int, help="Sampling rate to use when dealing with modulator and carrier audio files.", default=44100)
parser.add_argument("--window_size", type=int, help="Window size to consider in the STFT.", default=2048)
parser.add_argument("--window_overlap_size", type=int, help="Window overlap size to consider in the STFT.", default=1024)
parser.add_argument("--bands", type=int, help="Number of frequency bands.", default=1024)
parser.add_argument("--plot", help="Wheter the waves should be plotted.", default=False, action="store_true")

args = parser.parse_args()

modulator, _ = librosa.load(args.modulator, sr=args.sampling_rate, mono=True)
sf.write(args.modulator, modulator, args.sampling_rate)
carrier, _ = librosa.load(args.carrier, sr=args.sampling_rate, mono=True)

# In case the modulator is longer than the carrier audio, loop it
while len(carrier) < len(modulator):
    carrier = np.hstack((carrier, carrier))

carrier = carrier[0:len(modulator)]

wave = vocode(modulator, carrier, args.sampling_rate, args.window_size, args.window_overlap_size, args.bands)

sf.write(args.output, wave, args.sampling_rate)

if args.plot:
    matplotlib.use("Agg")
    save_waves_plot(args.output + ".png", [modulator, carrier, wave])
