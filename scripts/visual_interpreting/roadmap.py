import os

import cv2
import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree
from scipy.spatial import distance

from scripts.visual_interpreting.visual_interpreter import FindObjects


def compute_weighted_distance(pt1, pt2, img_width, img_height):
    weight_parameter = 0.9
    y_weight = ((pt1[1] + pt2[1]) / 2) / img_height
    x_weight = abs((img_width / 2) - ((pt1[0] + pt2[0]) / 2)) / (img_width / 2)
    return 1 + weight_parameter * y_weight + (1 - weight_parameter) * x_weight


def connect_mst(detected_obj, anno_image, im_h, im_w, name):
    centers = []
    for idx, bbox in detected_obj.items():
        cx, cy, w, h = bbox['object']
        centers.append((cx, cy))
    centers = np.array(centers, dtype=np.int32)
    dist_matrix = distance.cdist(centers, centers, 'euclidean')
    if "side" in name:
        for i in range(len(centers)):
            for j in range(len(centers)):
                if i != j:
                    pt1 = (int(centers[i][0]), int(centers[i][1]))
                    pt2 = (int(centers[j][0]), int(centers[j][1]))
                    weighted_distance = dist_matrix[i][j] * compute_weighted_distance(pt1, pt2, im_w, im_h)
                    dist_matrix[i][j] = weighted_distance
    mst = minimum_spanning_tree(dist_matrix).toarray()
    for i in range(len(centers)):
        for j in range(len(centers)):
            if mst[i, j] != 0:
                cv2.line(anno_image, (centers[i, 0], centers[i, 1]),
                         (centers[j, 0], centers[j, 1]), (255, 255, 255), 2)  # 파란색 선 그리기


def connect_line(detected_obj, anno_image, im_h, im_w, name):
    centers = []
    for idx, bbox in detected_obj.items():
        cx, cy, w, h = bbox['object']
        centers.append((cx, cy))

    dist_matrix = distance.cdist(centers, centers, 'euclidean')
    if "side" in name:
        for i in range(len(centers)):
            for j in range(len(centers)):
                if i != j:
                    pt1 = (int(centers[i][0]), int(centers[i][1]))
                    pt2 = (int(centers[j][0]), int(centers[j][1]))
                    weighted_distance = dist_matrix[i][j] * compute_weighted_distance(pt1, pt2, im_w, im_h)
                    dist_matrix[i][j] = weighted_distance

    for i in range(len(centers)):
        nearest_indices = np.argsort(dist_matrix[i])[1:4]
        closest_distance = dist_matrix[i][nearest_indices[1]]
        farthest_distance = dist_matrix[i][nearest_indices[-1]]
        for j in nearest_indices:
            pt1 = (int(centers[i][0]), int(centers[i][1]))
            pt2 = (int(centers[j][0]), int(centers[j][1]))
            if dist_matrix[i][j] <= 1.8 * closest_distance:
                cv2.line(anno_image, pt1, pt2, (255, 255, 255), 2)


def main():
    names = ["top_observation.png", "side_observation.png"]

    for inst in range(1, 39):
        print(inst)
        for name in names:
            image_path = f"/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v3/instance{inst}/" + name
            result_dir = f"/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v3/instance{inst}/"
            text_query = ["object"]

            detect_obj = FindObjects()
            detect_obj.modifying_text_prompt(text_query)
            detected_obj, anno_image = detect_obj.get_bbox(image_path, result_dir)

            im_h, im_w, _ = anno_image.shape

            """ Connect line """
            # for only graph image
            origin_image = cv2.imread(image_path)
            connect_line(detected_obj, origin_image, im_h, im_w, name)
            # connect_mst(detected_obj, anno_image, im_h, im_w, name)

            cv2.imwrite(os.path.join(result_dir, f"connected_{name}"), origin_image)


def merge_data():
    dist_dir = "/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v3_see_all_in_one/"
    for i in range(1, 39):
        source = f'/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v3/instance{i}/'
        top_name = f"connected_top_observation.png"
        side_name = f"connected_side_observation.png"
        dist = f"connected_instance_{i}.png"

        top_image = cv2.imread(os.path.join(source, top_name))
        side_image = cv2.imread(os.path.join(source, side_name))
        merged = np.hstack((top_image, side_image))
        cv2.imwrite(os.path.join(dist_dir, dist), merged)


if __name__ == '__main__':
    main()
    merge_data()
    # main_v2()
