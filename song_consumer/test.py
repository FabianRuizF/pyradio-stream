with open("temp.wav", "rb") as fwav:
    print(type(fwav))
    data = fwav.read(1024)
    while data:
        data = fwav.read(1024)
        print(len(data))
