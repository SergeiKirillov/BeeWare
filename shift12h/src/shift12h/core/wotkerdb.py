import json
import toga
from pathlib import Path
from importlib.resources import files

class WorkerDB:
    def __init__(self,file_path):
        self.file_path=Path(file_path)
        self.workers=self._load()

    def _load(self):

        # #file = files("shift12h.data").joinpath("personal.json")
        # with self.file_path.open("r", encoding="utf-8") as file:
        #     data = json.load(file)
        # return data["workers"]

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            return data["workers"]

        except FileNotFoundError:
            print(f"Файл не найден: {self.file_path}")
            # toga.ErrorDialog(
            #        "Ошибка",
            #        f"Файл не найден: {self.file_path}"
            # )
            return None

        except json.JSONDecodeError as e:
            print(f"Ошибка JSON: {e}")
            return None

    def get_workers_by_brigade(self, brigade):
        int_brigade=int(brigade)

        if self.workers is not None:    
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

   