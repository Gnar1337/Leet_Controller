# name=Leet Controller
# url=https://github.com/Gnar1337/Leet_Controller

"""
Leet Controller - FL Studio MIDI Script
This controller waits for 8 eighth notes from the user for one measure,
then creates a pattern definition with the 8 notes in place.
The pattern can be manually entered into FL Studio's piano roll.
"""

import patterns
import channels
import ui

# Constants
TICKS_PER_EIGHTH = 48  # 48 ticks = 1 eighth note at 96 PPQ
MAX_NOTES = 8  # Number of notes to capture for one measure

# Controller state
recording_notes = []
is_recording = False
current_step = 0

def OnInit():
    """
    Called when FL Studio starts or when the script is reloaded.
    Initialize the controller state.
    """
    global recording_notes, is_recording, current_step
    
    recording_notes = []
    is_recording = False
    current_step = 0
    
    print("Leet Controller Initialized")
    print("Press any MIDI note 8 times to create a pattern")
    print("The controller will display the pattern for you to manually enter")


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
    Create a pattern definition with the 8 recorded notes.
    Each note is placed as an eighth note (1/8th of a measure).
    
    This function displays the pattern information for manual entry
    into FL Studio's piano roll.
    """
    global recording_notes
    
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
        
        print(f"\n{'='*60}")
        print(f"PATTERN CREATED - Pattern {current_pattern}, Channel {channel_index}")
        print(f"{'='*60}")
        
        # Show success message
        ui.setHintMsg("Leet Controller: Pattern created! Check console for details.")
        
        print("\nPattern Details:")
        print(f"  Pattern Number: {current_pattern}")
        print(f"  Channel: {channel_index}")
        print(f"  Time Signature: 4/4")
        print(f"  Total Duration: 1 measure (8 eighth notes)")
        
        print("\nNotes in pattern:")
        print(f"  {'#':<4} {'MIDI Note':<12} {'Velocity':<10} {'Position (ticks)':<20} {'Position (beats)':<15}")
        print(f"  {'-'*4} {'-'*12} {'-'*10} {'-'*20} {'-'*15}")
        
        # Log captured notes with their timing information
        for i, note_data in enumerate(recording_notes):
            note = note_data['note']
            velocity = note_data['velocity']
            position_ticks = i * TICKS_PER_EIGHTH
            position_beats = i * 0.5  # Each eighth note is 0.5 beats
            
            print(f"  {i+1:<4} {note:<12} {velocity:<10} {position_ticks:<20} {position_beats:<15.1f}")
        
        print(f"\n{'='*60}")
        print("Pattern ready for manual entry into FL Studio piano roll!")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"Error in pattern creation: {e}")
        import traceback
        traceback.print_exc()


def OnRefresh(flags):
    """
    Called when the script needs to refresh its state.
    
    Args:
        flags: Refresh flags indicating what changed
    """
    pass


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
