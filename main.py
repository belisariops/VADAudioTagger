import subprocess
import pysrt
from pathlib import Path
from pydub import AudioSegment


def get_audio_from_video():
    input_path_name = "Input"
    path_list = Path(input_path_name).iterdir()
    output_path_name = "Output/"
    output_format = ".mp3"
    for path_input in path_list:
        path_output = output_path_name + str(path_input)[(len(input_path_name) + 1):-4] + output_format
        subprocess.call(
            ['ffmpeg', '-i', path_input, '-q:a', '0', '-map', 'a', path_output])
    return 0


def slice_audio(full_file_name, format, window):
    file_name = full_file_name[7:-4]
    audio = AudioSegment.from_file(full_file_name, format)
    audio_duration = (len(audio) / (1000))  # In seconds
    subprocess.call(["mkdir", "Slices/" + file_name])
    subs_name = "{0}/{1}.srt".format("Subtitles", file_name)
    subs = pysrt.open(subs_name)
    subs_index = 0
    current_end = 0

    for slice_num in range(round(audio_duration / window)):
        talking = False
        current_end += window

        if subs[subs_index].start.seconds < current_end:
            talking = True

        sliced = audio[slice_num * (window * 1000): (slice_num + 1) * (window * 1000)]
        sliced.export("Slices/" + file_name + "/" + file_name + "_" + str(slice_num) + "." + format, format,
                      tags={'talking': talking})

        while subs[subs_index].end.seconds < current_end:
            if subs_index == len(subs) - 1:
                break
            subs_index += 1


def main():
    get_audio_from_video()
    path_list = Path("Output").iterdir()
    for audio_path in path_list:
        slice_audio(str(audio_path), "mp3", 5)

    return 0


if __name__ == "__main__":
    main()
