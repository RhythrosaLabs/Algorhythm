from pydub import AudioSegment
from pydub.generators import Sine, Square, Sawtooth, Triangle, Pulse
import random
from datetime import datetime
import os

OUTPUT_DIR = "random_sounds"

def add_delay(segment):
    delay_time = random.randint(100, 600)  # Random delay between 100ms to 600ms
    delay_seg = segment._spawn(b"\0" * int(44.1 * delay_time))
    gain_overlay = random.randint(-10, -3)  # Random gain reduction between -10dB to -3dB
    delay_seg = delay_seg.overlay(segment, gain_during_overlay=gain_overlay)
    return delay_seg

def apply_stutter(segment):
    duration_ms = random.randint(10, 150)  # Random stutter duration between 10ms to 150ms
    repeats = random.randint(2, 10)  # Random repeats between 2 to 10
    stutter_piece = segment[:duration_ms]
    stuttered = AudioSegment.empty()
    for _ in range(repeats):
        stuttered += stutter_piece
    return stuttered

def apply_arpeggio(frequency, generator, step=50, steps=5, duration_per_step=100):
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
    return sound + delay + delayed_sound

def makeshift_reverb(sound, num_echoes=3, start_delay=50, decay_factor=-3):
    """Emulate a very simple reverb by layering echoes."""
    reverbed = sound
    for _ in range(num_echoes):
        sound = makeshift_echo(sound, start_delay, decay_factor)
        start_delay *= 1.5
        decay_factor -= 2
    return reverbed.overlay(sound)

def generate_random_sound(filename):
    generators = [Sine, Square, Sawtooth, Triangle, Pulse]
    gen_choice = random.choice(generators)

    # Random frequency between 400Hz and 900Hz
    freq = random.randint(400, 900)

    # Random duration between 0.4s and 6s in milliseconds
    duration = random.randint(400, 3000)

    # Generate the first sound
    freq = random.randint(400, 900)
    sound1 = gen_choice(freq).to_audio_segment(duration=duration)

    # With a 50% probability, generate a second sound and concatenate
    if random.random() > 0.5:
        gen_choice2 = random.choice(generators)
        freq2 = random.randint(400, 900)
        # Adjust duration of the second sound so total doesn't exceed 6s
    max_duration2 = 2000 - duration
    if max_duration2 > 400:
        duration2 = random.randint(400, max_duration2)
        gen_choice2 = random.choice(generators)
        freq2 = random.randint(400, 900)
        sound2 = gen_choice2(freq2).to_audio_segment(duration=duration2)
        sound = sound1 + sound2
    else:
        sound = sound1
          
    # Apply random effects
    if random.random() > 0.5:
        sound = sound + sound.reverse()

    if random.random() > 0.6:
        sound = add_delay(sound)

    if random.random() > 0.7:
        sound = apply_stutter(sound)

    if random.random() > 0.6:
        sound = apply_arpeggio(freq, gen_choice)

    if random.random() < 0.5:
        speed_change = random.uniform(1.1, 1.5)
        if len(sound) > 150: 
            sound = sound.speedup(playback_speed=speed_change)
        else:
            sound = sound.speedup(playback_speed=speed_change, chunk_size=int(len(sound)/2))

    if random.random() > 0.6:
        sound = sound.fade_in(duration=1000)

    if random.random() > 0.6:
        sound = sound.fade_out(duration=1000)

    if random.random() > 0.6:
        sound = sound.invert_phase()

    if random.random() > 0.7:
        cutoff = random.choice([300, 500, 1000, 2000])
        filter_choice = random.choice(['highpass', 'lowpass'])
        if filter_choice == 'highpass':
            sound = sound.high_pass_filter(cutoff)
        else:
            sound = sound.low_pass_filter(cutoff)

    if random.random() > 0.5:
        steps = [1, 9/8, 5/4, 3/2]
        duration_per_step = random.randint(100, 500)
        sound += randomized_arpeggiation(freq, steps, duration_per_step)

    if random.random() > 0.7:
        delay_time = random.randint(100, 500)
        decay_factor = random.uniform(-2, -5)
        sound += makeshift_echo(sound, delay_time, decay_factor)

    if random.random() > 0.7:
        sound += makeshift_reverb(sound)

    sound.export(filename, format="wav")

    # Random Arpeggiation
    if random.random() > 0.5:
        steps = [1, 9/8, 5/4, 3/2]  # Example steps, can be modified
        duration_per_step = random.randint(100, 500)  # Duration in milliseconds
        sound = randomized_arpeggiation(freq, steps, duration_per_step)

        # Echo effect
    if random.random() > 0.7:
        delay_time = random.randint(100, 500)  # Adjust as needed
        decay_factor = random.uniform(-2, -5)  # Adjust as needed
        sound = makeshift_echo(sound, delay_time, decay_factor)

    # Makeshift reverb
    if random.random() > 0.7:
        sound = makeshift_reverb(sound)

def main(num_sounds, prefix):
    # Generate a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create a new directory inside OUTPUT_DIR with "sound pack [timestamp]" as the name
    new_output_dir = os.path.join(OUTPUT_DIR, f"sound pack {timestamp}")

    if not os.path.exists(new_output_dir):
        os.makedirs(new_output_dir)

    for i in range(num_sounds):
        output_file = os.path.join(new_output_dir, f"{prefix}_{i}.wav")
        generate_random_sound(output_file)
        print(f"Generated {output_file}")

if __name__ == "__main__":
    num_sounds = 16  # Adjust as needed
    prefix = "sound"  # Adjust as needed
    main(num_sounds, prefix)
