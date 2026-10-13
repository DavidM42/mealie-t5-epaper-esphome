"""Makes the black and white picture of an album cover for the e-paper display.

The package music_epaper.yaml runs this inside Home Assistant:

    python3 epaper_cover.py <address of the cover> <file to write> <size in pixels>

The display has no grey. So the cover becomes a square picture of black and white dots, where many black dots
close together look dark and few look light.
"""

import io
import os
import sys
import urllib.request

from PIL import Image, ImageOps

address, target, size = sys.argv[1], sys.argv[2], int(sys.argv[3])

with urllib.request.urlopen(address, timeout=20) as response:
    cover = Image.open(io.BytesIO(response.read()))

# Grey, cut to a square, and stretched so that the darkest part is black and the lightest is white.
cover = ImageOps.fit(cover.convert("L"), (size, size), Image.Resampling.LANCZOS)
cover = ImageOps.autocontrast(cover, cutoff=1)

# The display may be loading the picture that is there now. So the new one is written next to it and then
# takes its place in one step.
cover.convert("1").save(target + ".new", "BMP")
os.replace(target + ".new", target)
