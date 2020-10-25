from synthesizer import Synthesizer, Waveform

import numpy as np

available_synthesizers = ["square", "sawtooth"]

def get_synthesizer_by_waveform_type(type: str) -> Synthesizer:
    if type == "sawtooth":
        return Synthesizer(osc1_waveform=Waveform.sawtooth, osc1_volume=1.0, use_osc2=True, osc2_waveform=Waveform.triangle, osc2_volume=0.2)

    elif type == "square":
        return Synthesizer(osc1_waveform=Waveform.square, osc1_volume=1.0, use_osc2=True, osc2_waveform=Waveform.triangle, osc2_volume=0.2)

def sheet_to_wave(path: str, synthesizer: Synthesizer) -> np.ndarray:
    sheet = open(path, "r") 
    lines = sheet.readlines()
    
    wave = np.array([])

    for line in lines: 
        info = line.strip().split(";")
        notes = info[0].split()
        duration = float(info[1])

        wave = np.hstack((wave, synthesizer.generate_chord(notes, duration)))

    return wave