
import streamlit as st
import io
import os
from chord_parser import parse_chord
from midi_generator import create_midi_file

st.set_page_config(page_title="Text-to-MIDI Converter", page_icon="🎵")

st.title("🎵 Text-to-MIDI Converter")
st.markdown("""
Enter a chord progression below to generate a MIDI file.
Separate chords with dashes `-` or spaces. 
Example: `Cm7 - F7 - Bbmaj7` or `C G Am F`
""")

# Input
chord_input = st.text_area("Chord Progression", height=100, placeholder="Cm7 - F7 - Bbmaj7")

if st.button("Generate MIDI"):
    if not chord_input.strip():
        st.error("Please enter a chord progression.")
    else:
        # Split by - or space
        # Normalize delimiters
        normalized = chord_input.replace('-', ' ')
        raw_chords = normalized.split()
        
        parsed_chords = []
        errors = []
        
        for ch in raw_chords:
            ch_clean = ch.strip()
            if not ch_clean:
                continue
            try:
                notes = parse_chord(ch_clean)
                parsed_chords.append(notes)
            except ValueError as e:
                errors.append(str(e))
        
        if errors:
            st.error("Error parsing chords:")
            for err in errors:
                st.write(f"- {err}")
        else:
            # Generate MIDI
            try:
                mid = create_midi_file(parsed_chords)
                
                # Save to buffer
                bio = io.BytesIO()
                mid.save(file=bio)
                
                st.success("MIDI file generated successfully!")
                
                st.download_button(
                    label="Download MIDI",
                    data=bio.getvalue(),
                    file_name="progression.mid",
                    mime="audio/midi"
                )
                
            except Exception as e:
                st.error(f"Error generating MIDI: {e}")

st.markdown("---")
st.caption("Common chord qualities supported: maj, min, 7, maj7, m7, dim, dim7, aug, 9.")
