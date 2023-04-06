import glob
import os

def loadlevel(filename):
    print("searching: ./" + filename + "/*.txt")
    txt = [os.path.basename(f) for f in glob.glob("./" + filename + "/*.txt")][0]
    print("found: ", txt)
    mp3 = [os.path.basename(f) for f in glob.glob("./" + filename + "/*.mp3")][0]
    print("found: ", mp3)
    png = [os.path.basename(f) for f in glob.glob("./" + filename + "/*.png")][0]
    print("found: ", png)

    bpm = 0
    file_content = []
    arrows = ""

    file = open("./" + filename + "/" + txt)
    for line in file:
        file_content.append(line.strip("\n"))

    bpm = file_content[0]
    arrows = file_content[1]

    return bpm, arrows, ("./" + filename + "/" + mp3), ("./" + filename + "/" + png)