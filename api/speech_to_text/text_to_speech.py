"""Bismillahirrahmanirahim
   Elhamdulillahirabbulalemin
   Esselatu vesselamu ala rasulina Muhammedin ve ala alihi ecmain
   ALLAH U Teala bizleri bu ilimden faydalandırsın.
   Amin.
"""
"""
Text-to-Speech Pipeline (PyTorch + torchaudio TTS)
Bu modül, verilen metni ses dosyasına çevirir. Basit bir örnek için torchaudio TTS veya pyttsx3 kullanılabilir.
"""
import pyttsx3

def text_to_speech(text, output_path='output.wav', lang='tr'):
    """
    Converts text to speech and saves as a WAV file.
    Args:
        text (str): Text to synthesize.
        output_path (str): Path to save the output WAV file.
        lang (str): Language code (default: 'tr' for Turkish)
    """
    engine = pyttsx3.init()
    # Set language if supported
    for voice in engine.getProperty('voices'):
        if lang in voice.languages[0].decode('utf-8'):
            engine.setProperty('voice', voice.id)
            break
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    print(f'Saved synthesized speech to {output_path}')

# Kullanım örneği:
# text_to_speech('Merhaba dünya', 'output.wav')
