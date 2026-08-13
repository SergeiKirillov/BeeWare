import json
from pathlib import Path
from importlib.resources import files

class WorkerDB:
    def __init__(self):
        self.workers=self._load()

    def _load(self):
        file = files("shift12h.data").joinpath("personal.json")
        
        with file.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return data["workers"]

    def get_workers_by_brigade(self, brigade):
        int_brigade=int(brigade)

        return [
            worker
            for worker in self.workers
            if worker["brigade"]==int_brigade
        ]


        # print(type(int_brigade));
        # result = []
        # for worker in self.workers:
        #     if worker["brigade"] == int_brigade:
        #         result.append(worker)

   