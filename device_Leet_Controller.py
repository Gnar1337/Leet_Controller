# name=Leet Controller
# url=https://github.com/Gnar1337/Leet_Controller

"""
Leet Controller - FL Studio MIDI Script
This controller waits for 8 eighth notes from the user for one measure,
then creates a pattern with the 8 notes in place by replaying them
into FL Studio's recording system.
"""

import patterns
import channels
import mixer
import device
import transport
import ui
import playlist
import arrangement
import time

# Constants
MAX_NOTES = 8  # Number of notes to capture for one measure

# Dynamic values (calculated based on tempo)
ticks_per_eighth = 48  # Will be calculated dynamically based on FL Studio's PPQ
current_tempo = 120.0  # Track the current tempo

# Controller state
recording_notes = []
is_recording = False
playback_notes = []
playback_index = 0
is_playing_back = False
current_step = 0

def calculate_ticks_per_eighth():
    """
    Calculate ticks per eighth note based on FL Studio's PPQ.
    FL Studio uses PPQ (Pulses Per Quarter note) system.
    An eighth note is half a quarter note, so ticks = PPQ / 2.
    Note: PPQ is independent of tempo - it's a resolution setting.
    """
    # FL Studio typically uses 96 PPQ (can be 192 or higher in some versions)
    ppq = 96  # FL Studio default PPQ
    return ppq // 2  # Eighth note = half of quarter note

def update_tempo():
    """
    Track tempo changes and update the ticks_per_eighth value if needed.
    Called whenever tempo might have changed.
    Note: While ticks_per_eighth depends on PPQ (not tempo), this function
    tracks tempo changes to ensure timing calculations stay synchronized.
    """
    global ticks_per_eighth, current_tempo
    
    # Get current tempo from FL Studio
    new_tempo = transport.getRunningTempo()
    
    if new_tempo != current_tempo:
        current_tempo = new_tempo
        ticks_per_eighth = calculate_ticks_per_eighth()
        print(f"Tempo changed to {current_tempo} BPM")
        print(f"Ticks per eighth note: {ticks_per_eighth}")

def OnInit():
    """
    Called when FL Studio starts or when the script is reloaded.
    Initialize the controller state.
    """
    global recording_notes, is_recording, current_step
    global playback_notes, playback_index, is_playing_back
    global ticks_per_eighth, current_tempo
    
    recording_notes = []
    is_recording = False
    current_step = 0
    playback_notes = []
    playback_index = 0
    is_playing_back = False
    
    # Initialize tempo and ticks calculation
    update_tempo()
    
    print("Leet Controller Initialized")
    print(f"Current tempo: {current_tempo} BPM")
    print(f"Ticks per eighth note: {ticks_per_eighth}")
    print("Press any MIDI note 8 times to create a pattern")
    print("The controller will replay the notes for pattern creation")


def OnDeInit():
    """
    Called when FL Studio closes or when the script is unloaded.
    """
    print("Leet Controller Deinitialized")


def OnMidiIn(event):
    """
    Called when a MIDI message is received.
    This is the main entry point for processing MIDI input.
    
    event.status: MIDI status byte
    event.data1: First data byte (note number for Note On/Off)
    event.data2: Second data byte (velocity for Note On/Off)
    event.handled: Set to True to prevent FL Studio from processing this event
    """
    # Check if this is a Note On event (status in range 144-159, which is 0x90-0x9F)
    if (event.status >= 144 and event.status <= 159):
        OnNoteOn(event)
        # Mark event as handled to prevent FL Studio from processing it again
        # This prevents double recording while we're capturing notes
        if is_recording:
            event.handled = True
    else:
        event.handled = False


def OnNoteOn(event):
    """
    Process Note On events to capture the 8 notes for pattern creation.
    
    Args:
        event: MIDI event object containing note information
    """
    global recording_notes, is_recording, current_step
    
    note_number = event.data1
    velocity = event.data2
    
    # If velocity is 0, treat it as Note Off
    if velocity == 0:
        return
    
    # Start recording automatically when first note is received
    if not is_recording:
        is_recording = True
        recording_notes = []
        current_step = 0
        print("Started recording notes...")
    
    # Record the note
    if len(recording_notes) < MAX_NOTES:
        recording_notes.append({
            'note': note_number,
            'velocity': velocity,
            'step': current_step
        })
        current_step += 1
        
        print(f"Note {len(recording_notes)}/{MAX_NOTES} recorded: Note {note_number}, Velocity {velocity}")
        
        # When we have all 8 notes, create the pattern
        if len(recording_notes) == MAX_NOTES:
            CreatePattern()
            # Reset for next recording
            is_recording = False
            recording_notes = []
            current_step = 0
            print("Pattern created! Ready for next 8 notes.")


def CreatePattern():
    """
    Create a new pattern in FL Studio with the 8 recorded notes.
    Each note is placed as an eighth note (1/8th of a measure).
    
    This function works by replaying the recorded notes back into FL Studio
    while recording is enabled, effectively creating the pattern.
    """
    global recording_notes, playback_notes, playback_index, is_playing_back
    
    if len(recording_notes) != MAX_NOTES:
        print(f"Error: Need exactly {MAX_NOTES} notes, but have {len(recording_notes)}")
        return
    
    try:
        # Get current pattern
        current_pattern = patterns.patternNumber()
        
        # Get the active channel
        channel_index = channels.selectedChannel()
        if channel_index < 0:
            channel_index = 0
        
        print(f"Creating pattern {current_pattern} on channel {channel_index}")
        
        # Store notes for playback
        playback_notes = recording_notes.copy()
        playback_index = 0
        is_playing_back = True
        
        # Show instruction message
        ui.setHintMsg("Leet Controller: Enable recording and press play to create pattern!")
        
        print("Pattern ready!")
        print("To create the pattern:")
        print("  1. Enable recording mode in FL Studio")
        print("  2. Position playhead at desired location")
        print("  3. Press Play - the notes will be automatically played back")
        print("  4. The pattern will be created with your 8 notes")
        
        # Log captured notes with their timing information
        for i, note_data in enumerate(recording_notes):
            note = note_data['note']
            velocity = note_data['velocity']
            position = i * ticks_per_eighth
            
            print(f"  Note {i+1}: MIDI note {note}, velocity {velocity}, position {position} ticks")
        
        print("\nNotes captured successfully!")
        print(f"Total notes: {len(recording_notes)}")
        
    except Exception as e:
        print(f"Error in pattern creation: {e}")
        import traceback
        traceback.print_exc()


def OnIdle():
    """
    Called continuously when FL Studio is idle.
    Used for automated playback of captured notes during recording.
    """
    global playback_notes, playback_index, is_playing_back
    
    if not is_playing_back or len(playback_notes) == 0:
        return
    
    # Check if transport is playing and recording
    if transport.isPlaying() and transport.isRecording():
        # Get current song position in ticks
        current_pos = transport.getSongPos()
        
        if playback_index < len(playback_notes):
            expected_pos = playback_index * ticks_per_eighth
            
            # Check if it's time to play the next note
            if current_pos >= expected_pos:
                note_data = playback_notes[playback_index]
                note = note_data['note']
                velocity = note_data['velocity']
                
                # Send note on event
                channel = channels.selectedChannel()
                if channel >= 0:
                    try:
                        # Trigger the note
                        channels.midiNoteOn(channel, note, velocity)
                        print(f"Playing back note {playback_index + 1}/{MAX_NOTES}: {note}")
                    except (AttributeError, RuntimeError) as e:
                        print(f"Warning: Could not play back note: {e}")
                
                playback_index += 1
        else:
            # Finished playing all notes
            is_playing_back = False
            playback_index = 0
            print("Playback complete! Pattern created.")
            ui.setHintMsg("Leet Controller: Pattern created!")


def OnRefresh(flags):
    """
    Called when the script needs to refresh its state.
    Use this to detect tempo changes.
    
    Args:
        flags: Refresh flags indicating what changed
    """
    # HW_Dirty_Tempo flag = 16 (tempo changed)
    if flags & 16:  # Tempo changed
        update_tempo()


def OnUpdateBeatIndicator(value):
    """
    Called when the beat indicator is updated.
    
    Args:
        value: Beat indicator value
    """
    pass


def OnDisplayZone():
    """
    Called to update the display zone.
    """
    pass


def OnUpdateLiveMode(lastTrack):
    """
    Called when live mode is updated.
    
    Args:
        lastTrack: Last track number
    """
    pass


def OnDirtyMixerTrack(index):
    """
    Called when a mixer track becomes dirty (modified).
    
    Args:
        index: Mixer track index
    """
    pass


def OnDirtyChannel(index):
    """
    Called when a channel becomes dirty (modified).
    
    Args:
        index: Channel index
    """
    pass
