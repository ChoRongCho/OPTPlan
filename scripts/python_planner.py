import os
import subprocess

from scripts.planner import PlannerFramework
from scripts.planner_v2 import PlannerFrameworkV2
from example import DICT_LIST, GOALS


class PythonPlanner(PlannerFramework):
    def __init__(self, args):
        super().__init__(args=args)
        self.args = args

    def plan_and_run(self):
        self.plan()
        self.run()

    def plan(self):
        self.make_plan()

    def pseudo_plan(self, inst_num: int):
        """
        test with random goal and constraints and without visual detection
        only for task planning

        :return: planning code
        """
        task_data = self.task_data
        task_data["goals"] = GOALS[inst_num - 1]
        self.make_plan_2(DICT_LIST[inst_num - 1])

    def run(self):
        file_path = os.path.join(self.result_dir, "planning.py")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"There is no file at {file_path}. ")
        process = subprocess.Popen(["python", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error:  # robot action re-definition
            planning_output = output.decode('utf-8') + "\n" + error.decode('utf-8')
        else:
            planning_output = output.decode('utf-8') + "\n"
        if self.is_save:
            file_path = os.path.join(self.result_dir, "planning_first_run_result.txt")
            with open(file_path, "w") as file:
                file.write(str(planning_output) + "\n\n")
                file.close()
        return planning_output

    def feedback(self):
        # for i in range(self.max_replanning):
        for i in range(self.max_replanning):
            print(f"Start Feedback ...{i}")
            is_feed = self.planning_feedback()
            if not is_feed:
                print("Re-Planning is done. ")
                break
        print("Maximum replanning number exceeded. ")


class PythonPlannerV2(PlannerFrameworkV2):
    def __init__(self, args):
        super().__init__(args=args)
        self.args = args

    def plan_and_run(self):
        self.plan()
        self.run()

    def plan(self):
        self.make_plan()

    def pseudo_plan(self, inst_num: int):
        """
        test with random goal and constraints and without visual detection
        only for task planning

        :return: planning code
        """
        task_data = self.task_data
        task_data["goals"] = GOALS[inst_num - 1]
        self.make_pseudo_plan(DICT_LIST[inst_num - 1])

    def run(self):
        file_path = os.path.join(self.result_dir, "planning.py")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"There is no file at {file_path}. ")
        process = subprocess.Popen(["python", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error:  # robot action re-definition
            planning_output = output.decode('utf-8') + "\n" + error.decode('utf-8')
        else:
            planning_output = output.decode('utf-8') + "\n"
        if self.is_save:
            file_path = os.path.join(self.result_dir, "planning_first_run_result.txt")
            with open(file_path, "w") as file:
                file.write(str(planning_output) + "\n\n")
                file.close()
        return planning_output

    def feedback(self):
        # for i in range(self.max_replanning):
        for i in range(self.max_replanning):
            print(f"Start Feedback ...{i}")
            is_feed = self.planning_feedback()
            if not is_feed:
                print("Re-Planning is done. ")
                break
        print("Maximum replanning number exceeded. ")
