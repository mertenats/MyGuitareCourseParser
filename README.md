# MyGuitareCourseParser


## Installation

The utility `video-download`:

```
git clone https://github.com/mertenats/vimeo-download.git
cd video-download
sudo python3 install -r requirements.txt
sudo apt-get install ffmpeg
sudo apt-get install parallel
```

This script:

```
git clone https://github.com/mertenats/MyGuitareCourseParser.git
cd MyGuitareCourseParser
```

## Usage

Rename and edit `Constants_example.py` to `Constants.py`:

```
COURSE_NAME       	= ''

API_BASE_URL      	= ''
API_BEARER        	= ''

VIMEO_BASE_URL    	= 'https://player.vimeo.com/video/'

VIMEO_DOWNLOAD_PATH	= '.../vimeo-download/vimeo-download.py'

VIDEO_DOWNLOAD_DST	= '/home/samuel/Downloads/'
```

Launch the script:

```
python3 MyGuitareCourseParser.py
```

Start downloading the ressources:

```
parallel < links.txt
```