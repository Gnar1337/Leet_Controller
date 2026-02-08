# Leet_Controller

A Python MIDI script for FL Studio that captures 8 eighth notes from user input and displays a pattern definition with those notes.

## Features

- Automatically captures 8 consecutive MIDI note inputs
- Displays a formatted pattern definition with the 8 notes as eighth notes (spanning one measure in 4/4 time)
- Each note retains its original pitch and velocity
- Shows note positions in both ticks and beats for easy manual entry
- Ready for next recording immediately after pattern creation

## Installation

1. Locate your FL Studio MIDI Scripts folder:
   - Windows: `C:\Users\<YourUsername>\Documents\Image-Line\FL Studio\Settings\Hardware`
   - macOS: `~/Documents/Image-Line/FL Studio/Settings/Hardware`

2. Copy `device_Leet_Controller.py` to the MIDI Scripts folder

3. Restart FL Studio

4. Enable the controller:
   - Go to Options → MIDI Settings
   - Find "Leet Controller" in the controller list
   - Enable it and select your MIDI input device

## Usage

1. Once enabled, the controller will automatically start listening for MIDI input

2. Play any 8 notes on your MIDI keyboard or controller

3. After the 8th note is received, the controller will:
   - Capture those 8 notes with their velocities
   - Display a formatted pattern definition in the console
   - Show note positions in ticks and beats for manual entry into the piano roll

4. To add the pattern to FL Studio:
   - Open the piano roll for your desired channel
   - Manually add the notes at the positions shown in the console
   - Each note's MIDI number, velocity, and position (in ticks or beats) is displayed

5. The controller will reset and be ready for the next 8 notes

### Pattern Details

- Each note is spaced 48 ticks apart (1 eighth note at 96 PPQ)
- 8 eighth notes = 1 measure in 4/4 time
- Notes preserve their original pitch and velocity

## Technical Details

- Follows the FL Studio MIDI Scripting API
- Each eighth note is 48 ticks (assuming standard 96 PPQ)
- 8 eighth notes span one complete measure in 4/4 time
- Notes preserve their original velocity values
- Pattern information is displayed in a formatted table for easy manual entry

## Implementation Notes

The FL Studio MIDI Scripting API has limitations on direct pattern manipulation. This script uses a capture-and-display approach:

1. **Capture Phase**: Records 8 MIDI notes with their properties (pitch, velocity)
2. **Display Phase**: Outputs formatted pattern information to the console with precise positioning
3. **Manual Entry**: User manually adds notes to the piano roll using the displayed information

This approach avoids using FL Studio's recording system and provides a clean pattern definition for manual implementation.

## API Reference

This script implements the following FL Studio MIDI script callbacks:
- `OnInit()` - Initialization and state setup
- `OnDeInit()` - Cleanup when script is unloaded
- `OnMidiIn(event)` - MIDI input processing and event routing
- `OnNoteOn(event)` - Note capture logic
- Additional callbacks (OnRefresh, OnUpdateBeatIndicator, etc.) for FL Studio compatibility

## License

Open source - feel free to modify and distribute