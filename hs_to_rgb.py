import os
import glob
import datetime
import sys
import cv2
import numpy as np

# フォルダが存在しない場合、新規作成
def make_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

# ハイパースペクトルデータを読み込み、画像データを生成
def hyprawread(file_path, width, height, spectral_dim):
    with open(file_path, 'rb') as file:
        img_data = np.fromfile(file, np.uint16)
    img_data = np.reshape(img_data, (height, spectral_dim, width))
    img_data = np.transpose(img_data, (0, 2, 1))
    return img_data

# ハイパースペクトルデータからRGB画像を抽出
def extract_rgb(img_data):
    red_band = np.mean(img_data[:, :, 54:70], axis=2)
    green_band = np.mean(img_data[:, :, 30:40], axis=2)
    blue_band = np.mean(img_data[:, :, 20:30], axis=2)

    red_band = 255 * red_band / np.max(red_band)
    green_band = 255 * green_band / np.max(green_band)
    blue_band = 255 * blue_band / np.max(blue_band)

    rgb_image = np.dstack((red_band, green_band, blue_band)).astype(np.uint8)
    rgb_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    return rgb_image

# ガンマ補正を適用する関数
def apply_gamma_correction(image, gamma):
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(256)]).astype("uint8")
    return cv2.LUT(image, table)

# ハイパースペクトルデータから赤外線画像を抽出
def extract_infrared(img_data):
    infrared_band = np.mean(img_data[:, :, 71:], axis=2)
    infrared_band = 255 * infrared_band / np.max(infrared_band)
    infrared_stack = np.dstack((infrared_band, infrared_band, infrared_band)).astype(np.uint8)
    return infrared_band, infrared_stack

# ハイパースペクトルデータからRGBと赤外線を組み合わせた画像を生成
def create_rgb_nir_image(img_data):
    rgb_image = extract_rgb(img_data)
    infrared_band, _ = extract_infrared(img_data)
    rgb_nir_image = np.dstack((rgb_image, infrared_band)).astype(np.uint8)
    return rgb_nir_image

# ハイパースペクトル画像を処理し、指定されたディレクトリに保存
def process_hyperspectral_images(input_dir, output_dir, width, height, spectral_dim, gamma):
    files = glob.glob(os.path.join(input_dir, "*.nh9"))
    for file_path in files:
        img_data = hyprawread(file_path, width, height, spectral_dim)
        rgb_nir_image = create_rgb_nir_image(img_data)

        # ガンマ補正の適用
        corrected_image = apply_gamma_correction(rgb_nir_image, gamma)

        base_name = os.path.basename(file_path)
        output_name = f"rgb-{os.path.splitext(base_name)[0]}.jpg"
        output_path = os.path.join(output_dir, output_name)

        cv2.imwrite(output_path, corrected_image)
        print(f"Image saved: {output_path}")

# 指定されたフォルダー内のすべてのサブフォルダーを処理する関数
def process_hyperspectral_images_in_all_subdirs(parent_dir, output_dir, width, height, spectral_dim, gamma):
    # 親フォルダ内のすべてのサブフォルダをリスト化
    subdirs = [os.path.join(parent_dir, d) for d in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, d))]
    
    for subdir in subdirs:
        print(f"Processing folder: {subdir}")
        
        # サブフォルダごとの処理を行い、結果を指定された出力フォルダに保存
        process_hyperspectral_images(subdir, output_dir, width, height, spectral_dim, gamma)

if __name__ == "__main__":
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    if len(sys.argv) > 1:
        parent_directory = sys.argv[1]
    else:
        print("Please provide the parent directory path.")
        sys.exit()

    # カレントディレクトリに日付付きフォルダを作成
    output_directory = os.path.join(os.getcwd(), f"rgb-{current_date}")
    make_folder(output_directory)

    width, height, spectral_dim = 2048, 1080, 151
    gamma_value = 2.2

    # 指定された親フォルダ内のすべてのサブフォルダを処理
    process_hyperspectral_images_in_all_subdirs(parent_directory, output_directory, width, height, spectral_dim, gamma_value)
