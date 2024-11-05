# from scripts.pddl_planner import PDDLPlanner
import os.path
import random
import time

from scripts.python_planner import PythonPlanner
from scripts.utils.utils import parse_args_v2, save2csv, save2csv_v2, initialize_csv_file
from example import DICT_LIST, GOALS, OBJS, PROPERTIES, OCPS


def probing_test():
    args = parse_args_v2()

    for i in range(1):
        args.exp_number = i + 1
        args.exp_name = 101
        planner = PythonPlanner(args=args)

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
                planner = PythonPlanner(args=args)
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

    test_num = 38
    test_start = 24102800
    while True:
        print(f"Start a {test_start}")
        for exp_num in range(test_start+1, test_start+4):  # 3
            args.image_version = exp_num - test_start
            print(f"    Try {args.image_version}")

            result_csv_path = os.path.join(f"/home/changmin/PycharmProjects/OPTPlan/result", f"exp{exp_num}_results.csv")

            initialize_csv_file(result_csv_path)
            args.exp_number = exp_num
            for i in range(1, test_num + 1):
                # print(f"Start a number {i} experiment")
                args.exp_name = i
                planner = PythonPlanner(args=args)

                # """-----------Detection Module-----------"""
                object_dict = planner.only_detection_2()
                save2csv_v2(instance=i, object_dict=object_dict, filename=result_csv_path)
                time.sleep(3)
                """--------------------------------------"""
            time.sleep(10)
        test_start += 100
        if test_start == 24102800 + 400:
            break


def main_v2():
    begin_time = time.time()
    args = parse_args_v2()
    max_time = 0
    min_time = 1000000000

    inst_num = 38
    total_iter = 10
    planner = PythonPlanner(args=args)
    # start
    for iter_num in range(24110001, 24110001 + total_iter):
        planner.exp_number = str(iter_num)
        for i in range(1, inst_num + 1):
            print(f"\nStart a number {i} experiment")
            planner.exp_name = f"instance{i}"
            start_time = time.time()
            planner.initiating_dir()
            time1 = time.time()

            planner.pseudo_plan(inst_num=i, obj_python_class=OCPS)
            time2 = time.time()
            table_path = os.path.join(planner.result_dir, "table.txt")
            with open(table_path, 'a') as file:
                file.write("\n\n")
                file.write(f"\t\tInitialize time:  {round(time1 - start_time, 4)}\n")
                file.write(f"\t\tPlanning time:  {round(time2 - time1, 4)}\n")
                file.write(f"\t\tTotal time:  {round(time2 - start_time, 4)}\n")
                file.close()

            if time2 - time1 > max_time:
                max_time = round(time2 - time1, 4)
            if time2 - time1 < min_time:
                min_time = round(time2 - time1, 4)

        end_time = time.time()
        time.sleep(10)

        if iter_num == 24110001:
            print("\n")
            print("-" * 99)
            print("\tTotal consumed time (s): ", round(end_time - begin_time, 4))
            print("\tAverage consumed time (s): ", round((end_time - begin_time) / inst_num, 4))
    print("Max Consumed Time: ", max_time)
    print("Min Consumed Time: ", min_time)


# def main():
#     begin_time = time.time()
#     args = parse_args_v2()
#     max_time = 0
#     min_time = 1000000000
#     test_num = 2
#     for j in range(24110100, 24110100):
#         result_csv_path = os.path.join("/home/changmin/PycharmProjects/OPTPlan/result", f"exp{j}_results.csv")
#         args.exp_number = j
#         test_dict = {}
#         for i in range(1, test_num + 1):  # 40
#             print("-" * 50)
#             print(f"Start a number {i} experiment")
#             args.exp_name = i
#             start_time = time.time()
#
#             # planner = PythonPlanner(args=args)
#             planner = PythonPlanner(args=args)
#             time1 = time.time()
#             planner.plan()
#             time2 = time.time()
#
#             table_path = os.path.join(planner.result_dir, "table.txt")
#             with open(table_path, 'a') as file:
#                 file.write("\n\n")
#                 file.write(f"\t\tInitialize time:  {round(time1 - start_time, 4)}\n")
#                 file.write(f"\t\tPlanning time:  {round(time2 - time1, 4)}\n")
#                 file.write(f"\t\tTotal time:  {round(time2 - start_time, 4)}\n")
#                 file.close()
#
#             if time2 - time1 > max_time:
#                 max_time = round(time2 - time1, 4)
#             if time2 - time1 < min_time:
#                 min_time = round(time2 - time1, 4)
#
#         end_time = time.time()
#         time.sleep(10)
#         print("\n")
#         print("-" * 99)
#         print("\tTotal consumed time (s): ", round(end_time - begin_time, 4))
#         print("\tAverage consumed time (s): ", round((end_time - begin_time) / test_num, 4))
#     print("Max Consumed Time: ", max_time)
#     print("Min Consumed Time: ", min_time)


def plan_result():
    args = parse_args_v2()
    positive = 0
    negative = 0
    negative_list = []

    inst_num = 38
    total_iter = 10
    planner = PythonPlanner(args=args)

    for iter_num in range(24110001, 24110001 + total_iter):
        planner.exp_number = str(iter_num)
        for i in range(1, inst_num + 1):
            # print(f"EXP {i}")
            planner.exp_name = f"instance{i}"
            planner.initiating_dir()
            planning_output = planner.run()
            if "Cannot" in planning_output:
                negative += 1
                negative_list.append(f"exp{iter_num}:, instance:{i}")
            else:
                positive += 1
        print(f"Iter{iter_num}: Positive:{positive}, Negative: {negative}, Total: {positive + negative}")

    print(f"Positive Rate: {round(positive / (positive + negative) * 100, 4)}")
    for ne_inst in negative_list:
        print(ne_inst)


def re_planning():
    args = parse_args_v2()
    planner = PythonPlanner(args=args)
    planner.feedback()


if __name__ == '__main__':
    main_v2()
    # plan_result()
