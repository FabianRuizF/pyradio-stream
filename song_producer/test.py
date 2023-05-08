import soundfile as sf

import librosa
x,_ = librosa.load("b_slipout.mp3",sr=22050)
sf.write('tmp_v2.wav', x, 22050)

