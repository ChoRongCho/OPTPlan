import os.path
import time

from scripts.python_planner import PythonPlanner
from scripts.utils.utils import parse_args_v2, save2csv


def main():
    begin_time = time.time()
    args = parse_args_v2()
    max_time = 0
    min_time = 1000000000
    for j in range(24081610, 24081611):
        result_csv_path = os.path.join("/home/changmin/PycharmProjects/OPTPlan/result", f"exp{j}_results.csv")
        args.exp_number = j
        test_dict = {}
        for i in range(1, 37):  # 37
            print("-" * 50)
            print(f"Start a number {i} experiment")
            args.exp_name = i
            start_time = time.time()

            # planner = PythonPlanner(args=args)
            planner = PythonPlanner(args=args)

            time1 = time.time()
            # planner.plan()
            """-----------Detection Module-----------"""
            _, object_dict = planner.only_detection()
            test_dict[f"instance{i}"] = {}
            for k, data in object_dict.items():
                test_dict[f"instance{i}"][data['name']] = data['init_pose']
            """--------------------------------------"""
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
        save2csv(data=test_dict, filename=result_csv_path)

    #     print("\n")
    #     print("-"*99)
    #     print("\tTotal consumed time (s): ", round(end_time-begin_time, 4))
    #     print("\tAverage consumed time (s): ", round((end_time-begin_time)/36, 4))
    # print("Max Consumed Time: ", max_time)
    # print("Min Consumed Time: ", min_time)


def plan_result():
    args = parse_args_v2()
    positive = 0
    negative = 0
    for j in range(24080116, 24080117):
        args.exp_number = j
        for i in range(2, 3):
            args.exp_name = i
            planner = PythonPlanner(args=args)
            planning_output = planner.run()
            print(planning_output)
            print("-"*99)
            if "Error" in planning_output:
                negative += 1
            else:
                positive += 1
        print(f"Positive:{positive}, Negative: {negative}, Total: {positive+negative}")
        print(f"Positive Rate: {round(positive/(positive+negative)*100, 4)}")


def object_save():
    args = parse_args_v2()
    for i in range(1, 36):
        print(i)
        args.exp_name = i
        planner = PythonPlanner(args=args)
        planner.object_dict_save()


def re_planning():
    args = parse_args_v2()
    planner = PythonPlanner(args=args)
    planner.feedback()


def new_test():
    args = parse_args_v2()
    args.mkdb = True
    for i in range(9, 10):
        args.exp_name = i
        # args.mkdb = True
        start_time = time.time()

        # planner = PythonPlanner(args=args)
        planner = PythonPlanner(args=args)
        time1 = time.time()
        # planner.plan()


if __name__ == '__main__':
    main()
