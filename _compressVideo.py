import os
import sys
import json
import ffmpeg
import asyncio

DEBUG_MODE = False

async def get_video_info(file_path):
    ffprobe_cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=bit_rate,width,height -print_format json "{file_path}"'
    process = await asyncio.create_subprocess_shell(
        ffprobe_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    output_json, _ = await process.communicate()
    output_str = output_json.decode('utf-8')
    stream_info = json.loads(output_str)

    if "streams" not in stream_info or len(stream_info["streams"]) == 0:
        print(f"No video stream found in file: {file_path}. This file will be skipped.")
        return None

    stream = stream_info["streams"][0]
    bitrate = round(int(stream["bit_rate"]) / (10 ** 6), 2)
    width = int(stream["width"])
    height = int(stream["height"])
    return bitrate, (width, height)

def find_video_files(path):
    video_extensions = (
        '.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv',
        '.m4v', '.mpg', '.mpeg', '.m2v', '.mxf', '.3gp', 
        '.ogg', '.ogv', '.webm', '.rm', '.rmvb', '.ts',
        '.m2ts', '.mts', '.yuv', '.divx', '.vob', '.svi', 
        '.mpe', '.asf', '.f4v', '.f4p', '.f4a', '.f4b'
    )

    video_files = [
        os.path.join(root, file)
        for root, _, files in os.walk(path)
        for file in files
        if file.endswith(video_extensions)
    ]
    
    if DEBUG_MODE:
        print("[DEBUG] Found video files: ", video_files)  # Debug Printout
    return video_files

def compress_video(input_file, crf, output_file):
    try:
        (
            ffmpeg
            .input(input_file)
            .output(output_file, vcodec='libx264', crf=crf)
            .run()
        )
        print("\nVideo compression completed.")
        
        if DEBUG_MODE:
            print(f"\n[DEBUG] Compression status for {input_file}: Success")  # Debug Printout
        return True
        
    except (ffmpeg.Error, Exception) as e:
        print(f"\nError compressing {input_file}: {str(e)}")
        
        if DEBUG_MODE:
            print(f"\n[DEBUG] Compression status for {input_file}: Failure")  # Debug Printout
        return False

def print_top_bitrates(video_info):
    max_file_length = max(len(file) for file in video_info.keys())

    print("\nTop 20 video files by bitrate:")
    sorted_info = sorted(video_info.items(), key=lambda x: x[1]["bitrate"], reverse=True)
    for i, (file, info) in enumerate(sorted_info[:20], 1):
        print(f"{i}. {file:<{max_file_length}} - {info['bitrate']} Mbit/s - {info['dimensions'][0]}x{info['dimensions'][1]}")

def get_user_selection(path, video_info):
    if len(video_info) == 1:
        selected_file = next(iter(video_info))
        print(f"Only one file found: {selected_file}.\nIt will be automatically selected for compression.")
    else:
        user_input = input("\nSelect a video file by number or enter the file name with extension if it's not in the list: ")

        if user_input.isdigit():
            index = int(user_input) - 1
            sorted_info = sorted(video_info.items(), key=lambda x: x[1]["bitrate"], reverse=True)
            if 0 <= index < len(sorted_info):
                selected_file = sorted_info[index][0]
            else:
                print("Invalid selection.")
                sys.exit()
        else:
            selected_file = os.path.join(path, user_input)
            if not os.path.isfile(selected_file):
                print("File not found.")
                sys.exit()

    if DEBUG_MODE:
        print(f"[DEBUG] Selected file: {selected_file}")  # Debug Printout
    return selected_file

def compress_selected_file(selected_file, video_info):
    file_root, file_ext = os.path.splitext(selected_file)
    output_file = f'{file_root}_compressed{file_ext}'

    bitrate = video_info[selected_file]['bitrate']
    resolution = video_info[selected_file]['dimensions']

    crf = determine_crf(bitrate, resolution)

    if compress_video(selected_file, crf, output_file):
        print(f"Video compressed successfully: {output_file}")
        post_compress_operations(selected_file, output_file)
    else:
        print("Video compression failed.")
        
def determine_crf(bitrate, resolution):
    width, height = resolution
    total_pixels = width * height

    if bitrate > 5 or total_pixels > 1920*1080:  # Full HD
        return 23
    elif bitrate > 2 or total_pixels > 1280*720:  # HD
        return 18
    else:
        return 15
        
def is_compression_worthwhile(bitrate, resolution):
    width, height = resolution
    total_pixels = width * height
    
    if total_pixels > 3840*2160:  # if the video is 4K
        return bitrate > 10
    else:
        return bitrate > 2 or total_pixels > 1280*720
        
def post_compress_operations(selected_file, output_file):
    #delete_original = input("\nWould you like to delete the original file? (y/n): ")
    delete_original = "y"
    if delete_original.lower() == 'y':
        original_filename = selected_file
        os.remove(selected_file)  # Delete the original file
        os.rename(output_file, original_filename)  # Rename the compressed file to original filename
        print(f"Original file deleted and compressed file renamed to {original_filename}")
    else:
        print(f"Original file kept. Compressed file is at {output_file}")


async def main():
    path = os.getcwd()
    video_files = find_video_files(path)

    if not video_files:
        print("No video files found.")
        sys.exit()

    video_infos = await asyncio.gather(*[get_video_info(file) for file in video_files])
    video_info = {
        file: {"bitrate": bitrate, "dimensions": dimensions} 
        for (file, info) in zip(video_files, video_infos)
        if info is not None and (bitrate := info[0]) and (dimensions := info[1]) and is_compression_worthwhile(*info)
    }


    if not video_info:
        print("No video files found that would benefit from compression.")
        sys.exit()

    print_top_bitrates(video_info)
    selected_file = get_user_selection(path, video_info)

    if DEBUG_MODE:
        print(f"Selected file: {selected_file}")

    compress_selected_file(selected_file, video_info)

    if DEBUG_MODE:
        print("End of program")

if __name__ == '__main__':
    asyncio.run(main())