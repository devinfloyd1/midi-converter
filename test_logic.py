
from chord_parser import parse_chord
from midi_generator import create_midi_file

def test_logic():
    chords = ["Cm7", "F7", "Bbmaj7"]
    parsed = []
    print("Testing Parsing:")
    for c in chords:
        try:
            notes = parse_chord(c)
            print(f"{c} -> {notes}")
            parsed.append(notes)
        except Exception as e:
            print(f"Error parsing {c}: {e}")
            
    print("\nTesting MIDI Generation...")
    try:
        mid = create_midi_file(parsed)
        mid.save("test_output.mid")
        print("Successfully saved test_output.mid")
    except Exception as e:
        print(f"Error generating MIDI: {e}")

if __name__ == "__main__":
    test_logic()
