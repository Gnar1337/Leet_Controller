# Leet_Controller

A Python MIDI script for FL Studio that captures 8 eighth notes from user input and automatically creates a pattern with those notes.

## Features

- Automatically captures 8 consecutive MIDI note inputs
- Creates a pattern with the 8 notes as eighth notes (spanning one measure in 4/4 time)
- Each note retains its original pitch and velocity
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
   - Display a confirmation message
   - Prepare the notes for pattern creation

4. To create the pattern in FL Studio:
   - **Manual Method**: The captured notes are logged to the console. You can manually add them to the piano roll at the positions indicated (48 ticks apart)
   - **Recording Method**: Enable recording mode in FL Studio, position the playhead, and press Play. The controller will automatically play back the 8 notes at eighth note intervals for recording

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
- Implements automatic playback functionality for easy pattern recording
- Compatible with FL Studio's native MIDI recording system

## Implementation Notes

The FL Studio MIDI Scripting API has limitations on direct pattern manipulation. This script uses a hybrid approach:

1. **Capture Phase**: Records 8 MIDI notes with their properties (pitch, velocity)
2. **Logging**: Outputs note information to the console for manual entry
3. **Playback Mode**: Optionally replays notes during FL Studio recording for automatic pattern creation

For direct pattern manipulation (if supported in your FL Studio version), the script structure allows for future extension with native API calls.

## API Reference

This script implements the following FL Studio MIDI script callbacks:
- `OnInit()` - Initialization and state setup
- `OnDeInit()` - Cleanup when script is unloaded
- `OnMidiIn(event)` - MIDI input processing and event routing
- `OnNoteOn(event)` - Note capture and recording logic
- `OnIdle()` - Continuous callback for automated note playback during recording
- Additional callbacks (OnRefresh, OnUpdateBeatIndicator, etc.) for FL Studio compatibility

## License

Open source - feel free to modify and distribute