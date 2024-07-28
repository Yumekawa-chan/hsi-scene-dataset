import cv2
import numpy as np
from parameter.color_matching_function import color_matching_function

def load_hsi(file_name):
    hsi = np.fromfile(file_name, np.uint16, -1).reshape(1080, 151, 2048)
    hsi = np.transpose(hsi, (0, 2, 1))
    return hsi

def hsi_to_rgb(hsi, color_matching_function, lower_limit_wavelength=390, upper_limit_wavelength=830, spectrum_stepsize=5, gamma=2.2):
    hsi = hsi.astype(np.float32)
    height, width, bands = hsi.shape
    hsi = hsi / 65535.0

    wave_length = np.arange(lower_limit_wavelength, upper_limit_wavelength + 1, spectrum_stepsize)
    cmf = color_matching_function()
    index_low = np.where(wave_length == cmf[0, 0])[0][0]
    index_high = np.where(wave_length == cmf[-1, 0])[0][0] + 1

    hsi_cie_range = hsi[:, :, index_low:index_high]

    img_xyz = np.zeros((height, width, 3))

    intensity = hsi_cie_range.reshape(-1, index_high - index_low)
    xyz = np.dot(intensity, cmf[:, 1:])

    img_xyz = xyz.reshape(height, width, 3)

    # XYZ値を正規化
    img_xyz = img_xyz / np.max(img_xyz)

    # XYZからRGBに変換
    img_rgb = np.zeros_like(img_xyz)
    img_rgb[:, :, 0] = 3.2406 * img_xyz[:, :, 0] - 1.5372 * img_xyz[:, :, 1] - 0.4986 * img_xyz[:, :, 2]
    img_rgb[:, :, 1] = -0.9689 * img_xyz[:, :, 0] + 1.8758 * img_xyz[:, :, 1] + 0.0415 * img_xyz[:, :, 2]
    img_rgb[:, :, 2] = 0.0557 * img_xyz[:, :, 0] - 0.2040 * img_xyz[:, :, 1] + 1.0570 * img_xyz[:, :, 2]

    # ガンマ補正を適用
    if gamma is not None:
        img_rgb = gamma_correction(img_rgb, gamma=gamma)

    # 値を [0, 1] の範囲にクリップ
    img_rgb = np.clip(img_rgb, 0, 1)
    # 8ビット整数に変換
    img_rgb = (img_rgb * 255).astype(np.uint8)

    return img_rgb

def gamma_correction(img, gamma=2.2):
    img = np.power(img, 1.0 / gamma)
    return img

def show_image(image):
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    hsi = load_hsi('outdoor_manual_image.nh9')
    rgb = hsi_to_rgb(hsi, color_matching_function)
    show_image(rgb)

if __name__ == '__main__':
    main()
