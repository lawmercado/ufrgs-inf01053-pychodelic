import argparse

from synthesizer import Synthesizer, Waveform, Writer

from pychodelic.synthesis import available_synthesizers, get_synthesizer_by_waveform_type, sheet_to_wave

parser = argparse.ArgumentParser(
    description="Synthesize a given sheet music (in txt format)"
)

parser.add_argument("sheet", type=str, help="Path for the sheet music containing instructions for the synthesizer.")
parser.add_argument("type", type=str, help="Type of the main waveform of the synthesizer to use: " + str(available_synthesizers))
parser.add_argument("output", type=str, help="Main waveform of the synthesizer to use: " + str(available_synthesizers))

args = parser.parse_args()

if args.type not in available_synthesizers:
    raise ValueError("Unknown synthesizer type.")

synthesizer = get_synthesizer_by_waveform_type(args.type)

composition = sheet_to_wave(args.sheet, synthesizer)

writer = Writer()
writer.write_wave(args.output, composition)