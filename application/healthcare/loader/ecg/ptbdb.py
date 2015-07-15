from utils.csv_loader import CSVLoader
from numpy import genfromtxt

DATASET_ROOT = settings.BASE_DIR+"/media/healthcare/dataset/ecg/ptbdb"

size = 600
number = 7

# age: 81
# sex: female
# ECG date: 01/10/1990

# Diagnose:
# Reason for admission: Myocardial infarction
loader_pat1 = CSVLoader(DATASET_ROOT+"/patient001/s0010_re.csv")
data_pat1 = loader_pat1.extract_col(1, offset=2)
mid_points_pat1 = [640 + 730 * i for i in range(number)]
segments_pat1 = []
for p in mid_points_pat1:
    segments_pat1.append(data_pat1[p - size / 2 - 1:p + size / 2])

loader_pat2 = CSVLoader(DATASET_ROOT+"/patient002/s0015lre.csv")
data_pat2 = loader_pat2.extract_col(1, offset=2)
mid_points_pat2 = [690 + 720 * i for i in range(number)]
segments_pat2 = []
for p in mid_points_pat2:
    segments_pat2.append(data_pat2[p - size / 2 - 1:p + size / 2])

loader_pat3 = CSVLoader(DATASET_ROOT+"/patient003/s0017lre.csv")
data_pat3 = loader_pat3.extract_col(1, offset=2)
mid_points_pat3 = [1680 + 800 * i for i in range(number)]
segments_pat3 = []
for p in mid_points_pat3:
    segments_pat3.append(data_pat3[p - size / 2 - 1:p + size / 2])

loader_pat159 = CSVLoader(DATASET_ROOT+"/patient159/s0390lre.csv")
data_pat159 = loader_pat159.extract_col(1, offset=2)
mid_points_pat159 = [1200 + 700 * i for i in range(number)]
segments_pat159 = []
for p in mid_points_pat159:
    segments_pat159.append(data_pat159[p - size / 2 - 1:p + size / 2])

loader_pat171 = CSVLoader(DATASET_ROOT+"/patient171/s0364lre.csv")
data_pat171 = loader_pat171.extract_col(1, offset=2)
mid_points_pat171 = [450 + 700 * i for i in range(number)]
segments_pat171 = []
for p in mid_points_pat171:
    segments_pat171.append(data_pat171[p - size / 2 - 1:p + size / 2])

loader_pat175 = CSVLoader(DATASET_ROOT+"/patient175/s0009_re.csv")
data_pat175 = loader_pat175.extract_col(1, offset=2)
mid_points_pat175 = [1250 + 790 * i for i in range(number)] # 1300
segments_pat175 = []
for p in mid_points_pat175:
    segments_pat175.append(data_pat175[p - size / 2 - 1:p + size / 2])

loader_pat210 = CSVLoader(DATASET_ROOT+"/patient210/s0432_re.csv")
data_pat210 = loader_pat210.extract_col(1, offset=2)
mid_points_pat210 = [960 + 880 * i for i in range(number)]
segments_pat210 = []
for p in mid_points_pat210:
    segments_pat210.append(data_pat210[p - size / 2 - 1:p + size / 2])

loader_pat212 = CSVLoader(DATASET_ROOT+"/patient212/s0434_re.csv")
data_pat212 = loader_pat210.extract_col(1, offset=2)
mid_points_pat212 = [710 + 760 * i for i in range(number)]
segments_pat212 = []
for p in mid_points_pat212:
    segments_pat212.append(data_pat212[p - size / 2 - 1:p + size / 2])

loader_pat213 = CSVLoader(DATASET_ROOT+"/patient213/s0435_re.csv")
data_pat213 = loader_pat213.extract_col(1, offset=2)
mid_points_pat213 = [1080 + 700 * i for i in range(number)]
segments_pat213 = []
for p in mid_points_pat213:
    segments_pat213.append(data_pat213[p - size / 2 - 1:p + size / 2])

# plot(range(len(data_pat213)),data_pat213,alpha=0.8,color='blue',lw=3)
# show()


loader_pat244 = CSVLoader(DATASET_ROOT+"/patient244/s0473_re.csv")
data_pat244 = loader_pat244.extract_col(1, offset=2)
mid_points_pat244 = [1290 + 800 * i for i in range(number)]
segments_pat244 = []
for p in mid_points_pat244:
    segments_pat244.append(data_pat244[p - size / 2 - 1:p + size / 2])


loader_pat245 = CSVLoader(DATASET_ROOT+"/patient245/s0474_re.csv")
data_pat245 = loader_pat245.extract_col(1, offset=2)
mid_points_pat245 = [780 + 760 * i for i in range(number)]
segments_pat245 = []
for p in mid_points_pat245:
    segments_pat245.append(data_pat245[p - size / 2 - 1:p + size / 2])

loader_pat246 = CSVLoader(DATASET_ROOT+"/patient246/s0478_re.csv")
data_pat246 = loader_pat244.extract_col(1, offset=2)
mid_points_pat246 = [1290 + 800 * i for i in range(number)]
segments_pat246 = []
for p in mid_points_pat246:
    segments_pat246.append(data_pat246[p - size / 2 - 1:p + size / 2])

loader_pat247 = CSVLoader(DATASET_ROOT+"/patient247/s0479_re.csv")
data_pat247 = loader_pat247.extract_col(1, offset=2)
mid_points_pat247 = [580 + 670 * i for i in range(number)]
segments_pat247 = []
for p in mid_points_pat247:
    segments_pat247.append(data_pat247[p - size / 2 - 1:p + size / 2])

loader_pat248 = CSVLoader(DATASET_ROOT+"/patient248/s0481_re.csv")
data_pat248 = loader_pat248.extract_col(1, offset=2)
mid_points_pat248 = [1100 + 920 * i for i in range(number)]
segments_pat248 = []
for p in mid_points_pat248:
    segments_pat248.append(data_pat248[p - size / 2 - 1:p + size / 2])

