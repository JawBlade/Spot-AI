import logging
import struct
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HEADER_SIZE = 44

def adjust_volume(input_file: str, output_file: str, factor: float):
    try:
        with open(input_file, "rb") as infile, open(output_file, "wb") as outfile:
            header = infile.read(HEADER_SIZE)
            outfile.write(header)
            while True:
                data = infile.read(2)
                if not data:
                    break
                sample = struct.unpack("<h", data)[0]
                temp = int(sample * factor)
                temp = max(min(temp, 32767), -32768)
                outfile.write(struct.pack("<h", temp))
        logger.info(f"Volume adjusted successfully: {output_file}")
    except FileNotFoundError:
        logger.error(f"Could not open file: {input_file}")
    except Exception as e:
        logger.error(f"Error processing file: {e}")

def load_on_spot():
    try:
        result = subprocess.run(
            [
                "python3", 
                "/home/jaw_blade/my_spot_env/spot-sdk/python/examples/spot_cam/command_line.py",
                "10.57.200.85",
                "audio", 
                "load", 
                "ai",
                "../AI_CTEC/ai_response.wav"
            ],
            check=True,
            capture_output=True,
            text=True
        )
        logger.info("Loaded WAV file onto Spot.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running Spot audio command: {e.stderr}")

def play_on_spot():
    try:
        result = subprocess.run(
            [
                "python3",
                "/home/jaw_blade/my_spot_env/spot-sdk/python/examples/spot_cam/command_line.py",
                "10.57.200.85",
                "audio",
                "play",
                "ai"
            ],
            check=True,
            capture_output=True,
            text=True
        )
        logger.info("Played WAV file on Spot.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running Spot audio command: {e.stderr}")

def delete_from_spot():
    try:
        result = subprocess.run(
            [
                "python3",
                "/home/jaw_blade/my_spot_env/spot-sdk/python/examples/spot_cam/command_line.py",
                "10.57.200.85",
                "audio",
                "delete",
                "ai"
            ],
            check=True,
            capture_output=True,
            text=True
        )
        logger.info("Deleted WAV file from Spot.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running Spot audio command: {e.stderr}")

def record():
    try:
        result = subprocess.run(
            [
                "python3",
                "/home/jaw_blade/my_spot_env/spot-sdk/python/examples/spot_cam/command_line.py",
                "10.57.200.85",
                "webrtc",
                "record",
                "audio",
                "--time",
                "10"
            ],
            check=True,
            capture_output=True,
            text=True
        )
        logger.info("Recorded audio from Spot.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running Spot audio command: {e.stderr}")