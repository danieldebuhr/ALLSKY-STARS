import getopt
import sys
from PIL import Image


def main(argv):

    imagefile = None
    testoutputfile = None

    schwellwert = 150
    pixels = 8

    try:
        opts, args = getopt.getopt(argv, "i:o:s:")
    except getopt.GetoptError:
        print 'allsky_stars.py -i <imageFile> [-s <schwellwert=150,0...255> -o <testOutputFile>]'
        sys.exit(2)

    if len(argv) == 0:
        print 'allsky_stars.py -i <imageFile> [-s <schwellwert=150,0...255> -o <testOutputFile>]'
        sys.exit(2)

    for opt, arg in opts:
        if opt in "-i":
            imagefile = arg
        elif opt in "-o":
            testoutputfile = arg
        elif opt in "-s":
            schwellwert = int(arg)

    # Bild oeffnen
    try:
        im = Image.open(imagefile)
    except IOError:
        print 'Could no open ' + imagefile
        sys.exit(2)

    w, h = im.size

    # Schwarz/Weiss reicht aus
    im = im.draft("L", (w, h))

    zones = []
    stars = []

    # Im Bereich des gefundenen Pixels wird eine Zone gezogen, die fuer andere High-Pixel tabu ist
    def zone(x, y):
        inzone = False
        for z in zones:
            if z[0][0] < x < z[1][0] and z[0][1] < y < z[1][1]:
                inzone = True
        if not inzone:
            zones.append(((x-pixels if x-pixels > 0 else 0, y-pixels if y-pixels > 0 else 0), (x+pixels if x+pixels < w else w, y+pixels if y+pixels < h else h)))
            return True
        else:
            return False

    # Alle Pixel durchgehen, alles ab einen Schwellwert pruefen
    for i in range(0, w):
        for j in range(0, h):
            pixel = im.getpixel((i, j))
            if pixel > schwellwert:
                if zone(i, j):
                    stars.append((pixel, i, j))

    # Anzahl der gefundenen Sterne ausgeben
    print len(stars)

    # Output-Image erzeugen, wenn gewuenscht
    if testoutputfile:
        im2 = Image.new("L", (w, h))
        pix = im2.load()
        for i in range(0, w):
            for j in range(0, h):
                pix[i, j] = 0

        for star in stars:
            pix[star[1], star[2]] = star[0]

        try:
            im2.save(testoutputfile)
        except IOError:
            print 'Could not save ' + testoutputfile
            sys.exit(2)

    sys.exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])