import subprocess
from pathlib import Path

# resultディレクトリのパス
result_dir = Path('./result')

# サブフォルダ（＝対象データのある各フォルダ）を取得
target_folders = [f for f in result_dir.iterdir() if f.is_dir()]
print(target_folders)

# 実行
for folder in target_folders:
    print(f"Processing: {folder.name}")
    try:
        subprocess.run(['Rscript', 'xpht_analysis.R', str(folder)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] R script failed for folder: {folder.name}")
        print(f"Command: {e.cmd}")
        print(f"Exit code: {e.returncode}")
    except FileNotFoundError:
        print("Rscript not found. Make sure R is installed and Rscript is in your PATH.")
        break