import json
import random


DICT_LIST = [
{'Objects_out_box': ['brown_3D_cylinder', 'white_3D_cylinder', 'yellow_3D_cylinder', 'green_1D_line'], 'Objects_in_box': [], 'Bin': []},
{'Objects_out_box': ['blue_3D_polyhedron', 'brown_3D_cylinder', 'yellow_3D_cylinder'], 'Objects_in_box': [], 'Bin': []},
{'Objects_out_box': ['blue_3D_polyhedron', 'white_2D_loop', 'transparent_3D_cuboid', 'black_1D_line'], 'Objects_in_box': [], 'Bin': []},
{'Objects_out_box': ['brown_3D_cylinder', 'green_1D_line', 'yellow_3D_cylinder', 'green_3D_cuboid'], 'Objects_in_box': [], 'Bin': []},
{'Objects_out_box': ['green_1D_line', 'black_3D_cylinder', 'green_3D_cuboid', 'white_3D_cylinder', 'yellow_3D_cylinder'], 'Objects_in_box': [], 'Bin': []},
{'Objects_out_box': ['blue_3D_polyhedron', 'red_3D_polyhedron', 'black_3D_cylinder', 'brown_3D_cylinder'], 'Objects_in_box': [], 'Bin': []},
{'Objects_out_box': ['black_1D_line', 'yellow_3D_cuboid', 'blue_2D_triangle', 'green_3D_cuboid', 'yellow_3D_cylinder'], 'Objects_in_box': [], 'Bin': []},
{'Objects_out_box': ['white_2D_circle', 'brown_3D_cuboid', 'yellow_3D_cylinder', 'green_1D_line'], 'Objects_in_box': [], 'Bin': []},
{'Objects_out_box': ['white_2D_loop', 'blue_3D_polyhedron', 'black_1D_line', 'white_2D_circle', 'green_1D_line'], 'Objects_in_box': [], 'Bin': []},
{'Objects_out_box': ['transparent_2D_circle', 'black_3D_cylinder', 'green_1D_line', 'brown_3D_cuboid', 'yellow_3D_cylinder'], 'Objects_in_box': [], 'Bin': []},
{'Objects_out_box': ['green_3D_cylinder', 'white_3D_cylinder', 'transparent_2D_circle', 'yellow_2D_rectangle'], 'Objects_in_box': [], 'Bin': []},
{'Objects_out_box': ['yellow_2D_rectangle', 'blue_2D_triangle', 'blue_3D_polyhedron'], 'Objects_in_box': [], 'Bin': []},
{'Objects_out_box': ['transparent_3D_cuboid', 'blue_2D_triangle', 'yellow_3D_cylinder', 'white_2D_circle'], 'Objects_in_box': [], 'Bin': []},
{'Objects_out_box': ['green_1D_line', 'black_3D_cylinder', 'yellow_3D_cylinder'], 'Objects_in_box': [], 'Bin': []},
{'Objects_out_box': ['brown_3D_cuboid', 'green_1D_line', 'blue_3D_polyhedron', 'black_1D_line'], 'Objects_in_box': [], 'Bin': []},
{'Objects_out_box': ['green_1D_line', 'yellow_3D_cylinder', 'white_2D_loop', 'brown_3D_cylinder', 'black_1D_line'], 'Objects_in_box': [], 'Bin': []},
{'Objects_out_box': ['beige_1D_line', 'white_2D_circle', 'red_3D_polyhedron'], 'Objects_in_box': [], 'Bin': []},
{'Objects_out_box': ['blue_2D_triangle', 'yellow_3D_cylinder', 'black_3D_cylinder'], 'Objects_in_box': [], 'Bin': []},
{'Objects_out_box': ['gray_1D_line', 'blue_2D_loop', 'white_2D_loop', 'yellow_2D_rectangle', 'black_1D_line'], 'Objects_in_box': [], 'Bin': []},
{'Objects_out_box': ['brown_3D_cuboid', 'brown_3D_cylinder', 'black_1D_line', 'green_1D_line'], 'Objects_in_box': [], 'Bin': []},
{'Objects_out_box': ['yellow_3D_cylinder', 'white_2D_circle', 'blue_3D_polyhedron', 'green_3D_cuboid'], 'Objects_in_box': [], 'Bin': []},
{'Objects_out_box': ['white_2D_circle', 'brown_3D_cylinder', 'red_3D_polyhedron', 'brown_3D_cuboid'], 'Objects_in_box': [], 'Bin': []},
{'Objects_out_box': ['yellow_2D_rectangle', 'green_3D_cuboid', 'green_1D_line', 'blue_2D_loop'], 'Objects_in_box': [], 'Bin': []},
{'Objects_out_box': ['red_3D_polyhedron', 'brown_3D_cylinder', 'blue_2D_triangle'], 'Objects_in_box': [], 'Bin': []},
{'Objects_out_box': ['black_1D_line', 'black_3D_cylinder', 'red_3D_polyhedron'], 'Objects_in_box': [], 'Bin': []},
{'Objects_out_box': ['black_1D_line', 'brown_3D_cylinder', 'white_2D_loop', 'blue_2D_triangle'], 'Objects_in_box': [], 'Bin': []},
{'Objects_out_box': ['black_3D_cylinder', 'brown_3D_cylinder', 'black_1D_line', 'yellow_3D_cuboid'], 'Objects_in_box': [], 'Bin': []},
{'Objects_out_box': ['green_3D_cylinder', 'black_3D_cylinder', 'yellow_3D_cylinder', 'transparent_2D_circle', 'blue_3D_polyhedron'], 'Objects_in_box': [], 'Bin': []},
{'Objects_out_box': ['red_3D_polyhedron', 'yellow_2D_rectangle', 'gray_1D_line', 'brown_3D_cylinder', 'white_2D_circle'], 'Objects_in_box': [], 'Bin': []},
{'Objects_out_box': ['green_1D_line', 'green_3D_cuboid', 'yellow_3D_cylinder'], 'Objects_in_box': [], 'Bin': []}
]


GOALS = [
    "Pack all the objects except the white ones.",
    "Pack all the objects.",
    "Pack all the objects except rigid ones.",
    "Pack all the objects.",
    "Pack all the objects except the 2D ones.",
    "Pack all the objects except the yellow ones.",
    "Pack all the objects except foldable ones.",
    "Pack all the objects.",
    "Pack all the objects except rigid ones.",
    "Pack all the objects except foldable ones.",
    "Pack all the objects.",
    "Pack all the objects.",
    "Pack all the objects except the white ones.",
    "Pack all the objects.",
    "Pack all the objects except the 2D ones.",
    "Pack all the objects.",
    "Pack all the objects except rigid ones.",
    "Pack all the objects except the 2D ones.",
    "Pack all the objects.",
    "Pack all the objects except rigid ones.",
    "Pack all the objects.",
    "Pack all the objects.",
    "Pack all the objects except the white ones.",
    "Pack all the objects except the white ones.",
    "Pack all the objects.",
    "Pack all the objects except the white ones.",
    "Pack all the objects.",
    "Pack all the objects.",
    "Pack all the objects except the 2D ones.",
    "Pack all the objects.",
]


def get_pseudo_json():
    data_dir = "/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/pseudo_database.json"
    with open(data_dir, 'r') as file:
        data = json.load(file)
        bin_packing_data = data["bin_packing"]
    return bin_packing_data


def get_random_names(data, min_count=3, max_count=5):
    index_map = {}
    for name, details in data.items():
        index = details['index']
        if index not in index_map:
            index_map[index] = []
        index_map[index].append(name)

    selected_indices = random.sample(range(1, 17), random.randint(min_count, max_count))

    selected_names = []
    for idx in selected_indices:
        if idx in index_map:
            # 해당 인덱스의 이름 중 랜덤하게 하나 선택
            selected_names.append(random.choice(index_map[idx]))

    return selected_names


def get_random_goal():
    goal_list = [
        "Pack all the objects.",
        "Pack all the objects.",
        "Pack all the objects.",
        "Pack all the objects.",
        "Pack all the objects.",
        "Pack all the objects.",
        "Pack all the objects.",
        "Pack all the objects except foldable ones.",
        "Pack all the objects except rigid ones.",
        "Pack all the objects except the white ones.",
        "Pack all the objects except the yellow ones.",
        "Pack all the objects except the 2D ones.",
    ]
    random_goal = random.choice(goal_list)
    print(random_goal)

def main():
    packing_data = get_pseudo_json()
    selected_names = get_random_names(packing_data)
    dict_index = {'Objects_out_box': selected_names, 'Objects_in_box': [], 'Bin': []}
    print(dict_index)


if __name__ == '__main__':
    for i in range(30):
        get_random_goal()
