# surveillance-camera-object-detector
An object detector system for surveillance cameras using YOLO

# Configuration
First download the YOLO weights file from [here](https://pjreddie.com/media/files/yolov3.weights)

or in terminal:
`$ wget https://pjreddie.com/media/files/yolov3.weights`

If you have a slower machine you can download the YOLO tiny version using from [here](https://pjreddie.com/media/files/yolov3.weights)

or in terminal:
`$ wget https://pjreddie.com/media/files/yolov3-tiny.weights`

(if you use the tiny version you have to use the yolov3-tiny.cfg file as the --config argument of the script) 

# Example
`$ python surveillance-camera-object-detector.py --url 'http://192.82.150.11:8083/mjpg/video.mjpg' --weights ./YOLO/yolov3.weights --config ./YOLO/yolov3.cfg`<br/>
 ![](/examples/example1.png)
 
# Arguments

 | parameter | type    | description                                      |
 | --------- | ------- | ------------------------------------------------ |
 | `url`     | String  | URL to connect to the camera |
 | `weights`  | String | path to YOLO weights file |
 | `config` | String  | path to YOLO config file  |
 | `labels` | String  | path to classes labels files (coco.names) |
 | `threshold` | Float  | Confidence threshhold to detect an object |
 
# Tips
You can get public cameras URLs to test from [here](http://www.opentopia.com/)<br/><br/>
Example: `http://192.82.150.11:8083/mjpg/video.mjpg` is a public camera from canada<br/><br/>
You also can connect to your personal surveillance camera via RTSP protocol. In order to do that, you can check the RTSP url with the camera manufacturer or search on the internet.<br/><br/>
Some cameras models use the template `rtsp://username:password@ip`
