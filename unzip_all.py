import os
import gzip
import shutil
from glob import glob

# 対象ディレクトリ
result_dir = 'result'

# 各サブフォルダ内の *_airway.nii.gz を処理
for root, dirs, files in os.walk(result_dir):
    for gz_file in glob(os.path.join(root, '*_airway.nii.gz')):
        nii_file = gz_file[:-3]  # .nii.gz → .nii

        # すでに解凍済みならスキップ（オプション）
        if os.path.exists(nii_file):
            print(f"スキップ: {nii_file}（既に存在）")
            continue

        # 解凍処理
        with gzip.open(gz_file, 'rb') as f_in, open(nii_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        print(f"解凍完了: {nii_file}")
