# MyAuth
Editor and Viewer

## Requirements
wxPython
python-vlc
pyyaml

## Python version
3.13.0

### Install the Viewer
- Clone this repository.
- Go to the Viewer folder.
- Open a Terminal.
- Type ```python -m venv env``` and press enter.
- Type ```env/Scripts/activate``` on Windows or ```env/bin/activate``` and press enter.
- Type ```pip install wxPython``` and press enter.
- Type ```pip install python-vlc``` and press enter.
- Type ```pip install PyYAML``` and press enter.
- Refer to the section below to work with the viewer

## Data to deal with it
### YAML Fields
```yaml
main_config:
  fore: white # Item contour
  back: black # Item back
  sel_fore: yellow # When selected 
  sel_back: grey # When selected
  i_play: play.png # 32x32 image for UI
  i_pause: pause.png # 32x32 image for UI
  i_stop: stop.png # 32x32 image for UI
  i_cursor: same # 32x32 image for UI, same if no custom cursor (not yet implemented)
  image: main.png # 1920x1080 back image

title_*: # The * must be replaced by a number
  image: 01.png # Chosen image for your media, must be just a name
  x: 100 # Image x location
  y: 800 # Image y location
  width: 300 # Image width
  height: 168 # Image height
  media: '01.mkv' # Media to launch, must be just a name
  title: 'Chapter One' # Text for this element (not yet implemented)
  title_X: center # X location for this text (not yet implemented)
  title_Y: bottom # Y location for this text (not yet implemented)
```

### Resources structure
```
resources
  images
    'any image files supported by python'
  videos
    'any video files with codecs supported by vlc'
  media.yml
```

## How the viewer works?
- Go to the Viewer folder.
- Open a terminal.
- Type the command ```env/Scripts/activate``` on Windows or ```env/bin/activate``` and press enter.
- Type the command ```python main.py``` and press enter.
- A frame appears in the screen, move the mouse and select a video with a left click.
- The video is launched.
- You can pause/play the video by clicking play/pause/stop buttons or press SPACE.
- You can quit the video by pressing ESCAPE.
- You can select again and again another item and cycle the process like you want.
