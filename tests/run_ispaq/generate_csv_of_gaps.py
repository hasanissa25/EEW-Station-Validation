# flake8:noqa
from obspy import read
import pandas as pd
columns = ["Network", "Station", "Channel",
           "Last Sample", "Next Sample", "Delta", "Samples"]

HNE = read('tests/data/apollo/archive/miniseed/2022/06/01/QW.BCV11..HNE.2022.152')
HNZ = read('tests/data/apollo/archive/miniseed/2022/06/01/QW.BCV11..HNZ.2022.152')
HNN = read('tests/data/apollo/archive/miniseed/2022/06/01/QW.BCV11..HNN.2022.152')

HNE_gaps = HNE.get_gaps()
HNZ_gaps = HNZ.get_gaps()
HNN_gaps = HNN.get_gaps()

HNE_dataframe = pd.DataFrame(data=HNE_gaps)
HNE_dataframe = HNE_dataframe.drop(columns=[2])
HNE_dataframe.columns = columns
HNE_dataframe.to_csv("HNE_Gaps.csv", index=False)

HNZ_dataframe = pd.DataFrame(data=HNZ_gaps)
HNZ_dataframe = HNZ_dataframe.drop(columns=[2])
HNZ_dataframe.columns = columns
HNZ_dataframe.to_csv("HNZ_Gaps.csv", index=False)


HNN_dataframe = pd.DataFrame(data=HNN_gaps)
HNN_dataframe = HNN_dataframe.drop(columns=[2])
HNN_dataframe.columns = columns
HNN_dataframe.to_csv("HNN_Gaps.csv", index=False)
