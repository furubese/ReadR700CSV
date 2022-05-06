from multiprocessing import Process
from matplot_Render import rend as rnd

class Data:
    def __init__(self):
        self.Timestamp = ""
        self.EPC = ""
        self.TID = ""
        self.Antenna = ""
        self.RSSI = ""
        self.Frequency = ""
        self.Hostname = ""
        self.PhaseAngle = ""
        self.DopplerFrequency = ""


def file_to_data(path):
    ret_Data = []
    with open(path) as f:
        file_str_list = f.readlines()[3:]
        for line in file_str_list:
            line_split = line.split(",")
            data = Data()
            data.Timestamp = line_split[0]
            data.EPC = line_split[1]
            data.TID = line_split[2]
            data.Antenna = line_split[3]
            data.RSSI = line_split[4]
            data.Frequency = line_split[5]
            data.Hostname = line_split[6]
            data.PhaseAngle = line_split[7]
            data.DopplerFrequency = line_split[8]
            ret_Data.append(data)
    return ret_Data


def other_antena_append0(antena_id, antena_list, Timestamp, base):
    for key in antena_list:
        if antena_id == key and antena_list[key][0] == []:
            continue
        d = Data()
        d.RSSI = base
        d.Antenna = antena_id
        d.Timestamp = Timestamp
        antena_list[key].append(d)


def MINS(global_data):
    ret_min = float(global_data[0].RSSI)
    for sdata in global_data:
        rssi = float(sdata.RSSI)
        if ret_min > rssi:
            ret_min = rssi
    return ret_min


def CREATE_TagId_DICT(global_data):
    TagIdDict = {}
    for sdata in global_data:
        if sdata.EPC not in list(TagIdDict.keys()):
            insert_dict = {sdata.EPC : []}
            TagIdDict.update(insert_dict)
    return TagIdDict


def gen_data_antena(global_data, antena_list, base=None, data_0=False):
    if base is None:
        based = MINS(global_data)
    else:
        based = base

    for sdata in global_data:
        for antena_id in antena_list:
            if antena_id == sdata.Antenna:
                antena_list[antena_id].append(sdata)
                if data_0:
                    other_antena_append0(antena_id, antena_list, sdata.Timestamp, based)
                break

def gen_data_tagid(global_data, taglist, base=None):
    for sdata in global_data:
        for tag_id in taglist:
            if tag_id == sdata.EPC:
                taglist[tag_id].append(sdata)
                break


"""～～～サンプル関数～～～"""
def Line(AntenaData, base_line, BarSize):
    # 単純折れ線グラフ
    Render = rnd.Render(AntenaData, default_value=base_line)
    Render.figure("Line")
    Render.Line()
    Render.show()
def BadBar(AntenaData, base_line, BarSize):
    # ベースラインを設定しない棒グラフ
    Render = rnd.Render(AntenaData, default_value=0)
    Render.figure("BadBar")
    Render.Bar()
    Render.show()
def Bar(AntenaData, base_line, BarSize):
    # 棒グラフ
    Render = rnd.Render(AntenaData, default_value=base_line)
    Render.figure("Bar")
    Render.Bar(size=BarSize)
    Render.show()
def BarLine(AntenaData, base_line, BarSize):
    # 折れ線と棒グラフどっちも
    Render = rnd.Render(AntenaData, default_value=base_line)
    Render.figure("BarLine")
    Render.Line()
    Render.Bar(size=BarSize)
    Render.show()
def BarAndLine(AntenaData, base_line, BarSize):
    # 奇数：折れ線、偶数：棒グラフ
    Render = rnd.Render(AntenaData, default_value=base_line)
    Render.figure("BarAndLine")
    Render.One_Bar("1", size=-0.05)
    Render.One_Line("2")
    Render.One_Bar("3", size=0.05)
    Render.One_Line("4")
    Render.show()
def Bar1AndBar4(AntenaData, base_line, BarSize):
    # 1と4のみ棒グラフ 他は描写しない。
    Render = rnd.Render(AntenaData, default_value=base_line)
    Render.figure("Bar1AndBar4")
    Render.One_Bar("1", size=-0.05)
    Render.One_Bar("4", size=0.05)
    Render.show()
"""～～～～～～～～～～～～"""

if __name__ == '__main__':
    path        =   "./data.csv"            # データファイルパス
    global_data =   file_to_data(path)      # 読み込み
    data_0      =   False                   # データを0へ
    base_line   =   MINS(global_data)       # ベースラインの設定
    BarSize     =   0.05                    # 棒グラフ横のサイズ

    AntenaData = {  #アンテナID
        "1": [],
        "2": [],
        "3": [],
        "4": [],
    }

    Tag_ID_Data = CREATE_TagId_DICT(global_data)    #TagID

    # gen_data_antena(global_data, AntenaData, base=base_line, data_0=data_0)
    gen_data_tagid(global_data, Tag_ID_Data, base=base_line)

    PlotData = Tag_ID_Data

    for pd in PlotData:
        print("~~~~~~~{}~~~~~~~~~~~~~~~~".format(pd))
        cnt = 0
        for p in PlotData[pd]:
            cnt += 1
        print("COUNT:{}".format(cnt))
    # 折れ線グラフを表示する
    Render = rnd.Render(PlotData, default_value=base_line)
    Render.Line()
    Render.show()

    # サンプルを一つ表示する
    # Bar1AndBar4(AntenaData, base_line, BarSize)

    # サンプルを全て表示する
    """
    method_l = [
        Line,
        Bar,
        BarLine,
        BarAndLine,
    ]
    prosseses = []
    for m in method_l:
        prs = Process(target=m, args=(PlotData, base_line, BarSize,))

        prs.start()
        prosseses.append(prs)

    for prs in prosseses:
        prs.join()
    """