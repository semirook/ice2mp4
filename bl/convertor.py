# coding=utf-8
import subprocess, os
import MediaFile


FFMPEG_COMMAND_PATTERN = (
    'ffmpeg -loglevel quiet -i "{input_file}" -vcodec libx264 '
    '-b {video_bitrate} -s {screen_size} '
    '-acodec libfaac -ab 128k -ar 48000 -f mp4 '
    '-deinterlace -y -threads 4 "{output_file}"'
)

FFMPEG_COMMAND_DEFAULTS = {
    'video_bitrate': '700k',
    'screen_size': '480x368',
}


class MediaFileTransferI(MediaFile.FileTransfer):
    UPLOADS_FOLDER = 'uploads'

    def send(self, filename, offset, bytes, *args, **kwargs):
        filename = os.path.join(self.UPLOADS_FOLDER, filename)
        with open(filename, 'ab') as myfile:
            myfile.write(bytes)

    def isFileExists(self, filename, *args, **kwargs):
        filename = os.path.join(self.UPLOADS_FOLDER, filename)
        return os.path.exists(filename)

    def removeFile(self, filename, *args, **kwargs):
        filename = os.path.join(self.UPLOADS_FOLDER, filename)
        if os.path.exists(filename):
            os.remove(filename)

    def convertToMp4(self, filename, *args, **kwargs):
        input_file_name = os.path.join(self.UPLOADS_FOLDER, filename)
        output_file_name = '%s.mp4' % input_file_name
        params = FFMPEG_COMMAND_DEFAULTS.copy()
        ffmpeg_command = FFMPEG_COMMAND_PATTERN.format(
            input_file=input_file_name,
            output_file=output_file_name,
            video_bitrate=params['video_bitrate'],
            screen_size=params['screen_size'],
        )
        subprocess.call(ffmpeg_command, shell=True)

        return '%s.mp4' % filename
