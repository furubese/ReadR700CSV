from datetime import datetime
from matplotlib import pyplot as p

def DictData_to_matplotData(data, first_datetime):
    x = []
    y = []
    for d in data:
        x.append(timestamp_to_float(d.Timestamp, first_datetime))
        y.append(RSSI_to_float(d.RSSI))
    return [x, y]


def timestamp_to_datetime(timestamp):
    return datetime.strptime(timestamp[:-7], '%Y-%m-%dT%H:%M:%S.%f')


def timestamp_to_float(timestamp, first_datetime):
    return float((timestamp_to_datetime(timestamp) - first_datetime).total_seconds())


def RSSI_to_float(RSSI):
    return float(RSSI)


def get_first_data_AntenaData(Antena_Data):
    first_index = next(iter(Antena_Data.keys()))
    for key in Antena_Data:
        if not Antena_Data[key]:
            continue
        if timestamp_to_datetime(Antena_Data[first_index][0].Timestamp)\
                > timestamp_to_datetime(Antena_Data[key][0].Timestamp):
            first_index = key
    return first_index


class Render:
    def __init__(self, AntenaData, reverse=False, default_value=0):
        self.AntenaData = AntenaData
        self.firstData = timestamp_to_datetime(AntenaData[get_first_data_AntenaData(AntenaData)][0].Timestamp)
        self.enable_keys = []
        self.ADD_enable_keys()
        self.default_value = -default_value
        if reverse:
            self.set_default_value()


    def output(self, value):
        print(value)

    def set_default_value(self, defval=0):
        if defval:
            self.default_value = defval
        else:
            self.default_value = self.MINS()

    def MINS(self):
        ret_min_val = 0
        for key in self.enable_keys:
            xy = DictData_to_matplotData(self.AntenaData[key], self.firstData)
            min_y = min(xy[1]) * -1
            if ret_min_val < min_y:
                ret_min_val = min_y
        self.output("===default_value===")
        self.output(ret_min_val)
        self.output("===================")
        return ret_min_val

    def ADD_enable_keys(self):
        for key in self.AntenaData:
            if not self.AntenaData[key]:
                continue
            self.enable_keys.append(key)

    def Fill(self):
        for key in self.enable_keys:
            xy = DictData_to_matplotData(self.AntenaData[key], self.firstData)
            p.plot(xy[0], list(map(lambda y: y+self.default_value, xy[1])), linewidth=0)
            p.fill(xy[0], list(map(lambda y: y+self.default_value, xy[1])))

    def BarSize(self):
        max_size = 1
        for key in self.enable_keys:
            s = len(self.AntenaData[key])
            if max_size < s:
                max_size = s
        return max_size

    def Bar(self, size=None):
        if not size:
            sized = 0.3
            #sized = 5 / self.BarSize()
        else:
            sized = size
        BLOCK = sized
        key_num = len(self.enable_keys)
        position_number = 0
        for key in self.enable_keys:
            xy = DictData_to_matplotData(self.AntenaData[key], self.firstData)
            p.bar(xy[0], list(map(lambda y: y+self.default_value, xy[1])), align="edge", width=BLOCK)
            position_number += 1

    def Bar_Line(self, size=None):
        if not size:
            sized = 0.3
            # sized = 5 / self.BarSize()
        else:
            sized = size
        BLOCK = sized
        key_num = len(self.enable_keys)
        position_number = 0
        for key in self.enable_keys:
            xy = DictData_to_matplotData(self.AntenaData[key], self.firstData)
            p.bar(xy[0], list(map(lambda y: y+self.default_value, xy[1])), align="edge", width=position_number - key_num / 2 * BLOCK)
            p.plot(xy[0], list(map(lambda y: y+self.default_value, xy[1])), linewidth="1")
            position_number += 1

    def Line(self):
        for key in self.enable_keys:
            xy = DictData_to_matplotData(self.AntenaData[key], self.firstData)
            p.plot(xy[0], list(map(lambda y: y+self.default_value, xy[1])))

    def Scatter(self):
        for key in self.enable_keys:
            xy = DictData_to_matplotData(self.AntenaData[key], self.firstData)
            p.scatter(xy[0], list(map(lambda y: y+self.default_value, xy[1])))

    def One_Bar(self, key, size=0.3):
        BLOCK = size
        xy = DictData_to_matplotData(self.AntenaData[key], self.firstData)
        p.bar(xy[0], list(map(lambda y: y+self.default_value, xy[1])), align="edge", width=BLOCK)

    def One_Line(self, key):
        xy = DictData_to_matplotData(self.AntenaData[key], self.firstData)
        p.plot(xy[0], list(map(lambda y: y + self.default_value, xy[1])))

    def figure(self, str):
        p.figure(str)

    def show(self):
        p.show()