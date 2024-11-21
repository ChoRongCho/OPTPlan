# from scripts.pddl_planner import PDDLPlanner
import os.path
import random
import time

# from scripts.python_planner import PythonPlanner
from scripts.python_planner import PythonPlannerV2
from scripts.utils.utils import parse_args_v2, save2csv, save2csv_v2, initialize_csv_file
from example import DICT_LIST, GOALS, OBJS, PROPERTIES, OCPS


def probing_test():
    args = parse_args_v2()

    for i in range(1):
        args.exp_number = i + 1
        args.exp_name = 101
        planner = PythonPlannerV2(args=args)

        source = f"/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v3_probe/obj{i+1}"
        obj_name = OBJS[i]
        images = [
            [os.path.join(source, "base_side.jpg")],
            [os.path.join(source, "probe_side.jpg")],
            [os.path.join(source, "recover_side.jpg")]
        ]
        properties = planner.probing_property(obj_name, images)
        gt = PROPERTIES[i]
        if properties == gt:
            print(f"Object{i+1} has True predicates {properties}. ")
        else:
            print(f"Object{i + 1} has False predicates {properties} /// True: {gt}.  ")


def probing_exp():
    total_obj = 13
    total_iter = 10
    mode0_acc_list = []
    mode1_acc_list = []
    mode2_acc_list = []
    mode3_acc_list = []

    args = parse_args_v2()

    for obj_idx in range(2, 2 + total_obj):
        for mode in range(3, 4):
            obj_count = 0
            for iteration in range(total_iter):
                time.sleep(10)
                args.exp_number = obj_idx
                args.exp_name = 107 + mode + iteration*1000
                planner = PythonPlannerV2(args=args)
                obj_name = OBJS[obj_idx-1]
                if mode == 0:
                    source = f"/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v3_probe/obj{obj_idx}"
                    images = [os.path.join(source, "base_side.jpg")]

                elif mode == 1:
                    source = f"/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v3_probe/obj{obj_idx}"
                    images = [os.path.join(source, "base_side.jpg")]

                elif mode == 2:
                    source = f"/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v3_probe/obj{obj_idx}"
                    images = [
                        [os.path.join(source, "base_side.jpg")],
                        [os.path.join(source, "probe_side.jpg")],
                        [os.path.join(source, "recover_side.jpg")]
                    ]

                elif mode == 3:
                    source = f"/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v3_probe/obj{obj_idx}"
                    images = [
                        [os.path.join(source, "base_side.jpg")],
                        [os.path.join(source, "probe_side.jpg")],
                        [os.path.join(source, "recover_side.jpg")]
                    ]
                else:
                    raise ValueError

                properties = planner.property_probing_exp(obj_name=obj_name, images=images, mode=mode)
                gt = PROPERTIES[obj_idx-1]
                if properties == gt:
                    obj_count += 1
                    print(f"EXP: {args.exp_number}-{args.exp_name}, Object{obj_idx} has True predicates {properties}. ")
                else:
                    print(f"EXP: {args.exp_number}-{args.exp_name}, Object{obj_idx} has False predicates {properties}  /// True: {gt}.  ")

            if mode == 0:
                mode0_acc_list.append(obj_count / total_iter)
            elif mode == 1:
                mode1_acc_list.append(obj_count / total_iter)
            elif mode == 2:
                mode2_acc_list.append(obj_count / total_iter)
            elif mode == 3:
                mode3_acc_list.append(obj_count / total_iter)
    print("vanilla", mode0_acc_list)
    print("vanilla+CL", mode1_acc_list)
    print("vanilla inter", mode2_acc_list)
    print("Ours", mode3_acc_list)


def detect_objects_only():
    args = parse_args_v2()
    inst_num = 38
    total_iter = 10

    save_path = "/home/changmin/PycharmProjects/OPTPlan/result_detection"
    planner = PythonPlannerV2(args=args)
    planner.image_version = 3

    # start
    for iter_num in range(24140001, 24140001 + total_iter):
        planner.exp_number = str(iter_num)
        result_csv_path = os.path.join(save_path, f"exp{iter_num}_results.csv")
        initialize_csv_file(result_csv_path)

        for i in range(1, inst_num + 1):
            print(f"\nStart a detection instance: {i}")
            planner.exp_name = f"instance{i}"

            """set"""
            planner.initiating_dir()
            planner.result_dir = os.path.join(save_path, f"instance{i}")
            planner.image_version = 3

            object_dict = planner.only_detection()
            save2csv_v2(instance=i, object_dict=object_dict, filename=result_csv_path)
            time.sleep(0.4)


def main_v2():
    args = parse_args_v2()
    inst_num = 37
    total_iter = 1
    planner = PythonPlannerV2(args=args)
    # start
    for iter_num in range(24140001, 24140001 + total_iter):
        planner.exp_number = str(iter_num)
        for i in range(37, inst_num + 1):
            print(f"\nStart a number {i} experiment")
            planner.exp_name = f"instance{i}"
            planner.initiating_dir()
            planner.pseudo_plan(inst_num=i)


def plan_result():
    args = parse_args_v2()
    positive = 0
    negative = 0
    negative_list = []

    inst_num = 38
    total_iter = 10
    planner = PythonPlannerV2(args=args)

    for iter_num in range(24131001, 24131001 + total_iter):
        planner.exp_number = str(iter_num)
        for i in range(1, inst_num + 1):
            planner.exp_name = f"instance{i}"
            planner.initiating_dir()
            planning_output = planner.run()
            if "Cannot" in planning_output:
                negative += 1
                negative_list.append(f"exp{iter_num}:, instance:{i}")
            else:
                positive += 1
        print(f"Iter{iter_num}: Positive:{positive}, Negative: {negative}, Total: {positive + negative}")

    print(f"Positive Rate: {round(positive / (positive + negative) * 100, 4)}%")
    for ne_inst in negative_list:
        print(ne_inst)


def re_planning():
    args = parse_args_v2()
    planner = PythonPlannerV2(args=args)
    planner.feedback()


if __name__ == '__main__':
    detect_objects_only()
    # main_v2()
    # print("\n---Start validating---\n")
    # plan_result()
