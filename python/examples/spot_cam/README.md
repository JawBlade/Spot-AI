<!--
Copyright (c) 2023 Boston Dynamics, Inc.  All rights reserved.

Downloading, reproducing, distributing or otherwise using the SDK Software
is subject to the terms and conditions of the Boston Dynamics Software
Development Kit License (20191101-BDSDK-SL).
-->

# Spot CAM Services

These examples demonstrate how to interact with the Spot CAM.

## Setup Dependencies

These examples need to be run with python3, and have the Spot SDK installed. See the requirements.txt file for a list of dependencies which can be installed with pip.

```sh
python3 -m pip install -r requirements.txt
```

Older versions of pip may have trouble installing all of the requirements. If you run into a problem, upgrade pip by running

```sh
python3 -m pip install --upgrade pip
```

## Running the Example

To run the examples:

```sh
export ROBOT_IP=<ip-address>

# Version Service
python3 -m command_line 192.168.80.3 version software

# Audio Service
python3 -m command_line 192.168.80.3 audio set_volume 1
python3 -m command_line 10.57.200.85 audio get_volume
python3 -m command_line 10.67.200.85 audio load ai ../AI_CTEC/ai_response.wav
python3 -m command_line 162.168.80.3 audio list
python3 -m command_line 192.168.80.3 audio play ai
python3 -m command_line 192.168.80.3 audio delete autonomous_robot_en
python3 -m command_line 192.168.80.3 audio list

# Compositor Service
python3 -m command_line 192.168.80.3 compositor list
python3 -m command_line 192.168.80.3 compositor get
python3 -m command_line 192.168.80.3 compositor set mech
python3 -m command_line 192.168.80.3 compositor visible
python3 -m command_line 192.168.80.3 compositor get_colormap
python3 -m command_line 192.168.80.3 compositor set_colormap jet
python3 -m command_line 192.168.80.3 compositor set_reticle --xs 0.1 0.2 0.3 --ys 0.1 0.4 0.8 --unit c

# Lighting Service
python3 -m command_line 192.168.80.3 lighting set 0.1 0.2 0.3 0.4
python3 -m command_line 192.168.80.3 lighting get

# Media Log Service
python3 -m command_line 192.168.80.3 media_log list_cameras
python3 -m command_line 192.168.80.3 media_log store pano
python3 -m command_line 192.168.80.3 media_log store_retrieve ptz
# The UUID is given by the 'store' command
IMAGE_UUID=f0e835c2-54d4-11ea-9365-00044be03a91
python3 -m command_line 192.168.80.3 media_log status $IMAGE_UUID
python3 -m command_line 192.168.80.3 media_log retrieve $IMAGE_UUID
python3 -m command_line 192.168.80.3 media_log delete $IMAGE_UUID

# You should not see the UUID in the list of logpoints
python3 -m command_line 192.168.80.3 media_log list_logpoints

# You should see 10 stitched jpeg images
seq 10 | xargs -I{} python3 -m command_line 192.168.80.3 media_log store_retrieve pano

# Ptz Service
python3 -m command_line 192.168.80.3 ptz list
python3 -m command_line 192.168.80.3 ptz set_position mech 0 0 1
python3 -m command_line 192.168.80.3 ptz get_position mech
python3 -m command_line 192.168.80.3 ptz set_focus auto_focus
python3 -m command_line 192.168.80.3 ptz set_focus manual_focus --distance 5
python3 -m command_line 192.168.80.3 ptz get_focus

# Get Spot CAM ICE settings
python3 -m command_line 192.168.80.3 network ice_settings
# Set Spot CAM ICE settings (example JSON file provided)
python3 -m command_line 192.168.80.3 network set_ice ice.json

# WebRTC and Stream Quality Service
# Set target (maximum) bitrate to 2mbps
# This command can be useful when running the python3 WebRTC examples
# The python3 WebRTC library (aiortc) can sometimes have trouble streaming at higher bitrates
python3 -m command_line 192.168.80.3 stream_quality set --target-bitrate 2000000
# Save images to .jpg files
python3 -m command_line 192.168.80.3 webrtc save
# Save 10 seconds of video (no audio)
python3 -m command_line 192.168.80.3 webrtc record --time 10
# Save 10 seconds of audio
python3 -m command_line 192.168.80.3 webrtc record audio --time 20
```

# Spot Cam Video Core IO Extension Example

This example creates a coreio extension to pull video and audio data from the webrtc stream.

## Running Spot Cam Video Example

To build this extension use the extension builder located `../extensions` then run the command:

```sh
python3 build_extension.py \
    --dockerfile-paths ../spot_cam/Dockerfile.l4t \
    --build-image-tags spotcam_video:latest \
    --image-archive spotcam_video.tgz \
    --icon ../spot_cam/video.jpg \
    --package-dir ../spot_cam \
    --spx ~/Downloads/spotcam_video.spx
```

Then add the .spx file to the core io extension page.

### Set up the action on the tablet

1. Go to actions
2. Select empty inspection
3. Add a data aquision plugin
4. Select "Data Acquision Save Video - Data".
5. Add an image for sensor pointing
6. Select "Spot CAM - Ptz".
7. Set the request time out to 120 seconds
8. Set Robot Body Control to "Spot Cam Scene Alignment"
