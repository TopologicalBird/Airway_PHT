import os
import subprocess
from tqdm import tqdm  # pip install tqdm

# 結果保存フォルダを作成
result_dir = 'result'
os.makedirs(result_dir, exist_ok=True)

# カレントディレクトリのサブフォルダ一覧を取得（resultを除外）
input_folders = [f for f in os.listdir('.') if os.path.isdir(f) and f != result_dir]
# もしすでに'source_r'や'.ipynb_checkpoints'があるなら
#input_folders = [f for f in os.listdir('.') if os.path.isdir(f) and f != result_dir and f != 'source_r' and f != '.ipynb_checkpoints']

# 検出されたフォルダ一覧を表示
print("検出された入力フォルダ:")
for folder in input_folders:
    print(f" - {folder}")

# 各フォルダに対してコマンドを実行（進捗バー付き）
print("\n変換を開始します...")
for folder in tqdm(input_folders, desc="処理中", unit="フォルダ"):
    input_path = os.path.abspath(folder)
    output_path = os.path.join(result_dir, folder)
    
    cmd = [
        'medpseg',
        '-i', input_path,
        '-o', output_path,
        '--post',
        '--disable_lobe'
    ]
    
    subprocess.run(cmd, check=True)
