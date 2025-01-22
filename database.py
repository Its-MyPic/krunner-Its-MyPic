from dataclasses import dataclass, field, asdict
from json import load, dump
from pathlib import Path
from requests import get
from concurrent import futures
from pprint import pprint
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
    
    def to_result(self, pluginPath:str):
        return (
            self.fileName,
            f"{self.text}",
            f"{pluginPath}/image/{self.eposode}_{self.frame_start}.jpg",
            100,
            self.usedcount,
            {},
        )

class Data:
    def __init__(self):
        self.pluginPath = Path(__file__).parent.as_posix()
        print(self.pluginPath)
        with open(f"{self.pluginPath}/data/data.json") as f:
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

    def query(self, text:str) -> list[SubtitleInfo]:
        if len(text):
            text = text.replace("妳", "你").lower()
            result = filter(lambda x: text in x.text, self.data)
        else:
            result = self.data
        result = sorted(result, key=lambda x: x.usedcount, reverse=True)
        result = result[:25]
        self.prepareImage(result)
        return result

    def prepareImage(self, subtitle:list[SubtitleInfo]):
        files = filter(lambda x: not Path(f"{self.pluginPath}/image/{x.fileName}").exists(), subtitle)
        with futures.ThreadPoolExecutor() as executor:
            executor.map(self.DownloadImage, files)

    def DownloadImage(self, subtitle:SubtitleInfo):
        print(subtitle.fileName)
        url = f"https://media.githubusercontent.com/media/jeffpeng3/MyPicDB/assets/images/{subtitle.fileName}"
        r = get(url)
        with open(f"{self.pluginPath}/image/{subtitle.fileName}", "wb") as f:
            f.write(r.content)



if __name__ == "__main__":
    pprint(Data().query("你"))