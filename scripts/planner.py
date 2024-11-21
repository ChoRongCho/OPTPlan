import json
import os
import re
import subprocess
import time
from datetime import datetime

from openai import OpenAI
from tabulate import tabulate

from scripts.llm_interface.gpt_interface import GPTInterpreter
from scripts.robot.robot_predicates_prove import RobotProve
from scripts.utils.prompt_set import PromptSet
from scripts.utils.utils import object_parsing, list_file, sort_files, dict_parsing, parse_single_name
from scripts.visual_interpreting.visual_interpreter import FindObjects
from scripts.visual_interpreting.zero_shot_cl import ZeroClassifier


class PlannerFramework:
    def __init__(self, args):

        # task and experiment setting
        self.task = args.task_name  # bin_packing
        self.exp_name = f"instance{args.exp_name}"

        if args.exp_number:
            self.exp_number = str(args.exp_number)
        else:
            self.exp_number = str(0)

        self.is_save = args.is_save
        self.max_predicates = args.max_predicates
        self.patience_repeat = 1
        self.max_replanning = args.max_feedback
        self.planning_repeat = 0
        self.random_mode = args.is_random

        self.im_v = [
            ["side_observation.png", "top_observation.png"],
            ["naive_annotated_side_observation.png", "naive_annotated_top_observation.png"],
            ["annotated_side_observation.png", "annotated_top_observation.png"]
        ]
        self.image_version = args.image_version

        # basic path
        self.args = args
        self.json_dir = args.json_dir
        self.data_dir = args.data_dir
        self.result_dir = os.path.join(args.result_dir, self.exp_name, "result" + self.exp_number)

        # domain path
        self.im_side = os.path.join(self.data_dir, self.task, "planning_v3", self.exp_name, f"side_observation.png")
        self.im_top = os.path.join(self.data_dir, self.task, "planning_v3", self.exp_name, f"top_observation.png")
        self.image_side = os.path.join(self.data_dir, self.task, "planning_v3", self.exp_name,
                                       self.im_v[self.image_version - 1][0])
        self.image_top = os.path.join(self.data_dir, self.task, "planning_v3", self.exp_name,
                                      self.im_v[self.image_version - 1][1])
        self.task_json = os.path.join(self.data_dir, self.task, "planning_v3", self.exp_name, "task_instruction.json")

        self.domain_image = [self.image_top, self.image_side]
        self.original_domain_image = [self.im_top, self.im_side]

        # json_dir
        self.api_json = os.path.join(self.json_dir, args.api_json)
        # self.example_json = os.path.join(self.json_dir, args.example_prompt_json)
        self.example_json = False
        self.robot_json = os.path.join(self.json_dir, args.robot_json)
        self.def_json = os.path.join(self.json_dir, "definitions.json")
        # self.task_json = os.path.join(self.json_dir, "task_instruction.json")

        # additional path
        self.database_path = os.path.join(self.data_dir, self.task)
        self.object_list = []
        self.db = {}

        # read json data
        self.robot_data = self.get_json_data(self.robot_json)
        self.task_data = self.get_json_data(self.task_json)
        self.definition = self.get_json_data(self.def_json)

        self.api_key, self.setting = self.get_api_key()

        # Initialize Class for planning
        self.answer = []
        self.question = []
        self.table = []
        self.anno_image = []

        # GPT setting
        self.client = OpenAI(api_key=self.api_key)
        self.gpt_interface_vision = GPTInterpreter(api_key=self.api_key,
                                                   setting=self.setting,
                                                   version="vision")
        self.gpt_interface_text = GPTInterpreter(api_key=self.api_key,
                                                 setting=self.setting,
                                                 version="text")
        self.grounding_dino = FindObjects(is_save=self.is_save)

        self.load_prompt = PromptSet(task=self.task, constraints=self.task_data["rules"],
                                     definition=self.definition,
                                     primitives=self.robot_data["actions"])
        self.robot = RobotProve(name=self.robot_data["name"],
                                goal=self.robot_data["goal"],
                                actions=self.robot_data["actions"],
                                gpt_interface=self.gpt_interface_vision)

        # Visual Interpreter
        self.classifier = ZeroClassifier()

        # init state, goal state, def_table
        self.state = {}
        self.print_args()
        self.object_dict = {}

        if self.args.mkdb:
            # make Database using object image
            for obj_num in range(1, 8):
                self.initialize_database(obj_num)
            if args.is_save:
                self.save_db()

        else:
            # use exist database
            self.database = self.get_json_data(os.path.join(self.database_path, "all_database.json"))

    def print_args(self):
        self.table = [["Project Time", datetime.now()],
                      ["Task", self.task],
                      ["Exp_Name", self.exp_name],
                      ["API JSON", self.args.api_json],
                      ["Max Predicates", self.args.max_predicates]]
        # print(tabulate(self.table))
        self.robot.print_definition_of_predicates()

    def initiating_dir(self):
        self.result_dir = os.path.join(self.args.result_dir, self.exp_name, "result" + self.exp_number)

        # domain path
        self.im_side = os.path.join(self.data_dir, self.task, "planning_v3", self.exp_name, f"side_observation.png")
        self.im_top = os.path.join(self.data_dir, self.task, "planning_v3", self.exp_name, f"top_observation.png")
        self.image_side = os.path.join(self.data_dir, self.task, "planning_v3", self.exp_name,
                                       self.im_v[self.image_version - 1][0])
        self.image_top = os.path.join(self.data_dir, self.task, "planning_v3", self.exp_name,
                                      self.im_v[self.image_version - 1][1])
        # self.task_json = os.path.join(self.data_dir, self.task, "planning_v3", self.exp_name, "task_instruction.json")

        self.domain_image = [self.image_top, self.image_side]
        self.original_domain_image = [self.im_top, self.im_side]

        # json_dir
        self.api_json = os.path.join(self.json_dir, self.args.api_json)
        self.robot_json = os.path.join(self.json_dir, self.args.robot_json)
        self.def_json = os.path.join(self.json_dir, "definitions.json")
        self.task_json = os.path.join(self.json_dir, "task_instruction.json")

        # additional path
        self.database_path = os.path.join(self.data_dir, self.task)
        self.object_list = []
        self.db = {}

        # read json data
        self.robot_data = self.get_json_data(self.robot_json)
        self.task_data = self.get_json_data(self.task_json)
        self.definition = self.get_json_data(self.def_json)

    def check_result_folder(self):
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)
            print(f"Directory '{self.result_dir}' created successfully.")
        else:
            print(f"Directory '{self.result_dir}' already exists.")

    def get_api_key(self):
        with open(self.api_json, "r") as file:
            setting = json.load(file)
            api_key = setting["api_key"]
            file.close()
            return api_key, setting

    def get_json_data(self, json_path):
        with open(json_path, "r") as file:
            data = json.load(file)
            data = data[self.task]
        return data

    def detect_single_object(self, images):
        self.gpt_interface_vision.reset_message()
        system_message, prompt = self.load_prompt.load_naming_message()
        self.gpt_interface_vision.add_message(role="system", content=system_message, image_url=False)
        self.gpt_interface_vision.add_message(role="user", content=prompt, image_url=images)
        for i in range(self.patience_repeat):
            try:
                answer = self.gpt_interface_vision.run_prompt()
                result_dict = parse_single_name(answer=answer)
                self.question.append(prompt)
                self.answer.append(answer)
                return result_dict
            except:
                raise Exception("Making expected answer went wrong. ")

    def detect_object(self):
        # self.gpt_interface_vision.reset_message()
        answer = self.detect_spatial_relationship()
        time.sleep(1)
        system_message, prompt = self.load_prompt.load_naming_message()
        self.gpt_interface_vision.add_message(role="assistant", content=answer, image_url=False)
        self.gpt_interface_vision.add_message(role="system", content=system_message, image_url=False)
        self.gpt_interface_vision.add_message(role="user", content=prompt, image_url=self.original_domain_image)

        for i in range(self.patience_repeat):
            try:
                answer = self.gpt_interface_vision.run_prompt()
                result_dict, result_list = object_parsing(answer=answer)
                self.question.append(prompt)
                self.answer.append(answer)
                return result_dict, result_list
            except:
                raise Exception("Making expected answer went wrong. ")

    def detect_spatial_relationship(self):
        self.gpt_interface_vision.reset_message()
        system_message, prompt = self.load_prompt.load_spatial_relationships()
        self.gpt_interface_vision.add_message(role="system", content=system_message, image_url=False)
        self.gpt_interface_vision.add_message(role="user", content=prompt, image_url=self.domain_image)
        answer = self.gpt_interface_vision.run_prompt()

        self.question.append(prompt)
        self.answer.append(answer)
        return answer

    def get_predicates(self, detected_object_dict, random_mode=True):
        """
        detected_object_dict:
        {
        'Objects_out_box': ['white_3D_cylinder', 'black_3D_cylinder'],
        'Objects_in_box': ['white_1D_ring', 'green_1D_ring'],
        'Bin': ['white_box']
        }
        """
        self.object_dict = dict_parsing(detected_object_dict)
        all_predicates = []
        if random_mode:
            for index, info in self.object_dict.items():
                predicates = self.robot.random_active_search(info)
                info["predicates"] = predicates
                all_predicates += predicates

        else:  # Do robot active validation
            for index, info in self.object_dict.items():
                predicates = self.robot.get_object_predicates(self.database, info)
                info["predicates"] = predicates
                all_predicates += predicates

        # Removing duplicate predicates.
        active_predicates = list(set(all_predicates))
        return active_predicates

    def get_object_class(self, object_dict, active_predicates):
        self.gpt_interface_text.reset_message()

        # load prompt
        system_message, prompt = self.load_prompt.load_prompt_object_class(object_dict=object_dict,
                                                                           max_predicates=self.max_predicates)

        if active_predicates:
            prompt += "Also you have to add predicates such as "
            for predicate in active_predicates:
                if predicate == active_predicates[-1]:
                    prompt += f"and {predicate}. \n"
                else:
                    prompt += predicate + ", "
        else:
            prompt += "We don't have to consider physical properties of the object."

        prompt += "You are free to add more predicates for bin_packing to class Object if necessary. \n"
        prompt += f"Add more predicates needed for {self.task} to class Object. \n"
        prompt += """
Please answer using the template below:
---template start---
Answer:
```python
# only write a code here without example instantiation
```
Reason:
# Explain in less than 200 words and why you made such predicates
---template end---
"""
        # add message
        self.gpt_interface_text.add_message(role="system", content=system_message, image_url=False)
        self.gpt_interface_text.add_message(role="user", content=prompt, image_url=False)

        # run prompt
        for i in range(self.patience_repeat):
            try:
                answer = self.gpt_interface_text.run_prompt()

                def extract_predicates(input_str, target):
                    start = input_str.find(target) + len(target)
                    end = input_str.find("```", start)
                    result = input_str[start:end].strip()
                    return result

                object_class_python_script = extract_predicates(answer, "python\n")
                object_class_python_script += """
                
@dataclass
class Box:
    # Basic dataclass
    index: int
    name: str
    
    # Predicates for box
    object_type: str  # box or obj
    in_bin_objects: list                
"""
                self.question.append(prompt)
                self.answer.append(object_class_python_script)
                return object_class_python_script
            except:
                raise Exception("Making expected answer went wrong. ")

    def get_robot_action_conditions_v2(self, object_class_python_script):
        self.gpt_interface_text.reset_message()
        # load prompt
        system_message, prompt1 = self.load_prompt.load_prompt_robot_action_prev(object_class_python_script)

        # add message
        self.gpt_interface_text.add_message(role="system", content=system_message, image_url=False)
        self.gpt_interface_text.add_message(role="user", content=prompt1, image_url=False)

        # run prompt
        answer = self.gpt_interface_text.run_prompt()
        self.question.append(prompt1)
        self.answer.append(answer)

        # load prompt
        _, prompt = self.load_prompt.load_prompt_robot_action(
            object_class_python_script=object_class_python_script)
        self.gpt_interface_text.add_message(role="assistant", content=answer, image_url=False)
        self.gpt_interface_text.add_message(role="user", content=prompt, image_url=False)
        answer = self.gpt_interface_text.run_prompt()

        def extract_predicates(input_str, target):
            start = input_str.find(target)
            end = input_str.find("```", start)
            result = input_str[start:end].strip()
            return result

        robot_class_python_script = extract_predicates(answer, "class Robot")
        self.question.append(prompt)
        self.answer.append(answer)
        return robot_class_python_script

    def get_robot_action_conditions(self, object_class_python_script):
        self.gpt_interface_text.reset_message()

        # load prompt
        system_message, prompt = self.load_prompt.load_prompt_robot_action(
            object_class_python_script=object_class_python_script)

        # add message
        self.gpt_interface_text.add_message(role="system", content=system_message, image_url=False)
        self.gpt_interface_text.add_message(role="user", content=prompt, image_url=False)

        # run prompt
        answer = self.gpt_interface_text.run_prompt()

        def extract_predicates(input_str, target):
            start = input_str.find(target)
            end = input_str.find("```", start)
            result = input_str[start:end].strip()
            return result

        robot_class_python_script = extract_predicates(answer, "class Robot")
        # print(robot_class_python_script)
        self.question.append(prompt)
        self.answer.append(answer)
        return robot_class_python_script

    def get_init_state(self,
                       object_dict,
                       object_python,
                       robot_python):

        self.gpt_interface_text.reset_message()
        system_message, prompt = self.load_prompt.load_prompt_init_state(object_dict=object_dict,
                                                                         object_python=object_python)

        self.gpt_interface_text.add_message(role="system", content=system_message, image_url=False)
        self.gpt_interface_text.add_message(role="user", content=prompt, image_url=False)

        # run prompt
        answer = self.gpt_interface_text.run_prompt()
        self.question.append(prompt)
        self.answer.append(answer)

        def extract_table(input_str, target):
            start = input_str.find(target) + len(target)
            end = input_str.find("### 2.", start)
            result = input_str[start:end].strip()
            return result

        def extract_code(input_str, target):
            start = input_str.find(target) + len(target)
            end = input_str.find("```", start)
            result = input_str[start:end].strip()
            return result

        init_state_table = extract_table(answer, "Init Table\n")
        init_state_code = extract_code(answer, "```python\n")
        return init_state_table, init_state_code

    def get_goal_state(self, init_state_table):
        self.gpt_interface_text.reset_message()

        # load prompt
        system_message, prompt = self.load_prompt.load_prompt_goal_state(init_state_table,
                                                                         self.task_data["goals"],
                                                                         self.task_data["rules"])

        # add message
        self.gpt_interface_text.add_message(role="system", content=system_message, image_url=False)
        self.gpt_interface_text.add_message(role="user", content=prompt, image_url=False)

        # run prompt
        answer = self.gpt_interface_text.run_prompt()
        self.question.append(prompt)
        self.answer.append(answer)

        # split a text
        def extract_table(input_str, target):
            start = input_str.find(target) + len(target)
            end = input_str.find("### 2.", start)
            result = input_str[start:end].strip()
            return result

        goal_state_table = extract_table(answer, "1. Goal Table\n")
        return goal_state_table

    def planning_from_domain(self,
                             object_class_python_script,
                             robot_class_python_script,
                             init_state_python_script,
                             goal_state_table):

        self.gpt_interface_text.reset_message()
        system_message, prompt = self.load_prompt.load_prompt_planning()

        self.gpt_interface_text.add_message(role="system", content=system_message, image_url=False)
        self.gpt_interface_text.add_message(role="user", content=prompt, image_url=False)

        answer = self.gpt_interface_text.run_prompt()
        self.question.append(prompt)
        self.answer.append(answer)

        def extract_code(input_str, target):
            start = input_str.find(target) + len(target)
            end = input_str.find("```", start)
            result = input_str[start:end].strip()
            return result

        planning_python_script = extract_code(answer, "python\n")
        return planning_python_script

    def planning_from_domain_v2(self,
                                object_class_python_script,
                                robot_class_python_script,
                                init_state_python_script,
                                goal_state_table):
        self.gpt_interface_text.reset_message()
        system_message, prompt = self.load_prompt.load_prompt_planning_prev(
            object_class_python_script=object_class_python_script,
            robot_class_python_script=robot_class_python_script,
            init_state_python_script=init_state_python_script,
            goal_state_table=goal_state_table)
        self.gpt_interface_text.add_message(role="system", content=system_message, image_url=False)
        self.gpt_interface_text.add_message(role="user", content=prompt, image_url=False)

        answer = self.gpt_interface_text.run_prompt()
        self.question.append(prompt)
        self.answer.append(answer)

        _, prompt = self.load_prompt.load_prompt_planning()

        self.gpt_interface_text.add_message(role="assistant", content=answer, image_url=False)
        self.gpt_interface_text.add_message(role="user", content=prompt, image_url=False)

        answer = self.gpt_interface_text.run_prompt()
        self.question.append(prompt)
        self.answer.append(answer)

        def extract_code(input_str, target):
            start = input_str.find(target) + len(target)
            end = input_str.find("```", start)
            result = input_str[start:end].strip()
            return result

        planning_python_script = extract_code(answer, "python\n")
        return planning_python_script

    def make_plan(self):
        # detect Object and make action predicates for objects
        detected_object_dict, _ = self.detect_object()
        time.sleep(1)

        active_predicates, object_dict = self.get_predicates(detected_object_dict, random_mode=self.random_mode)
        time.sleep(1)

        # integrate objects physical predicates to other predicates
        object_class_python_script = self.get_object_class(object_dict=object_dict,
                                                           active_predicates=active_predicates)
        time.sleep(1)

        # make robot action conditions
        robot_class_python_script = self.get_robot_action_conditions(object_class_python_script)
        time.sleep(1)

        # make an init state
        init_state_table, init_state_code = self.get_init_state(object_dict=object_dict,
                                                                object_python=object_class_python_script,
                                                                robot_python=robot_class_python_script)
        time.sleep(1)

        # make a goal state
        goal_state_table = self.get_goal_state(init_state_table=init_state_table)
        time.sleep(1)

        # direct planning from objects
        planning_python_script = self.planning_from_domain(object_class_python_script=object_class_python_script,
                                                           robot_class_python_script=robot_class_python_script,
                                                           init_state_python_script=init_state_code,
                                                           goal_state_table=goal_state_table)

        if self.is_save:
            self.check_result_folder()
            self.log_conversation()
            table_path = os.path.join(self.result_dir, "table.txt")
            with open(table_path, "w") as file:
                file.write("The Init State\n")
                file.write(str(init_state_table) + "\n\n\n")
                file.write("The Goal State\n")
                file.write(str(goal_state_table) + "\n")
                file.close()

            file_path = os.path.join(self.result_dir, "planning.py")
            with open(file_path, "w") as file:
                file.write(str(object_class_python_script) + "\n\n")
                file.write(str(robot_class_python_script) + "\n\n")
                file.write("    def dummy(self):\n        pass\n\n\n")
                file.write(" # Object Initial State\n")
                file.write(str(init_state_code) + "\n\n")
                file.write(str(planning_python_script) + "\n")
                file.close()

            with open(os.path.join(self.result_dir, "object.json"), 'w') as file:
                json.dump(object_dict, file, indent=4)

    def only_detection(self):
        detected_object_dict, detected_object_list = self.detect_object()
        active_predicates, object_dict = self.get_predicates(detected_object_dict, random_mode=self.random_mode)
        if self.is_save:
            self.check_result_folder()
            self.log_conversation()
        return active_predicates, object_dict

    def only_detection_2(self):
        detected_object_dict, detected_object_list = self.detect_object()
        if self.is_save:
            self.check_result_folder()
            self.log_conversation()
        return detected_object_dict

    def make_robot_action2(self, dict_obj):
        active_predicates, object_dict = self.get_predicates(dict_obj, random_mode=self.random_mode)
        time.sleep(0.5)

        # integrate objects physical predicates to other predicates
        object_class_python_script = self.get_object_class(object_dict=object_dict,
                                                           active_predicates=active_predicates)
        time.sleep(0.5)

        # make robot action conditions
        robot_class_python_script = self.get_robot_action_conditions(object_class_python_script)
        time.sleep(0.5)

    def make_plan_2(self, dict_obj):
        active_predicates = self.get_predicates(dict_obj, random_mode=self.random_mode)
        time.sleep(0.5)

        # integrate objects physical predicates to other predicates
        object_class_python_script = self.get_object_class(object_dict=self.object_dict,
                                                           active_predicates=active_predicates)
        time.sleep(0.5)

        # # make robot action conditions
        robot_class_python_script = self.get_robot_action_conditions_v2(object_class_python_script)
        time.sleep(0.5)

        # make an init state
        init_state_table, init_state_code = self.get_init_state(object_dict=self.object_dict,
                                                                object_python=object_class_python_script,
                                                                robot_python=robot_class_python_script)
        time.sleep(0.5)

        # make a goal state
        goal_state_table = self.get_goal_state(init_state_table=init_state_table)
        time.sleep(0.5)

        # direct planning from objects
        planning_python_script = self.planning_from_domain_v2(object_class_python_script=object_class_python_script,
                                                              robot_class_python_script=robot_class_python_script,
                                                              init_state_python_script=init_state_code,
                                                              goal_state_table=goal_state_table)

        if self.is_save:
            self.check_result_folder()
            self.log_conversation()
            table_path = os.path.join(self.result_dir, "table.txt")
            with open(table_path, "w") as file:
                file.write("The Init State\n")
                file.write(str(init_state_table) + "\n\n\n")
                file.write("The Goal State\n")
                file.write(str(goal_state_table) + "\n")
                file.close()

            file_path = os.path.join(self.result_dir, "planning.py")
            with open(file_path, "w") as file:
                file.write(str(object_class_python_script) + "\n\n\n")
                file.write(str(robot_class_python_script) + "\n\n")
                file.write("    def dummy(self):\n        pass\n\n\n")
                file.write(" # Object Initial State\n")
                file.write(str(init_state_code) + "\n\n")
                file.write(str(planning_python_script) + "\n")
                file.close()

            with open(os.path.join(self.result_dir, "object.json"), 'w') as file:
                json.dump(self.object_dict, file, indent=4)

    def log_conversation(self, filename="prompt.txt"):
        # log question and answer
        log_txt_path = os.path.join(self.result_dir, filename)

        with open(log_txt_path, "w") as file:
            if filename == "prompt.txt":
                file.write(tabulate(self.table))
                file.write("\n")
            file.write("-" * 50 + "\n")
            for q, a in zip(self.question, self.answer):
                file.write("Q: ")
                file.write(q + "\n\n")
                file.write("A: \n")
                file.write(a + "\n")
                file.write("--" * 50 + "\n\n")
            file.close()

    def planning_feedback(self):
        """
        find Error type
        if systax error: easy
        rule에 의한 error
        """

        if self.planning_repeat == 0:
            file_path = os.path.join(self.result_dir, "planning.py")
            self.planning_repeat += 1
        else:
            file_path = os.path.join(self.result_dir, f"planning_feed{self.planning_repeat}.py")
            self.planning_repeat += 1
        with open(file_path, "r") as file:
            content = file.read()
            file.close()

        # Get planning old_result
        process = subprocess.Popen(["python", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if not error:
            return False

        if error:  # robot action re-definition
            planning_output = output.decode('utf-8') + "\n" + error.decode('utf-8')
            answer = self.state_feedback(python_script=content, planning_output=planning_output)

            new_plan = self.replace_planning_code(content, answer)

            if self.is_save:
                new_file_path = os.path.join(self.result_dir, f"planning_feed{self.planning_repeat}.py")
                feedback_prompt = os.path.join(self.result_dir, f"prompt_feed{self.planning_repeat}.txt")
                planning_result_path = os.path.join(self.result_dir, f"planning_result{self.planning_repeat - 1}.txt")
                with open(new_file_path, "w") as file:
                    file.write(str(new_plan) + "\n\n")
                    file.close()
                with open(feedback_prompt, "w") as file:
                    file.write(answer)
                    file.close()
                with open(planning_result_path, "w") as file:
                    file.write(planning_output)
                    file.close()
            return True

    def state_feedback(self, python_script, planning_output):
        self.gpt_interface_text.reset_message()
        system_message, prompt = self.load_prompt.load_prompt_action_feedback(python_script=python_script,
                                                                              planning_output=planning_output,
                                                                              rules=self.task_data["rules"],
                                                                              goals=self.task_data["goals"])

        self.gpt_interface_text.add_message(role="system", content=system_message, image_url=False)
        self.gpt_interface_text.add_message(role="user", content=prompt, image_url=False)
        answer = self.gpt_interface_text.run_prompt()
        return answer

    def replace_planning_code(self, python_planning_code, output):
        planning_end_part = ["\nclass Robot", "\n# Object Init State", '\nif __name__ == "__main__":', "\n\n    print"]

        def extract_planning_part(input_str, target1, target2):
            start1 = input_str.find(target1) + len(target1)
            end1 = input_str.find("# Analysis", start1)
            result1 = input_str[start1:end1].strip()

            start2 = input_str.find(target2) + len(target2)
            end2 = input_str.find("```", start2)
            result2 = input_str[start2:end2].strip()
            return result1, result2

        planning_part, planning_content = extract_planning_part(output, "# Wrong Part", "python\n")
        p_idx = list(map(int, re.findall(r'\d+', planning_part)))[0]
        new_planning_script = self.replace_string(python_planning_code, planning_content, planning_end_part[p_idx - 1])
        return new_planning_script

    @staticmethod
    def replace_string(content, replace_part, end_part):
        fline_index = replace_part.find("\n")
        replace_def = replace_part[:fline_index]

        start_index = content.find(replace_def)
        end_index = content.find(end_part, start_index + 1)
        if end_index == -1:
            end_index = len(content)

        before = content[:start_index]
        middle = replace_part
        after = content[end_index:]

        replaced_script = before + middle + "\n\n    " + after
        return replaced_script

    def just_chat(self, message, role="user", image_url=False):
        if not image_url:
            self.gpt_interface_text.reset_message()
            self.gpt_interface_text.add_message(role=role, content=message, image_url=False)
            answer = self.gpt_interface_text.run_prompt()
            return answer
        else:
            self.gpt_interface_vision.reset_message()
            self.gpt_interface_vision.add_message(role=role, content=message, image_url=image_url)
            answer = self.gpt_interface_vision.run_prompt()
            return answer

    def append_chat(self, message, role="user", is_reset=False):
        if is_reset:
            self.gpt_interface_text.reset_message()
        self.gpt_interface_text.add_message(role=role, content=message, image_url=False)

    def run_chat(self):
        answer = self.gpt_interface_text.run_prompt()
        return answer

    def state_parsing(self, init_state_table, goal_state_table):
        json_state_path = os.path.join(self.result_dir, "state.json")

        def parse_state(state_str):
            state_dict = {}
            lines = state_str.strip().split('\n')
            header = [x.strip() for x in lines[1].strip('|').split('|')]

            for line in lines[3:]:
                data = [x.strip() for x in line.strip('|').split('|')]
                item_name = data[header.index('item')].strip()
                if "--" in item_name:
                    break
                state_dict[item_name] = {}
                for i, field in enumerate(header):
                    if field != 'item':
                        state_dict[item_name][field] = data[i].strip()
            return state_dict

        init_state = parse_state(init_state_table)
        goal_state = parse_state(goal_state_table)

        self.state = {
            "init_state": init_state,
            "goal_state": goal_state
        }

        with open(json_state_path, "w") as file:
            json.dump(self.state, file, indent=4)
            file.close()

    def probing_property_llms(self, object_name, property_keys, action, images):
        self.gpt_interface_vision.reset_message()

        def parsing_predicates_answer(input_str, target):
            positive = False
            negative = False

            start = input_str.find(target) + len(target)
            end = input_str.find('\n---')
            result = input_str[start:end].strip()
            if 'rigid' in result:
                negative = 'is_rigid'
            elif 'plastic' in result:
                negative = 'is_plastic'
            else:
                positive = True

            return positive, negative

        system_message, prompt = self.load_prompt.load_property_probing_message_1()
        self.gpt_interface_vision.add_message(role="system", content=system_message, image_url=False)
        self.gpt_interface_vision.add_message(role="user", content=prompt, image_url=images[0] + images[1])
        answer = self.gpt_interface_vision.run_prompt()
        self.gpt_interface_vision.add_message(role="assistant", content=answer)
        time.sleep(1)
        self.question.append(prompt)
        self.answer.append(answer)

        prompt = self.load_prompt.load_property_probing_message_2(object_name=object_name,
                                                                  action=action,
                                                                  property_keys=property_keys)
        self.gpt_interface_vision.add_message(role="user", content=prompt)
        answer = self.gpt_interface_vision.run_prompt()
        self.gpt_interface_vision.add_message(role="assistant", content=answer)
        time.sleep(1)
        self.question.append(prompt)
        self.answer.append(answer)

        prompt = self.load_prompt.load_property_probing_message_3(object_name=object_name,
                                                                  action=action,
                                                                  property_keys=property_keys)
        self.gpt_interface_vision.add_message(role="user", content=prompt, image_url=images[0] + images[1])
        answer = self.gpt_interface_vision.run_prompt()
        time.sleep(1)
        self.question.append(prompt)
        self.answer.append(answer)

        positive, negative = parsing_predicates_answer(answer, '- Property: ')
        if positive:
            positive = list(property_keys[action].keys())[0]
            recover_action = self.robot.action_recover
            self.gpt_interface_vision.reset_message()

            system_message, prompt = self.load_prompt.load_property_probing_message_1()
            self.gpt_interface_vision.add_message(role="system", content=system_message, image_url=False)
            self.gpt_interface_vision.add_message(role="user", content=prompt,
                                                  image_url=images[0] + images[1] + images[2])
            answer = self.gpt_interface_vision.run_prompt()
            self.gpt_interface_vision.add_message(role="assistant", content=answer)
            time.sleep(1)
            self.question.append(prompt)
            self.answer.append(answer)

            prompt = self.load_prompt.load_property_probing_message_2(object_name=object_name,
                                                                      action=recover_action,
                                                                      property_keys=property_keys,
                                                                      before_pos=positive)
            self.gpt_interface_vision.add_message(role="user", content=prompt)
            answer = self.gpt_interface_vision.run_prompt()
            self.gpt_interface_vision.add_message(role="assistant", content=answer)
            time.sleep(1)
            self.question.append(prompt)
            self.answer.append(answer)

            prompt = self.load_prompt.load_property_recover_message(object_name=object_name,
                                                                    action=recover_action,
                                                                    property_keys=property_keys,
                                                                    before_action=action)
            self.gpt_interface_vision.add_message(role="user", content=prompt,
                                                  image_url=images[0] + images[1] + images[2])
            answer = self.gpt_interface_vision.run_prompt()
            time.sleep(1)
            self.question.append(prompt)
            self.answer.append(answer)
            positive, negative = parsing_predicates_answer(answer, '- Property: ')
            if positive:
                positive = list(property_keys[action].keys())[0]
                properties = positive
            else:
                properties = negative

        else:
            properties = negative

        return properties

    def probing_property(self, object_name, images: list[list]):
        property_keys = self.robot.property_keys
        if "1D" in object_name:
            action = self.robot.action_1d
            properties = self.probing_property_llms(object_name=object_name,
                                                    property_keys=property_keys,
                                                    action=action,
                                                    images=images)
        elif "2D" in object_name:
            action = self.robot.action_2d
            properties = self.probing_property_llms(object_name=object_name,
                                                    property_keys=property_keys,
                                                    action=action,
                                                    images=images)
        elif "3D" in object_name:
            action = self.robot.action_3d
            properties = self.probing_property_llms(object_name=object_name,
                                                    property_keys=property_keys,
                                                    action=action,
                                                    images=images)
        else:
            raise ValueError

        if self.is_save:
            self.check_result_folder()
            self.log_conversation(filename="probing_conversation.txt")

        return properties

    def initialize_database(self, object_num: int):
        """
        using exist database

        [total_image]: top + side + probe_image[1,2,3] + recover_image[1,2,3] = total 8
        obj1_top_base_image
        obj1_side_base_image

        # using only side image
        obj1_side_probe_image
        obj1_side_probe_image
        obj1_side_probe_image

        # using only side image
        obj1_side_recover_image
        obj1_side_recover_image
        obj1_side_recover_image

        :param object_num: the number of existing object data
        :return:
        """

        print(f"Making Database... {object_num} ")
        root = os.path.join(self.database_path, "property_search_database", f"obj{object_num}")

        data_path = list_file(root)
        data_path = sort_files(data_path)

        base_images = []
        probe_images = []
        recover_images = []
        for name in data_path:
            if "base" in name:
                base_images.append(name)

            elif "probe" in name:
                probe_images.append(name)

            elif "recover" in name:
                recover_images.append(name)
            else:
                pass

        base_images = sort_files(base_images)
        probe_images = sort_files(probe_images)
        recover_images = sort_files(recover_images)

        object_name = self.detect_single_object(images=base_images)
        object_properties = self.probing_property(object_name=object_name,
                                                  images=[base_images, probe_images, recover_images])

    def save_db(self):
        with open(os.path.join(self.database_path, "database_new.json"), 'w') as file:
            json.dump({self.task: self.db}, file, indent=4)

        log_txt_path = os.path.join(self.database_path, "database_reason_new.txt")
        i = 1
        with open(log_txt_path, "w") as file:
            for q, a in zip(self.question, self.answer):
                file.write(q)
                file.write("\n")
                file.write(a)
                file.write("\n\n")
                if i % 2 == 0:
                    file.write("------\n\n")
                i += 1
            file.write("\n\n\n\n")
            file.close()

    def object_dict_save(self):
        json_path = os.path.join(self.data_dir, self.task, "planning", self.exp_name)

        detected_object_dict, detected_object_list = self.detect_object()
        _, object_dict = self.get_predicates(detected_object_dict, random_mode=False)

        with open(os.path.join(json_path, "planning_object_gt.json"), 'w') as file:
            json.dump(object_dict, file, indent=4)

    def vanilla_property_probing(self, object_name, images, info=False):
        """

        :param object_name:
        :param images:
        :param info:
        :return:
        """

        def parsing_property(text):
            if ": 'is_rigid'" in text:
                properties = 'is_rigid'
            elif ": 'is_bendable'" in text:
                properties = 'is_bendable'
            elif ": 'is_foldable'" in text:
                properties = 'is_foldable'
            elif ": 'is_compressible'" in text:
                properties = 'is_compressible'
            elif ": 'is_plastic'" in text:
                properties = 'is_plastic'
            else:
                properties = "Error"
            return properties

        if not object_name:
            self.gpt_interface_vision.reset_message()
            system_message, prompt = self.load_prompt.load_prompt_vanilla_probing()

            self.gpt_interface_vision.add_message(role="system", content=system_message, image_url=False)
            self.gpt_interface_vision.add_message(role="user", content=prompt, image_url=images)
            answer = self.gpt_interface_vision.run_prompt()

        else:
            self.gpt_interface_vision.reset_message()
            system_message, prompt = self.load_prompt.load_prompt_vanilla_probing(object_name, info)

            self.gpt_interface_vision.add_message(role="system", content=system_message, image_url=False)
            self.gpt_interface_vision.add_message(role="user", content=prompt, image_url=images)
            answer = self.gpt_interface_vision.run_prompt()

        self.question.append(prompt)
        self.answer.append(answer)
        properties = parsing_property(answer)
        if self.is_save:
            self.check_result_folder()
            self.log_conversation(filename="probing_conversation.txt")

        return properties

    def probing_property_vanilla(self, object_name, images):
        property_keys = self.robot.property_keys
        if "1D" in object_name:
            action = self.robot.action_1d
        elif "2D" in object_name:
            action = self.robot.action_2d
        elif "3D" in object_name:
            action = self.robot.action_3d
        else:
            raise ValueError

        def parsing_property(text):
            if ": 'is_rigid'" in text:
                properties = 'is_rigid'
            elif ": 'is_bendable'" in text:
                properties = 'is_bendable'
            elif ": 'is_foldable'" in text:
                properties = 'is_foldable'
            elif ": 'is_compressible'" in text:
                properties = 'is_compressible'
            elif ": 'is_plastic'" in text:
                properties = 'is_plastic'
            else:
                properties = "Error"
            return properties

        self.gpt_interface_vision.reset_message()
        system_message, prompt = self.load_prompt.load_prompt_vanilla_three_image(object_name, action)
        self.gpt_interface_vision.add_message(role="system", content=system_message, image_url=False)
        self.gpt_interface_vision.add_message(role="user", content=prompt, image_url=images[0] + images[1] + images[2])
        answer = self.gpt_interface_vision.run_prompt()

        self.question.append(prompt)
        self.answer.append(answer)
        properties = parsing_property(answer)
        if self.is_save:
            self.check_result_folder()
            self.log_conversation(filename="probing_conversation.txt")

        return properties

    def ODModule(self, image):
        image = self.classifier.load_image(image)
        obj_name, _ = self.classifier.predict_label(image)
        return obj_name

    def property_probing_exp(self,
                             obj_name,
                             images,
                             mode: int):
        if mode == 0:
            properties = self.vanilla_property_probing(object_name=None, images=images)

        elif mode == 1:
            image_path = f"/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v3_objects/obj_top_{self.exp_number}.png"
            obj_name = self.ODModule(image=image_path)
            properties = self.vanilla_property_probing(object_name=obj_name, images=images)

        elif mode == 2:
            # Vanilla input without decision tree
            properties = self.probing_property_vanilla(object_name=obj_name, images=images)

        elif mode == 3:
            properties = self.probing_property(object_name=obj_name, images=images)

        else:
            raise ValueError

        return properties