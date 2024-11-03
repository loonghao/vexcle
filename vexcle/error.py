# Import built-in modules
from typing import List


class VexcleError(Exception):
    """Base class for all Yuki exceptions."""
    pass


class FfmpegError(Exception):
    """Basic exception for errors raised by ffmpeg."""

    def __init__(self, msg: str, cmd: List[str], stdout: str, stderr: str):
        """Use last line as error message when given empty msg.

        Args:
            msg (str): Error message.
            cmd (List[str]): Command that was executed.
            stdout (str): stdout of ffmpeg.
            stderr (str): stderr of ffmpeg.

        """
        if not msg:
            msg = stderr.splitlines()[-1]
        super().__init__(msg)
        self.cmd = cmd
        self.stdout = stdout
        self.stderr = stderr
