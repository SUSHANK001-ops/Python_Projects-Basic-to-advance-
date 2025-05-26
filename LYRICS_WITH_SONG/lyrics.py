import pygame
import threading
import time
import os
import json
from datetime import datetime, timedelta

class MusicLyricsPlayer:
    def __init__(self, mp3_file, lyrics_file):
        self.mp3_file = mp3_file
        self.lyrics_file = lyrics_file
        self.lyrics = []
        self.current_lyric_index = 0
        self.start_time = None
        self.is_playing = False
        
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Load lyrics
        self.load_lyrics()
    
    def load_lyrics(self):
        """Load lyrics with timestamps from a JSON file"""
        try:
            with open(self.lyrics_file, 'r', encoding='utf-8') as f:
                self.lyrics = json.load(f)
        except FileNotFoundError:
            print(f"Lyrics file '{self.lyrics_file}' not found!")
            print("Please create a lyrics file with the format shown in the example.")
            return False
        except json.JSONDecodeError:
            print(f"Invalid JSON format in '{self.lyrics_file}'")
            return False
        
        # Sort lyrics by timestamp
        self.lyrics.sort(key=lambda x: x['time'])
        return True
    
    def time_to_seconds(self, time_str):
        """Convert time string (MM:SS or MM:SS.mmm) to seconds"""
        parts = time_str.split(':')
        minutes = int(parts[0])
        seconds = float(parts[1])
        return minutes * 60 + seconds
    
    def play_music(self):
        """Play the MP3 file"""
        try:
            pygame.mixer.music.load(self.mp3_file)
            pygame.mixer.music.play()
            self.is_playing = True
            self.start_time = time.time()
            print(f"🎵 Now playing: {os.path.basename(self.mp3_file)}")
            print("=" * 50)
        except pygame.error as e:
            print(f"Error playing music: {e}")
            return False
        return True
    
    def display_lyrics_word_by_word(self):
        """Display lyrics word by word synchronized with music playback"""
        if not self.lyrics:
            return
        
        # Fixed time per word in seconds
        FIXED_TIME_PER_WORD = 1.2 # Each word will be displayed for 1.2 seconds
        
        while self.is_playing and pygame.mixer.music.get_busy():
            current_time = time.time() - self.start_time
            
            # Check if it's time to display the next lyric line
            if (self.current_lyric_index < len(self.lyrics) and 
                current_time >= self.time_to_seconds(self.lyrics[self.current_lyric_index]['time'])):
                
                current_line = self.lyrics[self.current_lyric_index]['text']
                
                # Skip empty lines
                if current_line.strip():
                    # Split line into words
                    words = [w for w in current_line.split() if w.strip()]
                    displayed_words = []
                    
                    # Get timing for this line
                    current_line_time = self.time_to_seconds(self.lyrics[self.current_lyric_index]['time'])
                    
                    # Display words one by one with fixed timing
                    for i, word in enumerate(words):
                        # Wait for the right time for this word
                        word_time = current_line_time + (i * FIXED_TIME_PER_WORD)
                        while time.time() - self.start_time < word_time:
                            if not (self.is_playing and pygame.mixer.music.get_busy()):
                                return
                            time.sleep(0.05)
                        
                        displayed_words.append(word)
                        
                        # Clear and redisplay with highlighting
                        print(f"\r{' ' * 100}", end='')  # Clear line
                        
                        # Show previous words in dim color, current word highlighted
                        line_display = ""
                        for j, w in enumerate(displayed_words):
                            if j == len(displayed_words) - 1:  # Current word
                                line_display += f"\033[1;33m{w}\033[0m "  # Yellow bold
                            else:  # Previous words
                                line_display += f"\033[90m{w}\033[0m "  # Gray
                        
                        print(f"\r{line_display}", end='', flush=True)
                    
                    # Show complete line briefly
                    time.sleep(0.15)
                    print(f"\r\033[92m{current_line}\033[0m")  # Green for complete line
                
                self.current_lyric_index += 1
            
            time.sleep(0.05)  # Check every 50ms for smoother word timing
    
    def display_lyrics(self):
        """Display lyrics synchronized with music playback (original method)"""
        if not self.lyrics:
            print("No lyrics loaded!")
            return
        
        print("\n🎤 Lyrics:\n")
        
        while self.is_playing and pygame.mixer.music.get_busy():
            current_time = time.time() - self.start_time
            
            # Check if it's time to display the next lyric
            if (self.current_lyric_index < len(self.lyrics) and 
                current_time >= self.time_to_seconds(self.lyrics[self.current_lyric_index]['time'])):
                
                # Clear previous line and display current lyric
                print(f"\r{' ' * 80}", end='')  # Clear line
                print(f"\r🎵 {self.lyrics[self.current_lyric_index]['text']}")
                
                self.current_lyric_index += 1
            
            time.sleep(0.1)  # Check every 100ms
    
    def stop(self):
        """Stop music playback"""
        pygame.mixer.music.stop()
        self.is_playing = False
        print("\n\n⏹️  Playback stopped.")
    
    def run(self):
        """Main method to run the music player"""
        if not os.path.exists(self.mp3_file):
            print(f"MP3 file '{self.mp3_file}' not found!")
            return
        
        if not self.lyrics:
            return
        
        if not self.play_music():
            return
        
        print("Starting in 2 seconds...")
        time.sleep(2)
        
        # Start lyrics display in a separate thread
        lyrics_thread = threading.Thread(target=self.display_lyrics_word_by_word)
        lyrics_thread.daemon = True
        lyrics_thread.start()
        
        try:
            # Wait for music to finish or user to stop
            while pygame.mixer.music.get_busy():
                time.sleep(1)
            
        except KeyboardInterrupt:
            self.stop()

def create_sample_lyrics_file(filename="lyrics.json"):
    """Create a sample lyrics file for demonstration"""
    sample_lyrics = [
        {"time": "1:25", "text": "K-cha timro manma, k-cha?"},
        {"time": "1:36", "text": "Bhanideu-na, k-cha"},
        {"time": "1:46", "text": "Ma-nai chu ki? Ki aru nai cha?"},
        {"time": "1:56", "text": "Yadi ma-nai haina bhane bhandihaal-na"},
        {"time": "2:11", "text": "Haawajastai malai udna man cha, aljhaai narakh"},
        {"time": "2:21", "text": "Timilai pani ma birsidinchhu, mutu nadukhaairakh"},
        {"time": "2:31", "text": "Bhaejati sabai maya diẽ, badi bhaecha "},
        {"time": "2:41", "text": "aba Timilai pani ma birsidinchhu, mutu nadukhaairakh"},
        {"time": "2:53", "text": "Bujhauna khojẽ, bhanidiẽ"},
        {"time": "3:04", "text": "Timibaahek kohi chaina aru"},
        {"time": "3:14", "text": "Haaridiẽ, sumpisakẽ timrai khushi bhani"},
        {"time": "3:30", "text": "Ma chahi roidiẽ"},
        {"time": "3:38", "text": "Haawajastai malai udna man cha, aljhaai narakh"},
        {"time": "3:49", "text": "Timilai pani ma birsidinchhu, mutu nadukhaairakh"},
        {"time": "3:59", "text": "Bhaejati sabai maya diẽ, badi bhaecha"},
        {"time": "4:09", "text": "Aba timilai pani ma birsidinchhu, mutu nadukhaairakh"},
        {"time": "5:11", "text": "Haawajastai malai udna man cha, aljhaai narakh"},
        {"time": "5:21", "text": "Timilai pani ma birsidinchhu, mutu nadukhaairakh"},
        {"time": "5:31", "text": "Bhaejati sabai maya diẽ, badi bhaecha"},
        {"time": "5:41", "text": "Aba timilai pani ma birsidinchhu, mutu nadukhaairakh"},
        {"time": "5:55", "text": "Hm, timrai khushi bhani ma chahi roidiẽ"}
    ]
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(sample_lyrics, f, indent=2, ensure_ascii=False)
        print(f"Sample lyrics file created: {filename}")
    except Exception as e:
        print(f"Error creating lyrics file: {e}")

def main():
    print("🎵 Music Player with Synchronized Lyrics 🎵")
    print("=" * 50)
    
    # Configuration
    mp3_file = "HAWAJASTAI.mp3"
    lyrics_file = "lyrics.json"
    
    # Check if files exist, create sample if needed
    if not os.path.exists(mp3_file):
        print(f"MP3 file '{mp3_file}' not found!")
        return
    
    if not os.path.exists(lyrics_file):
        create_sample_lyrics_file(lyrics_file)
    
    # Create and run the player
    player = MusicLyricsPlayer(mp3_file, lyrics_file)
    player.run()

if __name__ == "__main__":
    main()