import argparse
import librosa
import numpy as np
import soundfile as sf

from pychodelic.vocoder import vocode

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

carrier = carrier[0:len(modulator)]

# In case the modulator is longer than the carrier audio, loop it
if len(carrier) != len(modulator):
    carrier = np.hstack((carrier, carrier[0:len(modulator) - len(carrier)]))

wave = vocode(modulator, carrier, args.sampling_rate, args.window_size, args.window_overlap_size)

sf.write(args.output, wave, args.sampling_rate)