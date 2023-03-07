# Emotion Detection 4 Stream 

This is source using Python to make many process for access camera and detection emotion from webcam 

## How to use

### GRPC

Firstly, we need start grpc service:

```sh
cd FaceService

python3 main.py 
```

### Start stream app 

```
cd Tracking App

python3 main
```

Note: Init the app, don't have any the camera. Using MQTT to send command start or stop