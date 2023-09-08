# Algorhythm

## Overview

Algorythm is a Python application that allows you to create various randomized sounds using waveform generators and effects. With the Random Sound Generator, you can create unique and experimental sound effects based on predefined algorithms combined with a degree of randomness.

## Dependencies

- Python 3.x
- pydub (`pip install pydub`)
- tkinter (comes pre-installed with most Python installations)

## Features

- **Waveform Generators:** Sine, Square, Sawtooth, Triangle, Pulse
- **Effects:**
  - Delay
  - Stutter
  - Arpeggiation (both pre-defined and randomized)
  - Echo (makeshift)
  - Reverb (makeshift)
  - And more!
  
- **GUI Interface:** A user-friendly GUI to easily set parameters like the number of sounds, randomness factor, and maximum duration.

## Usage

1. Clone the repository.
2. Install the necessary dependencies.
3. Run the Python script to launch the GUI.
4. Set the desired properties for your sounds.
5. Click "Generate Sounds" to create the sounds, which will be saved in a timestamped directory under "random_sounds".

## Code Structure

- **Main Functions:** Contains the core logic for generating and manipulating sound waveforms.
  - `add_delay(segment)`: Adds delay effects.
  - `apply_stutter(segment)`: Creates a stutter effect.
  - `apply_arpeggio(frequency, generator)`: Generates a basic arpeggio sound.
  - `randomized_arpeggiation(base_freq, steps, duration_per_step)`: Generates a randomized arpeggiated sound.
  - `makeshift_echo(sound, delay_time, decay_factor)`: Emulates a simple delay (echo) effect.
  - `makeshift_reverb(sound, num_echoes=5, start_delay=30, decay_factor=-5)`: Emulates a simple reverb by layering echoes.
  - `generate_random_sound(filename, randomness_factor=0.5, max_duration=6000)`: Main function for sound generation.

- **GUI Functions:** The logic for the graphical interface.
  - `start_gui()`: Initiates the GUI.

## Contribute

Feel free to fork this project, make changes, and open pull requests. Any contributions, whether it's new features or bug fixes, are highly appreciated.

## License

MIT License. See `LICENSE` for more details.

---

If you enjoy the Random Sound Generator or have any feedback, please drop a star on the repository and share your sounds with the community! 🎵🎶
