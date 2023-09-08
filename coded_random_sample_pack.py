from pydub import AudioSegment
from pydub.generators import Sine, Square, Sawtooth, Triangle, Pulse
import random
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox
import os

#------------------------------------------------------------------------------------

OUTPUT_DIR = "random_sounds"

#====================================================================================
#====================================================================================

# M A I N    F U N C T I O N S

# effects
def add_delay(segment):
    delay_time = random.randint(50, 700)  # More randomness
    overlays = random.randint(1, 3)  # Number of potential overlays
    delayed = segment
    for _ in range(overlays):
        delay_seg = segment._spawn(b"\0" * int(44.1 * delay_time))
        gain_overlay = random.randint(-15, -1)  # More randomness
        delayed = delayed.overlay(segment, gain_during_overlay=gain_overlay)
        delay_time = random.randint(50, 700)  # Re-randomize for next overlay if applicable
    return delayed

def apply_stutter(segment):
    start_point = random.randint(0, len(segment) - 150)  # Random start point
    duration_ms = random.randint(10, 200)  # More randomness
    repeats = random.randint(1, 15)  # More randomness
    stutter_piece = segment[start_point:start_point + duration_ms]
    stuttered = AudioSegment.empty()
    for _ in range(repeats):
        stuttered += stutter_piece
    return stuttered

def apply_arpeggio(frequency, generator):
    step = random.choice([50, 75, 100, 125])  # Random step size
    steps = random.randint(3, 8)  # Random number of steps
    duration_per_step = random.randint(50, 200)  # More randomness
    arp_sound = AudioSegment.empty()
    for i in range(steps):
        arp_freq = frequency + (i * step)
        arp_sound += generator(arp_freq).to_audio_segment(duration=duration_per_step)
    return arp_sound

def randomized_arpeggiation(base_freq, steps, duration_per_step):
    """Generate a randomized arpeggiated sound."""
    generators = [Sine, Square, Sawtooth, Triangle, Pulse]
    gen_choice = random.choice(generators)

    # Randomly shuffle the arpeggio steps
    random.shuffle(steps)

    arpeggio_segments = []
    for step in steps:
        freq = base_freq * step
        segment = gen_choice(freq).to_audio_segment(duration=duration_per_step)
        arpeggio_segments.append(segment)

    return sum(arpeggio_segments)

def makeshift_echo(sound, delay_time, decay_factor):
    """Emulate a simple delay (echo) effect."""
    delay = AudioSegment.silent(duration=delay_time)
    delayed_sound = sound.overlay(sound + decay_factor, position=delay_time)
    
    # Add another layer of delay for more intensity
    second_delay_time = int(delay_time * 1.5)
    second_delay = AudioSegment.silent(duration=second_delay_time)
    second_delayed_sound = sound.overlay(sound + (decay_factor * 1.5), position=second_delay_time)

    return sound + delay + delayed_sound + second_delay + second_delayed_sound

def makeshift_reverb(sound, num_echoes=5, start_delay=30, decay_factor=-5):
    """Emulate a very simple reverb by layering echoes."""
    reverbed = sound
    for _ in range(num_echoes):
        sound = makeshift_echo(sound, start_delay, decay_factor)
        start_delay *= 1.2  # Increase echo occurrence
        decay_factor -= 2.5  # Intensify the decay
    return reverbed.overlay(sound)

#------------------------------------------------------------------------------------


# generate
def generate_random_sound(filename, randomness_factor=0.5, max_duration=6000):  # <-- Add max_duration parameter here

    generators = [Sine, Square, Sawtooth, Triangle, Pulse]
    gen_choice = random.choice(generators)

    # Random frequency between 50Hz and 880Hz
    freq = random.randint(50, 880)

    # Random duration between 0.4s and 3s in milliseconds
    duration = random.randint(400, 3000)

    # Generate the first sound
    sound1 = gen_choice(freq).to_audio_segment(duration=duration)

    # With a probability dictated by randomness_factor, generate a second sound and concatenate
    sound = sound1
    if random.random() < randomness_factor:
        max_duration2 = max_duration - duration
        if max_duration2 > 400:
            duration2 = random.randint(400, max_duration2)
            gen_choice2 = random.choice(generators)
            freq2 = random.randint(50, 880)
            sound2 = gen_choice2(freq2).to_audio_segment(duration=duration2)
            sound += sound2
            
    # Random frequency between 400Hz and 900Hz
    freq = random.randint(50, 880)

    # Random duration between 0.4s and 6s in milliseconds
    duration = random.randint(400, 3000)

    # Generate the first sound
    sound1 = gen_choice(freq).to_audio_segment(duration=duration)

    # With a 50% probability, generate a second sound and concatenate
    sound = sound1
    if random.random() > 0.5:
        max_duration2 = 1000 - duration
        if max_duration2 > 400:
            duration2 = random.randint(400, max_duration2)
            gen_choice2 = random.choice(generators)
            freq2 = random.randint(400, 900)
            sound2 = gen_choice2(freq2).to_audio_segment(duration=duration2)
            sound += sound2

    # Apply random effects
    if random.random() > (0.5 - randomness_factor/2):
        sound = sound + sound.reverse()

    if random.random() > (0.6 - randomness_factor/2):
        sound = add_delay(sound)

    if random.random() > (0.7 - randomness_factor/2):
        sound = apply_stutter(sound)

    if random.random() > (0.6 - randomness_factor/2):
        sound = apply_arpeggio(freq, gen_choice)

    if random.random() < (0.5 - randomness_factor/2):
        speed_change = random.uniform(1.1, 1.5)
        if len(sound) > 150: 
            sound = sound.speedup(playback_speed=speed_change)
        else:
            sound = sound.speedup(playback_speed=speed_change, chunk_size=int(len(sound)/2))

    if random.random() > (0.6 - randomness_factor/2):
        sound = sound.fade_in(duration=1000)

    if random.random() > (0.6 - randomness_factor/2):
        sound = sound.fade_out(duration=1000)

    if random.random() > (0.6 - randomness_factor/2):
        sound = sound.invert_phase()

    if random.random() > (0.7 - randomness_factor/2):
        cutoff = random.choice([300, 500, 1000, 2000])
        filter_choice = random.choice(['highpass', 'lowpass'])
        if filter_choice == 'highpass':
            sound = sound.high_pass_filter(cutoff)
        else:
            sound = sound.low_pass_filter(cutoff)

    if random.random() > (0.5 - randomness_factor/2):
        steps = [1, 9/8, 5/4, 3/2]
        duration_per_step = random.randint(100, 500)
        sound += randomized_arpeggiation(freq, steps, duration_per_step)

    if random.random() > (0.7 - randomness_factor/2):
        delay_time = random.randint(100, 500)
        decay_factor = random.uniform(-2, -5)
        sound += makeshift_echo(sound, delay_time, decay_factor)

    if random.random() > (0.7 - randomness_factor/2):
        sound += makeshift_reverb(sound)

    # At the end, before exporting:
    if len(sound) > max_duration:
        sound = sound[:max_duration]  # Trim to desired length. You can also add a fade out for smoother ending.

    sound.export(filename, format="wav")

#------------------------------------------------------------------------------------

    
# main
def main(num_sounds, prefix, randomness_factor=0.5, max_duration=6000):  # <-- Add max_duration parameter here
    #... rest of the code remains unchanged

    # Generate a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create a new directory inside OUTPUT_DIR with "sound pack [timestamp]" as the name
    new_output_dir = os.path.join(OUTPUT_DIR, f"sound pack {timestamp}")

    if not os.path.exists(new_output_dir):
        os.makedirs(new_output_dir)

    for i in range(num_sounds):
        output_file = os.path.join(new_output_dir, f"{prefix}_{i}.wav")
        generate_random_sound(output_file, randomness_factor, max_duration)  # <-- pass max_duration here
        print(f"Generated {output_file}")



#====================================================================================
#====================================================================================


# G U I
def start_gui():
    root = tk.Tk()
    root.title("Random Sound Generator")

    # Sound Properties Frame
    sound_frame = tk.LabelFrame(root, text="Sound Properties", padx=10, pady=10)
    sound_frame.pack(padx=20, pady=20, fill=tk.X)

    tk.Label(sound_frame, text="Number of Sounds:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    num_sounds_entry = tk.Entry(sound_frame)
    num_sounds_entry.grid(row=0, column=1, padx=5, pady=5)
    num_sounds_entry.insert(0, "16")

    tk.Label(sound_frame, text="Max Duration (in milliseconds):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    length_slider = tk.Scale(sound_frame, from_=400, to=6000, resolution=100, orient=tk.HORIZONTAL)
    length_slider.grid(row=1, column=1, padx=5, pady=5)
    length_slider.set(6000)

    # Randomness Settings Frame
    randomness_frame = tk.LabelFrame(root, text="Randomness Settings", padx=10, pady=10)
    randomness_frame.pack(padx=20, pady=20, fill=tk.X)

    tk.Label(randomness_frame, text="Randomness Factor:").pack(side=tk.LEFT, padx=5, pady=5)
    randomness_slider = tk.Scale(randomness_frame, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL)
    randomness_slider.pack(fill=tk.X, expand=True, padx=5, pady=5)
    randomness_slider.set(0.5)

    # File Settings Frame
    file_frame = tk.LabelFrame(root, text="File Settings", padx=10, pady=10)
    file_frame.pack(padx=20, pady=20, fill=tk.X)

    tk.Label(file_frame, text="Filename Prefix:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    prefix_entry = tk.Entry(file_frame)
    prefix_entry.grid(row=0, column=1, padx=5, pady=5)
    prefix_entry.insert(0, "sound")

    # Generate Button
    def on_generate():
        try:
            num_sounds = int(num_sounds_entry.get())
            prefix = prefix_entry.get()
            randomness_factor = randomness_slider.get()
            max_duration = length_slider.get()
            main(num_sounds, prefix, randomness_factor)  # Updated main call
            messagebox.showinfo("Success", "Sounds generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    generate_btn = tk.Button(root, text="Generate Sounds", command=on_generate)
    generate_btn.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    start_gui()
