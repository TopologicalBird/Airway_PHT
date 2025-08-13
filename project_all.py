import os
import nrrd as nrrd
import pydicom as dicom
import cv2
import numpy as np
import copy
import math
import nibabel as nib
import tqdm

# ベースディレクトリ
base_dir = os.getcwd()
input_folders = [f for f in os.listdir(base_dir) if os.path.isdir(f) and f != 'result']
result_dir = os.path.join(base_dir, 'result')

# (入力フォルダパス, 対応する_airway.niiファイルパス) のペアを作成
folder_pairs = []

for folder in input_folders:
    input_path = os.path.join(base_dir, folder)
    result_path = os.path.join(result_dir, folder)

    if os.path.isdir(result_path):
        # *_airway.nii のみ対象とする
        nii_files = [
            os.path.join(result_path, f)
            for f in os.listdir(result_path)
            if f.endswith('_airway.nii')
        ]

        # ファイルが存在する場合だけ追加
        if nii_files:
            folder_pairs.append((input_path, nii_files))

# 確認出力
for input_path, nii_list in tqdm.tqdm(folder_pairs, desc="Processing folders"):
    print(f"[入力] {input_path}")
    for nii in nii_list:
        print(f"   ↳ [結果] {nii}")


for input_path, nii_files in folder_pairs:
    # DICOMファイル読み込み（固定名で想定）
    dcm_file = os.path.join(input_path, '1-001.dcm')
    d = dicom.read_file(dcm_file)

    # NIfTIファイル読み込み（最初の1つのみ使用）
    nii_img = nib.load(nii_files[0])
    nii_array = np.where(nii_img.get_fdata() > 0, 1, 0).astype(np.uint8)

    # 転置してZ方向スライス順に変換
    airway = np.array([np.transpose(nii_array[:, :, i]) for i in range(nii_array.shape[2])])

    # 投影処理設定
    rotate_num = 30
    airway_spots = np.where(airway)
    airway_spots = list(airway_spots)
    airway_spots[1] = airway_spots[1] * d.PixelSpacing[0] / d.SliceThickness
    airway_spots[2] = airway_spots[2] * d.PixelSpacing[1] / d.SliceThickness

    proj_results = []
    margin = 3

    for rot_index in range(rotate_num):
        theta = np.pi * rot_index / rotate_num
        projected_spots = (
            np.round(airway_spots[0]),
            np.round(-airway_spots[1] * math.sin(theta) + airway_spots[2] * math.cos(theta))
        )

        axis1_range = (np.max(projected_spots[0]) - np.min(projected_spots[0]) + margin * 2).astype('uint16')
        axis2_range = (np.max(projected_spots[1]) - np.min(projected_spots[1]) + margin * 2).astype('uint16')

        proj_result_theta = np.zeros((axis1_range, axis2_range))
        projected_spots_shifted = [
            projected_spots[0] - np.min(projected_spots[0]) + margin,
            projected_spots[1] - np.min(projected_spots[1]) + margin
        ]
        projected_spots_shifted[0] = projected_spots_shifted[0].astype('uint16')
        projected_spots_shifted[1] = projected_spots_shifted[1].astype('uint16')
        proj_result_theta[projected_spots_shifted[0], projected_spots_shifted[1]] = 1
        proj_results.append(proj_result_theta)

    # 保存用の出力ディレクトリ（niiファイルと同じフォルダ＝result内）
    result_output_dir = os.path.dirname(nii_files[0])

    for i in range(rotate_num):
        output_filename = f'rot_{i}_{rotate_num}.png'
        output_path = os.path.join(result_output_dir, output_filename)
        cv2.imwrite(output_path, (proj_results[i] * 255).astype(np.uint8))