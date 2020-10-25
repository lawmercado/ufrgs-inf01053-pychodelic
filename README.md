# ufrgs-inf01053-pychodelic
A Python implementation of a vocoder with a (really basic) audio synthesis module



## Installation

- Install [synthesizer](https://github.com/yuma-m/synthesizer)
- Install [librosa](https://librosa.org/doc/latest/install.html)



## Audio synthesis

To generate an audio sample based on sheet music, use the *synthesize.py* utility:

```python
usage: synthesize.py [-h] sheet type output

Synthesize a given sheet music (in txt format)

positional arguments:
  sheet       Path for the sheet music containing instructions for the synthesizer.
  type        Type of the main waveform of the synthesizer to use: ['square', 'sawtooth']
  output      Main waveform of the synthesizer to use: ['square', 'sawtooth']

optional arguments:
  -h, --help  show this help message and exit
```



### Sheet music

The sheet music syntax is pretty straightforward: notes to be played together and its duration. For example:

Suppose a file *my_song.txt* with the content

```
C3 E3 G3 C4;3.0
G3 B3 D4 G4;3.0
```

If you pass this file to the *synthesize.py* utility, it will generate a waveform corresponding to the chords CM7 followed by a G, both being played for 3 seconds.