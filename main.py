FONT_URL = 'https://fonts.gstatic.com/s/inter/v13/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuLyfAZ9hjQ.ttf'
import click
from moviepy.editor import *
import whisper
from cached_path import cached_path
from moviepy.video.tools.subtitles import SubtitlesClip
@click.command()
@click.argument("input")
@click.argument("output")
@click.option("--srt", default=None, help="File to save SRT to. Leave empty for no subtitles.")
@click.option('--model', type=click.Choice(['tiny', 'base', 'small', 'medium', 'large', 'large.v3'], case_sensitive=False), default='tiny')
# @click.option('--color', type=click.Choice(['tiny', 'base', 'small', 'medium', 'large', 'large.v3'], case_sensitive=False), default='tiny')
def subtitle(input, output, srt, model):
    print("Loading model...")
    mdl = whisper.load_model(model)
    print("Transcribing...")
    transcript = mdl.transcribe(
        word_timestamps=True,
        audio=input
    )
    print("Processing subtitles...")
    subs = []
    for segment in transcript['segments']:
        for word in segment['words']:
            subs.append(((word['start'], word['end'],), word['word'].strip(),))
    print("Loading video...")
    video = VideoFileClip(input)
    width, height = video.size
    print(width)
    generator = lambda txt: TextClip(txt, size=(width * (3 / 4) + 8, None), color='white', stroke_color='black', stroke_width=8, method='caption', fontsize=min(width / 7, height / 7), font=str(cached_path(FONT_URL)))
    generator1 = lambda txt: TextClip(txt, size=(width * (3 / 4), None), color='white', method='caption', fontsize=min(width / 7, height / 7), font=str(cached_path(FONT_URL)))
    print("Loading video clip...")
    subtitles = SubtitlesClip(subs, generator)
    subtitles2 = SubtitlesClip(subs, generator1)
    result_1 = CompositeVideoClip([video, subtitles.set_pos(('center','center'))])
    result = CompositeVideoClip([result_1, subtitles2.set_pos(('center','center'))])
    print("Writing video...")
    # result.write_videofile(output, codec='libx264', audio_codec='aac', threads=64)
    result.write_videofile(output, codec='h264_videotoolbox', audio_codec='aac', threads=64)

if __name__ == '__main__':
    subtitle()