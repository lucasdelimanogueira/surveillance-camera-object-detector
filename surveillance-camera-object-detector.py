import numpy as np
import cv2
import sys
import argparse

class CameraObjectDetector():
    def __init__(self, url, weights, config, labels, confidence_threshold):
        self.url = url
        self.weights = weights
        self.config = config
        self.confidence_threshold = confidence_threshold
        self.labels = labels
        self.configure()

    def configure(self):
        # config YOLO model
        with open(self.labels, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]

        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
        self.model = cv2.dnn.readNet(self.weights, self.config)
        self.layer_names = self.model.getLayerNames()
        self.output_layer = [self.layer_names[i[0]-1] for i in self.model.getUnconnectedOutLayers()]

        # config camera
        self.cap = cv2.VideoCapture(self.url)
    
    def start(self):
        while(True):
            # Capture frame-by-frame
            ret, img = self.cap.read()

            #img = cv2.resize(img, None, fx=self.size, fy=self.size)
            height, width, channels = img.shape

            # Detect objects
            blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

            self.model.setInput(blob)
            outs = self.model.forward(self.output_layer)

            # Show information on screen
            class_ids = []
            confidences = []
            boxes = []

            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]

                    if confidence > self.confidence_threshold: # Object detected
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        
                        # Retangles coordinates
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
            
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4) # Not show multiple boxes in the same object
            n_detected_objects = len(boxes)
            for i in range(n_detected_objects):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(self.classes[class_ids[i]])
                    color = self.colors[class_ids[i]]
                    cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
                    cv2.putText(img, label, (x, y - 30), cv2.FONT_HERSHEY_TRIPLEX, 1, color, 2)


            cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
            cv2.putText(img, "Press 'q' to exit", (30, 30), cv2.FONT_HERSHEY_TRIPLEX, 1, (255,255,255), 2)
            cv2.imshow("window", img)    

            # exit key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()

    ap.add_argument('-u', '--url', required=False, type=str,
                help = 'URL to connect to the camera', default = 'http://192.82.150.11:8083/mjpg/video.mjpg')

    ap.add_argument('-w', '--weights', required=False, type=str,
                help = 'path to YOLO weights file', default = './YOLO/yolov3.weights')    
    
    ap.add_argument('-c', '--config', required=False, type=str,
                help = 'path to YOLO config file', default = './YOLO/yolov3.cfg')
    
    ap.add_argument('-l', '--labels', required=False, type=str,
                help = 'path to classes labels files', default = './YOLO/coco.names')
    
    ap.add_argument('-t', '--threshold', required=False, type=float,
                help = 'Confidence threshhold', default = 0.5)
    
    
    args = ap.parse_args()

    detector = CameraObjectDetector(url=args.url, 
                weights=args.weights, 
                config=args.config, 
                labels=args.labels,
                confidence_threshold=args.threshold)

    detector.start()
        
