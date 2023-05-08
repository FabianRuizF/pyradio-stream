
import pyaudio
import wave

wf = wave.open("tmp.wav", 'rb') 
print(dir(wf))
p = pyaudio.PyAudio()
samp = p.get_format_from_width(wf.getsampwidth())
channels = wf.getnchannels()
rate = wf.getframerate()

print(wf.getsampwidth())
print(samp,channels,rate,wf.getsampwidth())
