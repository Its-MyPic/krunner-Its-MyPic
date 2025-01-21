from dataclasses import dataclass, field, asdict
from json import load, dump
from pathlib import Path

version = hash("なんで春日影やったの！？")

@dataclass
class History:
    Version: int
    History: list[int]


@dataclass
class SubtitleInfo:
    text: str
    eposode: str
    frame_start: int
    usedcount: int = 0
    fileName: str = field(init=False)

    def __post_init__(self):
        self.fileName = f"{self.eposode}_{self.frame_start}.jpg"

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            text=data["text"].replace("妳", "你").lower(),
            eposode=data["episode"],
            frame_start=data["frame_start"],
        )

class Data:
    def __init__(self):
        self.pluginPath = Path(__file__).parent.as_posix()
        print(self.pluginPath)
        with open(f"{self.pluginPath}/data.json") as f:
            self.data:list[SubtitleInfo] = load(f, object_hook=lambda x: SubtitleInfo.from_dict(x))
        historyFile = Path(f"{self.pluginPath}/history.json")
        if historyFile.exists():
            with open(historyFile) as f:
                self.history:History = History(**load(f))
        else:
            self.history = History(Version=version, History=[0] * len(self.data))
        if self.history.Version != version:
            self.history = History(Version=version, History=[0] * len(self.data))
        for i, subtitle in enumerate(self.data):
            subtitle.usedcount = self.history.History[i]


    def save(self):
        with open(f"{self.pluginPath}/history.json", "w") as f:
            dump(asdict(self.history), f)

    def query(self, text:str) -> list[tuple]:
        text = text.replace("妳", "你").lower()
        filter(lambda x: text in x.text, self.data)
        for i, subtitle in enumerate(self.data):
            if subtitle.text == text:
                self.history.History[i] += 1
                return subtitle
        return []



if __name__ == "__main__":
    Data()