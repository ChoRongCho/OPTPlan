from typing import List

from scripts.utils.utils import int_to_ordinal


class PromptSet:
    def __init__(self, task, task_description):
        self.task = task
        self.task_description = task_description

    def load_prompt_detect_object(self):
        prompt = f"We are now doing a {self.task} task. \n"
        prompt += "This is a first observation where I work in. \n"
        prompt += "What objects or tools are here? \n"
        return prompt

    def load_prompt_object_class(self, object_dict, max_predicates):
        system_message = "You are an assistant who organizes the properties of objects in task planning for bin_packing." + \
                         "Your role is to create an object property that has a Boolean value required for task planning." + \
                         "I'll tell you the rules you need to follow here. \n" + \
                         "1. You should never make a predicate beyond the given max_predicates. \n" + \
                         "2. You should follow the template below. " + \
                         ""
        prompt = f"We are now going to do a {self.task} task whose goal is {self.task_description}"
        prompt += "There are many objects in this domain, " + \
                  "this is an object information that comes from image observations. \n"
        prompt += f"1. {object_dict} \n\n"
        prompt += f"""from dataclasses import dataclass


@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj

    # Object physical properties predicates

    # {self.task} predicates expressed as a boolean (max {max_predicates})\n"""
        prompt += "However, we cannot do complete planning with this dataclass predicate alone" + \
                  f" that means we have to add another predicates that fully describe the {self.task}. \n"

        return system_message, prompt

    def load_prompt_robot_action(self,
                                 object_class_python_script,
                                 robot_action,
                                 task_instruction):

        system_message = "You are an action designer that strictly defines what the robot's action brings to the state." + \
                         "When you define robot action, you should make it by referring only to the given rule." + \
                         "You should look at the definition of the robot's action and write the preconditions of the action and its effects in Python scripts accordingly." + \
                         "Also, you should follow the template below. "

        prompt = f"We are now going to do a {self.task} task which means {self.task_description}. \n"
        prompt += "We have a basic python structure describing the available robot actions. \n"
        prompt += f"""{object_class_python_script}\n\n"""
        prompt += """
class Robot:
    # Define skills
    def __init__(self,
                 name: str = "UR5",
                 goal: str = None,
                 actions: dict = None):
        self.name = name
        self.goal = goal
        self.actions = actions
    
        self.robot_handempty = True
        self.robot_now_holding = False
        self.robot_base_pose = True
    
    # basic state
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_base_pose = False
    
    # basic state
    def state_holding(self, objects):
        self.robot_handempty = False
        self.robot_now_holding = objects
        self.robot_base_pose = False
    
    # basic state
    def state_base(self):
        self.robot_base_pose = True
    
    def pick(self, obj, bin):
        # make a preconditions for actions using if phrase
        print(f"Pick {obj.name}")
        
    def place(self, obj, bin):
        # make a preconditions for actions
        print(f"Place {obj.name} in {bins.name}")
    
    def push(self, obj, bin): 
        # make a preconditions for actions
        print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # make a preconditions for actions
        print(f"Fold {obj.name}")
    
    def out(self, obj, bin):
        # make a preconditions for actions
        print(f"Out {obj.name} from {obj.name}")\n\n"""

        prompt += "I want to create the preconditions and effects of the robot actions based on the given rules that is similar to PDDL stream. \n"
        prompt += f"""
{robot_action}
{task_instruction}\n"""
        prompt += "Please make more action conditions and effect of the robot " + \
                  f"and objects state that used for {self.task}. \n"
        prompt += f"For example, if you place an object in hand, obj.in_bin=False. \n"
        prompt += "However, if there are predicates that are mentioned in the rules but not in the object class, " + \
                  "do not reflect those predictions in the rules."
        prompt += """
Answer:
# only write a Robot python class here without example instantiation

        
Reason:
# Explain in less than 300 words why you made such robot action
"""
        return system_message, prompt

    def load_prompt_init_state(self,
                               object_dict,
                               object_python,
                               robot_python):

        system_message = "You are going to organize the given content in a table. These tasks are for defining initial states. " + \
                         "You should define the basic and physical predicates of objects resulting from objects' properties. " + \
                         "Also, you should follow the template below. "

        prompt = f"We are now making initial state of the {self.task}. We get these information from the observation. \n\n"
        prompt += f"{object_dict}\n"
        prompt += f"{object_python}\n"
        prompt += f"{robot_python}\n\n"

        prompt += "Using above information, Please organize the initial state of the domain in a table. \n\n"
        prompt += """
### 1. Init Table
# fill your table

### 2. Notes:
# Fill your notes

### 3. Python Codes
# make init state into python code
# don't include the object classes or robot class, make only objects and bin 
# example 
object0 = Object(index=0, name='black_3D_cuboid', color='black', shape='3D_cuboid', ...)
object1 = Object(index=1, name='white_2D_circle', color='white', shape='2D_circle', ...)
...

"""

        return system_message, prompt

    def load_prompt_goal_state(self, init_state_table, goals, rules):

        system_message = "You are going to organize the given content in a table. These tasks are for defining a goal state. " + \
                         "You should define the basic and physical predicates of objects resulting from rules and goals of bin_packing task. " + \
                         "Also, you should follow the template below. "

        prompt = (f"We are now making goal state of the {self.task}. "
                  f"Your goal is to redefine the goal state given in natural language into a table. \n\n")
        prompt += f"This is an init state table. \n"
        prompt += f"{init_state_table}\n\n"
        prompt += f"Our goal is listed below. \n"
        prompt += f"{goals}\n"
        prompt += f"And, this is rules that when you do actions. \n"
        prompt += f"{rules}\n\n"

        prompt += "\nUsing above information, Please organize the goal state of the domain in a table. \n\n"
        prompt += """
### 1. Goal Table
# fill your table similar with initial state

### 2. Notes:
# Fill your notes
"""

        return system_message, prompt

    def load_prompt_planning(self,
                             object_class_python_script,
                             robot_class_python_script,
                             init_state_python_script,
                             init_state_table,
                             goal_state_table,
                             rules):

        system_message = (f"You are a direct Python planner and you need to complete the {self.task} task planning"
                          f" using the given robot action and objects. ")
        system_message += ("You need to create an action sequence so that the init state reach to the goal state according to the given rules. "
                           "This action sequence should use robot class.")
        system_message += "Also, you should follow the template below. "

        prompt = f"{object_class_python_script}\n\n"
        prompt += f"{robot_class_python_script}\n\n"
        prompt += f"{init_state_python_script}\n\n"

        prompt += "if __name__ == '__main__':\n\t# packing all object in the box\n\t# make a plan\n"

        # prompt += f"Your goal is {self.task_description}. \n"
        prompt += "You must follow the rules: \n"
        prompt += f"{rules}\n"

        prompt += "Make a plan under the if __name__ == '__main__':. \nYou must make a correct action sequence. \n"
        prompt += f"{init_state_table}\n\n{goal_state_table}\n\n"

        prompt += """
if __name__ == "__main__":
    # Using goal table, Describe the final state of each object
     
    # make your order
    
    # after making all actions, fill your reasons according to the rules
    
    # check if the goal state is satisfied using goal state table 
"""

        return system_message, prompt

    def load_prompt_action_feedback(self, python_script, planning_output):
        prompt = f"We made a plan for a {self.task} and our goal is {self.task_description}. \n"
        prompt += f"Below is the Python code for it. \n\n"
        prompt += python_script + " \n"

        prompt += "And this is a old_result. \n"
        prompt += planning_output + " \n"

        prompt += "We find that there is an error in the robot action part that describes the preconditions and " + \
                  "effects of the action. \n"
        prompt += "Please modify the action preconditions if they use preconditions that the Object class doesn't use. \n"
        return prompt

    def load_prompt_planner_feedback(self, python_script, planning_output, task_instruction, robot_action):
        prompt = f"We made a plan for a {self.task} and our goal is {self.task_description}. \n"
        prompt += f"Below is the Python code for it. \n\n"
        prompt += python_script + " \n"

        prompt += "And this is a old_result. \n"
        prompt += planning_output + " \n"

        prompt += "There are some planning errors in this code that is represented as Cannot. \n" + \
                  " Here are some rules for planning. \n"
        prompt += f"{task_instruction}\n"
        prompt += f"{robot_action}\n"

        prompt += "Please re-planning under the if __name__ == '__main__' part. \n"

        return prompt

    def load_verification_message(self, available_actions: list[bool], object_name):
        n = 2
        system_message = f"You're working to verify the object's properties through images for {self.task}." + \
                         f"This table defines the physical properties of the object we are investigating." + \
                         f"Answer the questions below in accordance with this criterion. \n"
        system_message += """
---------------  -------------------------------------------------------
Predicates List  Definition(a noun form)
is_fragile       the fact of tending to break or be damaged easily
is_rigid         the fact of being very strict and difficult to change
is_soft          the quality of changing shape easily when pressed (only 3D object)
is_foldable      the ability to bend without breaking
is_elastic       the quality of returning to its original size and shape
is_flexible      the ability to change or be changed easily (only 2D and 1D object)
---------------  -------------------------------------------------------
"""

        prompt = f"\nThe first two images are original images of {object_name}. Please refer to this image and answer. \n"
        end_message = f"""Please answer with the template below:  
---
Answer
**rigid: True or False
**soft: True or False
**foldable: True or False
**elastic: True or False
**flexible: True or False

Reason:
-Describe a object and feel free to write down your reasons for each properties in less than 50 words
---
"""
        if available_actions[0]:  # push
            m1 = "We will show the image when the robot does the action 'push' on the object." + \
                 f"\nThe {int_to_ordinal(n + 1)} image is just before the robot pushes the object. \n" + \
                 f"The {int_to_ordinal(n + 2)} image is the image when the robot is pushing the object. \n" + \
                 f"If there is a significant deformation in the shape of the object, the object is soft(3D) or flexible(2D and 1D), else it is rigid. " + \
                 f"You have to keep in mind that soft and flexible are incompatible depending on the dimension of the object. \n" + \
                 f"Does this object have soft(flexible) or rigid properties? \n\n"
            n += 2
            prompt += m1

        if available_actions[1]:  # fold
            m2 = "We will show the image when the robot does the action 'fold' on the object." + \
                 f"\nThe {int_to_ordinal(n + 1)} image shows the robot just before it grabs an object. \n" + \
                 f"The {int_to_ordinal(n + 2)} image is after it is completely folded. \n" + \
                 f"The {int_to_ordinal(n + 3)} image shows after the robot leaves it hand on the object. \n" + \
                 f"If the end of the robot gripper that holds the object touches on the opposite side of the object, the object can be folded or elastic. " + \
                 f"When the robot lets go of the object, if the object return to its original shape, the object is elastic, else foldable" + \
                 f"Does this object have foldable or elastic or None properties? \n\n"
            n += 3
            prompt += m2
        if available_actions[2]:  # pull
            m3 = "We will show the image when the robot does the action 'pull' on the object." + \
                 f"\nThe {int_to_ordinal(n + 1)} image shows before the robot pulls an unknown object. \n" + \
                 (f"The {int_to_ordinal(n + 2)} image shows while the robot pulls an object. "
                  f"If an object changes in size more than twice and come back to its original shape, it can be said to be elastic."
                  f"Does this object have elastic properties? \n")
            n += 2
            prompt += m3
        prompt += end_message
        return system_message, prompt

    def load_naming_message(self):
        """
        from images, the llm module makes judge of its shape and color
        """
        system_message = f"You are a vision AI that describes the shape and color of an object for {self.task}. " + \
                         "You should look at a picture of given objects and explain their size and color."
        prompt = "The first image is when you see the object from the side " + \
                 "and the next image is when you see the object from the top. \n" + \
                 "Define the shape and color of the object through this image. \n" + \
                 "Use the simple classification table below for the shape of the object. \n" + \
                 """
-----  ----------------------------------------------             
Shape  Examples
1D     linear or ring <- if there is a space in the center like string
2D     flat rectangle, circle <- if there is no space in the center etc
3D     cube, cuboid, cylinder, cone, polyhedron, etc
-----  ----------------------------------------------

Please answer with the template below:

Answer
---
object in box: # if there is nothing, fill it blank
object out box: brown_3D_cuboid, black_3D_circle, blue_1D_ring  # this is an example
box: white_box # only color
---

Descriptions about objects in the scene
*your descriptions in 200 words

"""
        return system_message, prompt

    def load_naming_module_single(self):
        system_message = f"You are a vision AI that describes the shape and color of an object for {self.task}. " + \
                         "You should look at a picture of a given object and explain its size and color."
        prompt = "The first image is when you see the object from the side " + \
                 "and the next image is when you see the object from the top. \n" + \
                 "Define the shape and color of the object through this image. \n" + \
                 "Use the simple classification table below for the shape of the object. \n" + \
                 """
-----  ----------------------------------------------             
Shape  Examples
1D     linear or ring <- if there is a space in the center like string
2D     flat rectangle, circle <- if there is no space in the center etc
3D     cube, cuboid, cylinder, cone, polyhedron, etc
-----  ----------------------------------------------

Please answer with the template below:

---
Answer: red_3D_cuboid, black_2D_circle or blue_1D_ring or etc  # these are examples for your answer format

Descriptions about objects in the scene
*your descriptions in 200 words
---
"""
        return system_message, prompt


class PromptSetPDDL:
    def __init__(self, task, task_description):
        self.task = task
        self.task_description = task_description

    def load_prompt_detect_object(self):
        prompt = f"We are now doing a {self.task} task. \n"
        prompt += "This is a first observation where I work in. \n"
        prompt += "What objects or tools are here? \n"
        return prompt

    def load_prompt_get_predicates(self, detected_object, detected_object_types, active_predicates: List or bool):
        prompt = f"Q. We are now going to do a {self.task} task whose goal is {self.task_description}"
        prompt += "There are many objects in this domain, " + \
                  "this is object information that comes from image observation. \n"
        prompt += f"1. {detected_object_types} \n2. {detected_object}\n"

        prompt += f"""\n(define (domain {self.task})
    (:requirements :strips :typing)
    (:types ;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
        ;define types of the task
    )
    (:predicates 
        ; general predicates

        ; robot predicates

        ; object property predicates

        ; old_result of object property after action
        
    )\n\n
"""
        if active_predicates:
            prompt += "Also you have to add predicates such as "
            for predicate in active_predicates:
                if predicate == active_predicates[-1]:
                    prompt += f"and {predicate}. \n"
                else:
                    prompt += predicate + ", "
        else:
            prompt += "We don't have to consider physical properties of the object."
        prompt += f"Add more predicates needed for {self.task}." + \
                  f"Don't add predicates that are not useful for {self.task} such as shape and color. \n"
        return prompt

    def load_prompt_ruled_predicates(self,
                                     original_pddl,
                                     robot_action,
                                     task_instruction):
        prompt = f"This is a front part of the domain.pddl of the {self.task} task. \n"
        prompt += f"{original_pddl}"
        prompt += f"Here are robot actions and rules for bin_packing task. \n" + \
                  f"{robot_action}\n{task_instruction}\n"
        prompt += "Please add or modify the pddl predicates that are needed to be used for rules and actions. \n"
        return prompt

    def load_prompt_planning(self,
                             object_class_python_script,
                             robot_class_python_script,
                             init_state_python_script,
                             robot_action,
                             task_instruction):
        prompt = f"{object_class_python_script}\n\n"
        prompt += f"{robot_class_python_script}\n\n"
        prompt += f"{init_state_python_script}\n\n"
        prompt += "if __name__ == '__main__':\n\t# packing all object in the box\n\t# make a plan\n"

        prompt += f"Your goal is {self.task_description}. \n"
        prompt += "You must follow the rule: \n"
        prompt += f"""
{robot_action}
{task_instruction}\n"""

        prompt += "Make a plan under the if __name__ == '__main__':. \nYou must make a correct order. \n"
        return prompt

    def load_prompt_action_feedback(self, python_script, planning_output):
        prompt = f"We made a plan for a {self.task} and our goal is {self.task_description}. \n"
        prompt += f"Below is the Python code for it. \n\n"
        prompt += python_script + " \n"

        prompt += "And this is a old_result. \n"
        prompt += planning_output + " \n"

        prompt += "We find that there is an error in the robot action part that describes the preconditions and " + \
                  "effects of the action. \n"
        prompt += "Please modify the action preconditions if they use preconditions that the Object class doesn't use. \n"
        return prompt

    def load_prompt_planner_feedback(self, python_script, planning_output, task_instruction, robot_action):
        prompt = f"We made a plan for a {self.task} and our goal is {self.task_description}. \n"
        prompt += f"Below is the Python code for it. \n\n"
        prompt += python_script + " \n"

        prompt += "And this is a old_result. \n"
        prompt += planning_output + " \n"

        prompt += "There are some planning errors in this code that is represented as Cannot. \n" + \
                  " Here are some rules for planning. \n"
        prompt += f"{task_instruction}\n"
        prompt += f"{robot_action}\n"

        prompt += "Please re-planning under the if __name__ == '__main__' part. \n"

        return prompt
