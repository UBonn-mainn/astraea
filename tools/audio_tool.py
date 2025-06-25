from langchain.tools import Tool
import whisper

class AudioTranscriber:
    def __init__(self):
        self.model = whisper.load_model("base")

    def __call__(self, audio_path: str) -> str:
        result = self.model.transcribe(audio_path)
        return result["text"]

audio_tool = Tool(
    name="AudioTranscriber",
    func=AudioTranscriber(),
    description="Transcribes speech from an audio file path."
)
