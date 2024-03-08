import json
import numpy as np


class Data:
    def __init__(self, file_path):
        self.file_path = file_path
        self.dimension = file_path.split("_")[-2]
        self.type = file_path.split(".")[-1]

    def read_file(self):
        with open(self.file_path, "r") as file:
            return file.read()

    def pop_frame(self):
        raise NotImplementedError

    def get_length(self):
        raise NotImplementedError


class Esoil_Data(Data):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.data = np.load(file_path).tolist()

    def pop_frame(self):
        raw_frame = self.data.pop(0)
        array = np.array(raw_frame)
        norm_frame = (array - array.min()) / (array.max() - array.min())
        norm_frame_reshaped = norm_frame.reshape(
            int(pow(array.size, 0.5)), int(pow(array.size, 0.5))
        )
        return norm_frame_reshaped

    def get_length(self):
        return len(self.data)


class Butlr32_Data(Data):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.raw_data = self.read_file()
        self.parser = Butlr32_Parser()
        data = self.parser.parse_raw(self.raw_data)
        self.data = data

    def pop_frame(self):
        raw_frame = self.data.pop(0)
        frame = self.parser.parse_frame(raw_frame)
        array = np.array(frame)
        return array

    def get_length(self):
        return len(self.data)


class Butlr32_Parser:
    def parse_raw(self, raw_data):
        if not raw_data:
            raise Exception
        filtered_data = [
            data for data in raw_data.replace(", b", "").split('"')[1:] if data
        ]
        return filtered_data

    def parse_frame(self, raw_frame):
        clean_frame = (
            raw_frame.replace(",)", "")[1:].replace("'", '"').replace("       ", "")
        )
        frame = json.loads(clean_frame.split("array(")[1].split("),")[0])
        return frame


if __name__ == "__main__":
    txt = Butlr32_Data("data\\standing_9_32x32_sensor.txt")
    print(txt.pop_frame())
