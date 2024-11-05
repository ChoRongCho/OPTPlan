import cv2
import os
import numpy as np
import re


def main():
    # 이미지 폴더 경로

    # names = ["top_observation.png", "side_observation.png"]
    # for name in names:
    image_files = []
    for i in range(1, 15):
        image_folder = f"/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v3_objects"
        name = f"obj_top_{i}.png"
        image_files.append(os.path.join(image_folder, name))

    # 이미지 사이즈 설정
    img_width, img_height = 540, 360
    grid_height_size = 7
    grid_width_size = 2
    footnote_size = 60

    # 빈 캔버스 생성
    final_image = np.zeros((img_height * grid_width_size + footnote_size, img_width * grid_height_size, 3),
                           dtype=np.uint8)
    final_image.fill(255)

    for idx, file in enumerate(image_files):
        if idx >= grid_height_size * grid_width_size:
            break

        img = cv2.imread(file)
        img = cv2.resize(img, (img_width, img_height))

        row = idx // grid_height_size
        col = idx % grid_height_size

        y_offset = row * img_height + (footnote_size if row >= 1 else 0)
        final_image[y_offset:y_offset+img_height, col*img_width:(col+1)*img_width] = img

        # 0:60

    output_path = os.path.join("/home/changmin/PycharmProjects/OPTPlan/data/bin_packing", 'merged_objects_v3_1' + ".png")
    # output_path = os.path.join("/home/changmin/PycharmProjects/OPTPlan/data/bin_packing", 'merged_all_objects_v3.png')
    cv2.imwrite(output_path, final_image)

    print(f"Combined image saved at {output_path}")


if __name__ == '__main__':
    main()
