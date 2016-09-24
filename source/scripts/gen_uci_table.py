import sys
import pexpect
sys.path.append('../../../efti/script')
from efti_intf import get_dsets_info
import csv

c_data_path = "../../../efti/src/datasets"

attr_cnt = dict(get_dsets_info(c_data_path, r"#define ATTR_CNT (\d*)"))
cls_cnt = dict(get_dsets_info(c_data_path, r"#define CATEG_MAX (\d*)"))
inst_cnt = dict(get_dsets_info(c_data_path, r"#define INST_CNT (\d*)"))

with open('uci.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(['Short Name', 'Dataset Name', 'No. of attributes', 'No. of instances', 'No. of classes'])
    for ds in sorted(attr_cnt):
        row = [ds, ds, attr_cnt[ds], inst_cnt[ds], cls_cnt[ds]]
        csvwriter.writerow(row)
