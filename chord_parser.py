
import re

# Base MIDI note for middle C (C4) is 60.
NOTE_MAP = {
    'C': 0, 'C#': 1, 'Db': 1,
    'D': 2, 'D#': 3, 'Eb': 3,
    'E': 4,
    'F': 5, 'F#': 6, 'Gb': 6,
    'G': 7, 'G#': 8, 'Ab': 8,
    'A': 9, 'A#': 10, 'Bb': 10,
    'B': 11
}

def parse_chord(chord_str, octave=4):
    """
    Parses a chord string into a list of MIDI note numbers.
    Example: 'Cm7' -> [60, 63, 67, 70] (if root is C4)
    """
    chord_str = chord_str.strip()
    if not chord_str:
        return []

    # Regex: Root (A-G), Accidental (# or b), Quality (rest)
    match = re.match(r'^([A-G])(#|b)?(.*)$', chord_str) 
    # Note: checking case-sensitive for quality, but root usually Capital.
    # If user types 'cm7', we should handle 'c' as 'C'.
    
    if not match:
        # Try capitalizing first letter only?
        # Let's try to match case-insensitively for Root.
        match = re.match(r'^([a-gA-G])(#|b)?(.*)$', chord_str)
        if not match:
            raise ValueError(f"Invalid chord format: {chord_str}")

    root_char = match.group(1).upper()
    accidental = match.group(2) if match.group(2) else ''
    quality_raw = match.group(3)

    full_root = root_char + accidental
    
    # Resolve root MIDI base
    if full_root in NOTE_MAP:
        base_val = NOTE_MAP[full_root]
    else:
        # Enharmonics not in map (e.g. Cb, E#, etc.)
        if full_root == 'Cb': base_val = 11; octave -= 1
        elif full_root == 'E#': base_val = 5
        elif full_root == 'Fb': base_val = 4
        elif full_root == 'B#': base_val = 0; octave += 1
        else:
            raise ValueError(f"Unknown root: {full_root}")

    root_midi = base_val + (octave + 1) * 12

    # Parse Quality
    # Map common qualities to semitone intervals
    # We need to handle 'm', 'min', 'maj', '7', etc.
    
    # Normalizing quality string for easier mapping
    # 'maj7' -> 'maj7'
    # 'M7' -> 'maj7' ? No, 'M' usually implies Major. 
    # 'm7' -> minor 7.
    
    q = quality_raw
    
    intervals = [0, 4, 7] # Default Major

    if q == '' or q == 'M' or q == 'maj':
        intervals = [0, 4, 7]
    elif q == 'm' or q == 'min' or q == '-':
        intervals = [0, 3, 7]
    elif q == '7' or q == 'dom7':
        intervals = [0, 4, 7, 10]
    elif q == 'maj7' or q == 'M7' or q == 'Maj7':
         intervals = [0, 4, 7, 11]
    elif q == 'm7' or q == 'min7' or q == '-7':
        intervals = [0, 3, 7, 10]
    elif q == 'dim':
        intervals = [0, 3, 6]
    elif q == 'dim7' or q == 'o7':
        intervals = [0, 3, 6, 9]
    elif q == 'aug' or q == '+':
        intervals = [0, 4, 8]
    elif q == '9' or q == 'dom9':
        intervals = [0, 4, 7, 10, 14]
    elif q == 'maj9':
        intervals = [0, 4, 7, 11, 14]
    elif q == 'm9' or q == 'min9':
        intervals = [0, 3, 7, 10, 14]
    elif q == '11' or q == 'dom11':
        intervals = [0, 4, 7, 10, 14, 17]
    elif q == '13' or q == 'dom13':
        intervals = [0, 4, 7, 10, 14, 21]
    elif q == 'sus4':
        intervals = [0, 5, 7]
    elif q == 'sus2':
        intervals = [0, 2, 7]
    else:
        # Fallback or strict?
        # If it's something like 'Cm9', q is 'm9'.
        # Let's try to handle cases we missed or default to major?
        # Better to error so user knows.
        raise ValueError(f"Unknown chord quality: '{q}' in '{chord_str}'")

    return [root_midi + i for i in intervals]
