#!/bin/bash

WIDTH=320
HEIGHT=240

gst-launch-0.10 dv1394src ! dvdemux ! queue ! dvdec \
 ! queue ! videoscale ! video/x-raw-yuv,width=$WIDTH,height=$HEIGHT \
 ! queue ! ffmpegcolorspace ! queue ! theoraenc quality=20 ! queue ! mux. \
 jackaudiosrc connect=0 ! queue ! audioconvert \
 ! queue ! vorbisenc quality=0.3 ! queue ! mux. \
 oggmux name=mux ! shout2send mount=/telecaster_live_video.ogg port=8000 password=source2parisson ip=127.0.0.1 

