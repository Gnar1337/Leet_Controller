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
   - Create a pattern with those 8 notes
   - Place each note as an eighth note in sequence
   - Display a confirmation message
   - Reset and be ready for the next 8 notes

4. The pattern will be created on the currently selected channel

## Technical Details

- Follows the FL Studio MIDI Scripting API
- Each eighth note is 48 ticks (assuming standard 96 PPQ)
- 8 eighth notes span one complete measure in 4/4 time
- Notes preserve their original velocity values

## API Reference

This script implements the following FL Studio MIDI script callbacks:
- `OnInit()` - Initialization
- `OnDeInit()` - Cleanup
- `OnMidiIn(event)` - MIDI input processing
- `OnNoteOn(event)` - Note processing

## License

Open source - feel free to modify and distribute