# README

The emulator is based on the official frontend of [mooneye-gb](https://github.com/Gekkio/mooneye-gb/).

Will run `main.gb` in your current working directory. Also requires a valid `dmg_boot.bin` (`32fbbd84168d3482956eb3c5051637f5`) bootrom there. Google is your friend...

If you're running Wayland you may want to set `WINIT_UNIX_BACKEND=x11` in your environment.

**The challenge runs with 10 minute timeout and 60 CPU-seconds (whatever triggers first). If your run is slower, the server will kill the connection without further notice.**
## How to use

### Record your run

This may not be possible in docker, since you may need graphical output.

```sh
tas-emulator record filename
```

### Record file format

The record file is gzipped and can be easily modified for speedrunning.

The format is the following:

```.
8b little endian: length of input
8b data, set 01 / unset 00
  right
  left
  up
  down
  A
  B
  start
  select
```

### Playback

```sh
# using a file
tas-emulator playback filename

# using stdin (input must be b64 encoded, can be created with `base64 filename -w0`)
tas-emulator playback STDIN

# choose renderer
# when running in terminal mode, you will not be able to see the game in full detail. The server runs in terminal mode so you can connect via nc
tas-emulator playback filename -r (terminal|opengl)

# frame skipping in terminal renderer to reduce load on your terminal (skip 5 frames in this example, every 6th is shown)
# last frame will always be rendered, so you get your flag
tas-emulator playback filename -r terminal:5

# increase emulator speed for improved speedrunning experience, brought to you by hxp
tas-emulator -s 2 playback filename -r terminal:15
```

## About the game

The font used in the game can be found at https://de.fonts2u.com/modern-dos-8x8.schriftart
