# Music Player with Synchronized Lyrics

A Python-based music player that displays synchronized lyrics word by word, creating an engaging karaoke-like experience. The player supports MP3 files and custom lyrics in JSON format.

## Features

- 🎵 MP3 music playback
- 📝 Synchronized word-by-word lyrics display
- 🎨 Color-coded word highlighting
- ⏱️ Precise timing control
- 🎯 Support for custom lyrics files
- 🎨 Beautiful console-based interface

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
```

2. Install the required dependencies:
```bash
pip install pygame
```

## Usage

1. Prepare your files:
   - Place your MP3 file in the project directory
   - Create a lyrics file in JSON format (see example below)

2. Run the player:
```bash
python lyrics.py
```

## Lyrics File Format

The lyrics should be in JSON format with the following structure:
```json
[
    {"time": "1:25", "text": "Your lyrics line here"},
    {"time": "1:36", "text": "Next lyrics line"},
    ...
]
```

- `time`: Format should be "MM:SS" (minutes:seconds)
- `text`: The actual lyrics line

## Example

```python
# Configuration
mp3_file = "your_song.mp3"
lyrics_file = "lyrics.json"

# Create and run the player
player = MusicLyricsPlayer(mp3_file, lyrics_file)
player.run()
```

## Features in Detail

- **Word-by-Word Display**: Each word appears with precise timing
- **Color Coding**: 
  - Current word: Yellow and bold
  - Previous words: Gray
  - Complete line: Green
- **Synchronization**: Lyrics are perfectly timed with the music
- **Customizable Timing**: Adjust word display speed as needed

## Developer

Developed by **Sushank Lamichhane**

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 