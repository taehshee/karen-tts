from flask import Flask, request, jsonify, render_template
import os
from pydub import AudioSegment

app = Flask(__name__)

# Path to the folder containing audio files
AUDIO_FOLDER = "static/audio_files/"  # Update this path with your actual folder

# Load available words
word_audio_map = {file.split('.')[0]: os.path.join(AUDIO_FOLDER, file) for file in os.listdir(AUDIO_FOLDER) if file.endswith('.wav')}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/tts', methods=['POST'])
def text_to_speech():
    data = request.json
    text = data.get("text", "").strip()
    words = text.split()
    
    audio_clips = []
    for word in words:
        audio_path = word_audio_map.get(word)
        if audio_path:
            audio_clips.append(AudioSegment.from_wav(audio_path))
        else:
            print(f"Warning: No audio found for '{word}'")
    
    if audio_clips:
        combined_audio = sum(audio_clips)  # Merge clips
        output_path = "static/output_sentence.wav"
        combined_audio.export(output_path, format="wav")
        return jsonify({"message": "Audio generated", "file": output_path})
    else:
        return jsonify({"error": "No valid words found"})

if __name__ == '__main__':
    app.run(debug=True)
