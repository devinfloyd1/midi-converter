
import mido
from mido import MidiFile, MidiTrack, Message

def create_midi_file(chord_sequence, duration_beats=4, tempo=120):
    """
    Creates a MIDI file from a sequence of chords.
    chord_sequence: List of lists, where each inner list contains MIDI note numbers.
    duration_beats: Number of beats each chord plays.
    tempo: BPM
    """
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    # Set tempo (ticks per beat is default 480)
    # mido.bpm2tempo(tempo) gives us microseconds per beat
    # MetaMessage 'set_tempo'
    
    track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(tempo)))
    
    ticks_per_beat = mid.ticks_per_beat
    duration_ticks = int(ticks_per_beat * duration_beats)
    
    for notes in chord_sequence:
        if not notes:
            # Rest
            track.append(Message('note_off', note=60, velocity=0, time=duration_ticks))
            continue
            
        # Note On for all notes
        # First note has time=0, others time=0 (simultaneous)
        first = True
        for note in notes:
            track.append(Message('note_on', note=note, velocity=64, time=0))
            
        # Note Off for all notes
        # First note off carries the duration (delta time)
        # Others have 0 delta time
        first = True
        for note in notes:
            dt = duration_ticks if first else 0
            track.append(Message('note_off', note=note, velocity=64, time=dt))
            first = False
            
    return mid
