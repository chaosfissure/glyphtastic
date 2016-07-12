# glyphtastic

This project page is dedicated to Python scripts I create to generate patterns of lines or blocks to look like glyphs, letters, or things of that sort.


# glyphgen.py

Use of this script can be tweaked manually if you want custom effects. 

If you're just looking to generate different numbers of glyphs, force glyphs to behave in various ways during setup, and don't really want to dig into the code, the following command line args are for you:

`vglyphs=tall` and `hglyphs=wide` - the generated image contains glyphs expanding `tall` down and `wide` to the right.

`vblocks=height` and `hblocks=width` - each glyph contains `width` horizontal blocks and `height` vertical blocks.

`blocksize=px` - the square blocks used to create glyphs are `px` x `px` in area.

`mode=what` - `what` is either `0`, `1`, or `2`. `0` means "lots of vertical lines", `1` means "a lot more angles," and `2` means "randomize parameters."

`exclusive=prob` - `prob` represents the chance that we only create a connection from one block down to another block, rather than down to the sides.  `1.0` means it will never have areas that cross over each other, `0.0` means that it always tries to send connections to the left and right from the current block.

`fixed=val` - `val` being either `0` (use time to randomize - ensures different results each run of the program) or `1` (each time you run the program, the results should be consistent).


