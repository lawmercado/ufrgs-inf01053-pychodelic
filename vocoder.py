import argparse
import librosa
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf

from pychodelic.vocoder import vocode

def savefig(filename, figlist, log=True):
    n = len(figlist)

    plt.figure()
    for i, f in enumerate(figlist):
        plt.subplot(n, 1, i+1)
        if len(f.shape) == 1:
            plt.plot(f)
            plt.xlim([0, len(f)])
            
    plt.savefig(filename)

parser = argparse.ArgumentParser(
    description="Modulates a carrier with a given modulator (i.e. creates a vocoder effect)."
)

parser.add_argument("modulator", type=str, help="Path for the modulator audio file.")
parser.add_argument("carrier", type=str, help="Path for the carrier audio file.")
parser.add_argument("output", type=str, help="Path where to save the resulting audio file.")
parser.add_argument("--sampling_rate", type=int, help="Sampling rate to use when dealing with modulator and carrier audio files.", default=44100)
parser.add_argument("--window_size", type=int, help="Window size to consider in the STFT.", default=2048)
parser.add_argument("--window_overlap_size", type=int, help="Window overlap size to consider in the STFT.", default=1024)

args = parser.parse_args()

modulator, _ = librosa.load(args.modulator, sr=args.sampling_rate, mono=True)
carrier, _ = librosa.load(args.carrier, sr=args.sampling_rate, mono=True)

# In case the modulator is longer than the carrier audio, loop it
while len(carrier) < len(modulator):
    carrier = np.hstack((carrier, carrier))

carrier = carrier[0:len(modulator)]

wave = vocode(modulator, carrier, args.sampling_rate, args.window_size, args.window_overlap_size)

matplotlib.use("Agg")
savefig(args.output + ".png", [modulator, carrier, wave])

sf.write(args.output, wave, args.sampling_rate)