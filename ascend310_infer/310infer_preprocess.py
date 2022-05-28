# Copyright 2022 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

import os
import sys
import numpy as np

class DatasetGenerator:
    def __init__(self, data_dir, drop=True):
        self.data = []
        self.label = []
        filelist = os.path.join(data_dir, "fea.lst")
        labellist = os.path.join(data_dir, "label.lst")
        with open(filelist, 'r') as fp:
            for fpath in fp:
                self.data.append(os.path.join(data_dir, fpath.strip()))
        with open(labellist, 'r') as fp:
            for label in fp:
                self.label.append(os.path.join(data_dir, label.strip()))
        if drop:
            self.data.pop()
            self.label.pop()
        print("dataset init ok, total len:", len(self.data))

    def __getitem__(self, index):
        npdata = np.load(self.data[index])
        nplabel = np.load(self.label[index]).tolist()
        return npdata, nplabel[0]

    def __len__(self):
        return len(self.data)

if __name__ == "__main__":
    data_path = sys.argv[1]
    output_path = "testdata/"
    dataset_eval = DatasetGenerator(data_path, False)
    steps_per_epoch_enroll = len(dataset_eval)
    print("size of eval data:", steps_per_epoch_enroll)

    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=False)

    for idx in range(steps_per_epoch_enroll):
        datacut = dataset_eval[idx][0][0, :301, :]
        savename = os.path.join(output_path, dataset_eval[idx][1].replace('/', '_') + '.bin')
        datacut.tofile(savename)
