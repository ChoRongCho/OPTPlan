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
        system_message = f"You are an AI assistant who organizes the properties of objects in task planning for {self.task}." + \
                         "Your role is to create predicates for object property that has a Boolean value required for task planning." + \
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
    
    # Basic effect predicates for obj
    pushed: bool
    folded: bool
    
    # Predicates for box
    in_bin_objects: list
    
    # Object physical properties 
    
    # Preconditions and effects for {self.task} task planning (max: {max_predicates})
    
    
"""
        prompt += "However, we cannot complete a planning with this dataclass predicate alone" + \
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
        prompt += f"""
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
        # {robot_action["pick"]}
        # make a preconditions for actions using if-else phrase
        print(f"Pick obj.name")
        print(f"Cannot Pick obj.name")
        
    def place(self, obj, bin):
        # {robot_action["place"]}
        print(f"Place obj.name in bin.name")
        bins.in_bin.append(obj)
        ...
    
    def push(self, obj, bin): 
        # {robot_action["push"]}
        print(f"Push obj.name")
        obj.pushed
        ...
    
    def fold(self, obj, bin):
        # {robot_action["fold"]}
        print(f"Fold obj.name")
        obj.folded
        ...
    
    def out(self, obj, bin):
        # {robot_action["out"]}
        print(f"Out obj.name from bin.name")
        bins.in_bin.remove(obj)
        ...\n\n"""

        prompt += "I want to create the preconditions and effects of the robot actions based on the given rules that is similar to PDDL stream. \n"
        prompt += f"""
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
# Explain in less than 300 words why you made such robot actions
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
        prompt += f"{object_python}\n\n"
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
                             object_class_python_script: str,
                             robot_class_python_script: str,
                             init_state_python_script: str,
                             init_state_table: str,
                             goal_state_table: str,
                             rules: dict):

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
        prompt += (f"\nThis is a initial state of all objects. \n{init_state_table}\n\n"
                   f"And this is a goal state of all objects. \n{goal_state_table}\n\n")

        prompt += """
if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    ...
    # Second, using given rules and object's states, make a task planning strategy
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box, this is an example. 
    box = object5
    
    # Fourth, after making all actions, fill your reasons according to the rules
    ...
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.is_in_box == True or False
    assert object1.is_in_box == True or False
    ...
    print("All task planning is done") 
"""

        return system_message, prompt

    def load_prompt_action_feedback(self, python_script, planning_output, rules, goals):
        system_message = ("You are a developer who catches and fixes errors in Python code. "
                          "You need to find the wrongs in the given code and its results and correct them. "
                          "Also, you should follow the template below. ")

        prompt = f"""This is a python code that you have to fix.\n
{python_script}\n\n 
This code consists of four parts below.
1. Object Class (Start with [@dataclass])
2. Robot Class (Start with [class Robot:])
3. Initial State (Start with [object0 = Object(...) ])
4. Planning State (Start with [if __name__ == "__main__":])

And this is a result of the code.
{planning_output}

Here are rules and goals you should refer
rules: {rules}
goals: {goals}

All you need to do is fix the wrong action or syntax error in the given code. You have to use the goal state given in the code.

# First, check the actions of robot class
a) Do preconditions satisfy the given rules?
b) Is the effect of action right?
c) Is there any syntax error in action codes?

# Second, check the symbolic robot action under [if __name__ == "__main__"]
d) Is the goal state right at assert part?
e) Is the order of robot action right?
f) Are there unnecessary actions?

Here, I'll give you a template.

# Wrong Part (Choose one from an error description) 
1. Object Class / 2. Robot Class / 3. Initial State / 4. Planning State

# Analysis using given error
# a) 
# b)
# c)
# d)
# e) 
# f)

# Modified Code (Make the part only)


"""

        return system_message, prompt

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
---------------  -------------------------------------------------------
"""

        prompt = f"\nThe first two images are original images of {object_name}. Please refer to this image and answer. \n"
        end_message = f"""Please answer with the template below:  
---
Answer  # If there is no mention of the object's properties, fill it with False. 
**rigid: True or False
**soft: True or False
**foldable: True or False
**elastic: True or False

Reason:
-Describe a object and feel free to write down your reasons for each properties in less than 50 words
---
"""
        if available_actions[0]:  # push
            m1 = "We will show the image when the robot does the action 'push' on the object to verify the object is soft or rigid." + \
                 f"\nThe {int_to_ordinal(n + 1)} image is just before the robot pushes the object. \n" + \
                 f"The {int_to_ordinal(n + 2)} image is the image when the robot is pushing the object. \n" + \
                 f"If there is a significant deformation in the shape of the object(see image {n + 1} and {n + 2}), the object is soft(3D), else it is rigid. " + \
                 f"Does this object have soft(only in 3D objects) or rigid properties? \n\n"
            n += 2
            prompt += m1

        if available_actions[1]:  # fold
            m2 = "We will show the image when the robot does the action 'fold' on the object to verify the object is foldable or elastic." + \
                 f"\nThe {int_to_ordinal(n + 1)} image shows the robot just before it grabs an object. \n" + \
                 f"The {int_to_ordinal(n + 2)} image is after it is completely folded. \n" + \
                 f"The {int_to_ordinal(n + 3)} image shows after the robot leaves it hand on the object. \n" + \
                 f"If the end of the robot gripper that holds the object touches on the opposite side of the object(see image {n + 1} and {n + 2}), the object is not rigid. \n" + \
                 f"If the object return to its original shape after the robot lets go of the object(see image {n + 1} and {n + 3}), the object is elastic, else it is foldable. \n" + \
                 f"Does this object have foldable or elastic or None properties? \n\n"
            n += 3
            prompt += m2
        if available_actions[2]:  # pull
            m3 = "We will show the image when the robot does the action 'pull' on the object to verify the object is elastic or not." + \
                 f"\nThe {int_to_ordinal(n + 1)} image shows before the robot pulls an unknown object. \n" + \
                 f"The {int_to_ordinal(n + 2)} image shows while the robot pulls the object. " + \
                 f"The {int_to_ordinal(n + 3)} image shows after the robot pulls the object. " + \
                 (f"If the object changes in size more than twice (see image {n + 1} and {n + 2}),"
                  f" and come back to its original shape(see image {n + 1} and {n + 3}), it is said to be elastic.") + \
                 f"Does this object have elastic properties? \n"
            n += 3
            prompt += m3
        prompt += end_message
        return system_message, prompt

    def load_naming_message(self):
        """
        from images, the llm module makes judge of its shape and color
        """
        # Use 1D, 2D, 3D definition of ChatGPT
        system_message = f"You are a vision AI that describes the shape and color of an object for {self.task}. " + \
                         "You should look at a picture of given objects and explain their size and color." + \
                         "Also, classify objects using the given classification table rather than your common sense."
        prompt = "The first image is when you see the object from the side " + \
                 "and the next image is when you see the object from the top. \n" + \
                 "Define the shape and color of the object through this image. \n" + \
                 "Use the simple classification table below for the shape of the object. \n" + \
                 "You should match dimension and shape. For example, 3D_circle is not acceptable. \n\n" + \
                 """
----- ----------------------------- ----------------------------------------------             
Dim   Description                   Shape
1D    related to lines or length    linear
2D    related to plane or flatness  rectangle, circle, ring
3D    related to volume             cube, cuboid, cylinder, cone, polyhedron, etc
----- ----------------------------- ----------------------------------------------

Please answer with the template below:

Answer
---
object in box: # if there is nothing, fill it blank
object out box: brown_3D_cuboid, black_3D_circle  # this is an example
box: white_box # only color
---

Descriptions about objects in the scene
*your descriptions in 200 words

"""
        return system_message, prompt

    def load_naming_module_single(self):
        system_message = f"You are a vision AI that describes the shape and color of an object for {self.task}. " + \
                         ("You should look at a picture of a given object and explain its size and color. "
                          "Also, classify objects using the given classification table rather than your common sense.")
        prompt = "The first image is when you see the object from the side " + \
                 "and the next image is when you see the object from the top. \n" + \
                 "Define the shape and color of the object through this image. \n" + \
                 "Use the simple classification table below for the shape of the object. \n" + \
                 "You should match a dimension and shape. For example, 2D_ring, 3D_circle are not acceptable. \n\n" + \
                 """
----- ----------------------------- ----------------------------------------------             
Dim   Description                   Shape
1D    related to lines or length    linear
2D    related to plane or flatness  rectangle, circle, ring
3D    related to volume             cube, cuboid, cylinder, cone, polyhedron, etc
----- ----------------------------- ----------------------------------------------

Please answer with the template below:

---
Answer: red_3D_cuboid, black_2D_ring or etc  # these are examples for your answer format

Descriptions about the object in the scene
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
