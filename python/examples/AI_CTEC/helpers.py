import struct
import subprocess

HEADER_SIZE = 44

def adjust_volume(input_file: str, output_file: str, factor: float):
    try:
        with open(input_file, "rb") as infile, open(output_file, "wb") as outfile:

            header = infile.read(HEADER_SIZE)
            outfile.write(header)

            while True:
                data = infile.read(2)  # 2 bytes per sample
                if not data:
                    break

                sample = struct.unpack("<h", data)[0]

                temp = int(sample * factor)
                if temp > 32767:
                    temp = 32767
                elif temp < -32768:
                    temp = -32768

                # Pack back into binary format and write
                outfile.write(struct.pack("<h", temp))

        print(f"Volume adjusted successfully: {output_file}")

    except FileNotFoundError:
        print(f"Could not open file: {input_file}")
    except Exception as e:
        print(f"Error processing file: {e}")

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
    except subprocess.CalledProcessError as e:
        print("Error running Spot audio command:", e.stderr)

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
    except subprocess.CalledProcessError as e:
        print("Error running Spot audio command:", e.stderr)

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
    except subprocess.CalledProcessError as e:
        print("Error running Spot audio command:", e.stderr)

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
    except subprocess.CalledProcessError as e:
        print("Error running Spot audio command:", e.stderr)
