from scripts.utils.utils import int_to_ordinal


class PromptSet:
    def __init__(self, task, task_description, definition):
        self.task = task
        self.task_description = task_description
        self.definition = definition

        self.def_shape = "".join(self.definition["shape"])
        self.def_property = "".join(self.definition["properties"])
        self.def_dimension = "".join(self.definition["dimension"])

    def load_naming_module_single(self):
        system_message = f"You are a vision AI designed to describe the shape and color of objects for {self.task}. " + \
                         "Analyze the given images of the objects and accurately describe their size and color. " + \
                         "Use the provided classification table to categorize the objects, " + \
                         "adhering strictly to the given classifications rather than relying on common sense."

        prompt = f"""
The first image shows a top view of objects (the one which is the closest to the center of the image) while the second image shows a side view of them.
Please identify the shapes, dimensions, and colors of the object based on these images according to the definitions in "[Definitions of dimensions and shapes]" below.
Your answer must follow the naming convention which is "color_dimension_shape" (e.g., red_3D_cuboid or black_2D_ring).
Ensure that there is no contradiction between the shape and dimension. For example, "3D" and "circle" are not compatible according to their definitions in "[Definitions of dimensions and shapes]".

[Definitions of dimensions and shapes]
Dimension
{self.def_dimension}

Shape
{self.def_shape}

Your answer must use the template below:

Please answer with the template below:
---template start---
Answer: red_3D_cuboid, black_2D_ring or etc  # these are examples for your answer format

Descriptions about the object in the scene
*your descriptions in 200 words
---template end---
"""
        return system_message, prompt

    def load_spatial_relationships(self):
        system_message = f"You are a vision AI designed to describe the spatial relationships of the objects. "
        message = """ 
The first image shows a top view of an object (the one which is the closest to the center of the image) while the second image shows a side view of them.
Each view captures the same scene, with the objects in the images corresponding one-to-one between the two views.
I will provide you with images that have bounding boxes drawn around the objects and its logits. 
However, unfortunately, these images can occasionally contain errors. 
Therefore, you need to make accurate judgments about the objects' positions and relationships. 
Additionally, the white lines represent the relationships between the bounding boxes, so think of this as a graph.

Based on the spatial information from this graph, you should be able to recognize the same objects. 
Please describe the given environment based on these images.      

Your answer must use the template below:

Please answer with the template below:
---template start---
### Objects and Their Descriptions:
# top view
|  top index  | descriptions  
|      1      |  
|      2      |
  
# side view
|  side index  | descriptions
|       1      |  
|       2      |

# Find same objects in both views 


### Spatial Relationships:

### Critical bounding box errors Description:
# if there is any critical error such as wrong bonding box and additional bounding box, describe here 

---template end---

  
"""

        return system_message, message

    def load_naming_message(self):
        # Use 1D, 2D, 3D definition of ChatGPT

        system_message = f"You are a vision AI designed to describe the shape and color of objects for {self.task}. " + \
                         "Analyze the given images of the objects and accurately describe their size and color. " + \
                         "Use the provided classification table to categorize the objects, " + \
                         "adhering strictly to the given classifications rather than relying on common sense."

        prompt = f"""
Now that you've obtained the spatial information of the objects, you need to describe each object's shape, color, and dimensions.
And for clarity, I will provide the original images. Please identify the shapes, dimensions, and colors of the object based on these images according to the definitions in "[Definitions of dimensions and shapes]" below.
Your answer must follow the naming convention which is "color_dimension_shape" (e.g., red_3D_cuboid or black_2D_ring).
Ensure that there is no contradiction between the shape and dimension. For example, "1D" and "loop" or "3D" and "circle" are not compatible according to their definitions in "[Definitions of dimensions and shapes]".

[Definitions of dimensions and shapes]
Dimension
{self.def_dimension}

Shape
{self.def_shape}

Your answer must use the template below:

Please answer with the template below:
---template start---
Answer
---
object: red_3D_polyhedron, yellow_3D_cuboid, ... # if there are duplicate objects, add '_N' at the end, e.g., red_3D_cuboid_2.
---

Descriptions about objects in the scene
*your descriptions in 200 words
---template end---
"""
        return system_message, prompt

    def load_prompt_object_class(self, object_dict, max_predicates):
        system_message = f"""
You are an AI assistant responsible for converting the properties of objects into predicates used in generating an action sequence for {self.task}. The predicates for object properties will be assigned Boolean values. Please follow these rules:
1. Do not create more predicates than the given max_predicates.
2. Use the template provided below.
"""
        prompt = f"We are going to generate an action sequence to perform the task, {self.task}, using Python which works similar to PDDL. " + \
                 "Our goal is to define the types of objects and their predicates within the dataclass Object. \n"
        prompt += "Here, we have the types, names, and properties of the objects recognized from the input images. We need to use this information to complete the Object class."
        prompt += f"{object_dict} \n\n"
        prompt += f"""from dataclasses import dataclass


@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj
    
    # physical state of an object
    pushed: bool
    folded: bool
    in_bin: bool
    
    # Object physical properties 
    
    # pre-conditions and effects for {self.task} task planning (max: {max_predicates})

@dataclass
class Box:
    # Basic dataclass
    index: int
    name: str
    
    # Predicates for box
    object_type: str  # box or obj
    in_bin_objects: list

"""
        prompt += "However, we cannot complete a planning with this dataclass predicate alone" + \
                  f" which means that we have to add other predicates that fully describe {self.task} task. \n"

        return system_message, prompt

    def load_prompt_robot_action(self,
                                 object_class_python_script,
                                 robot_action,
                                 task_instruction):

        system_message = f"""
You are an action designer responsible for strictly defining the preconditions and effects of the robot's actions for {self.task} task.
When defining a robot action, you should refer exclusively to the given rules. 
Based on the action definitions, write the pre-conditions and effects of the actions in Python scripts accordingly. 
Be sure to follow the template below.
"""

        prompt = ("Our current task is to create actions for the robot, similar to the domain file in PDDL. "
                  "The parts corresponding to the types of objects and predicates are provided as a class object, as shown below.")
        prompt += f"""{object_class_python_script}\n\n"""

        prompt += ("Our goal is to define the pre-conditions and effects for the robot's actions, similar to how they are done in PDDL. \n"
                   "Definitions of pre-conditions and effects in natural language are provided in each action in the basic "
                   "Robot class below. Please refer to them to create actions.")

        prompt += f"""
class Robot:
    def __init__(self,
                 name: str = "OpenManipulator",
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
        # make a pre-conditions for actions using if-else phrase
        # Action Description: {robot_action["pick"]}
        print(f"Pick obj.name")
        print(f"Cannot Pick obj.name")
        
    def place(self, obj, bin):
        # Action Description: {robot_action["place"]}
        print(f"Place obj.name in bin.name")
        print(f"Cannot Place obj.name")
        bin.in_bin_objects.append(obj)
    
    def push(self, obj, bin): 
        # Action Description: {robot_action["push"]}
        print(f"Push obj.name")
        print(f"Cannot Push obj.name")
        obj.pushed
    
    def fold(self, obj, bin):
        # Action Description: {robot_action["fold"]}
        print(f"Fold obj.name")
        print(f"Cannot Fold obj.name")
        obj.folded
    
    def out(self, obj, bin):
        # Action Description: {robot_action["out"]}
        print(f"Out obj.name from bin.name")
        print(f"Cannot Out obj.name")
        bin.in_bin_objects.remove(obj)
        \n\n"""

        prompt += "Please make more action pre-conditions and effect of the robot "
        prompt += f"For example, if you place an object in hand, obj.in_bin=False. \n"
        prompt += "However, if there are predicates that are mentioned in the rules but not in the object class, " + \
                  "do not reflect those predictions in the rules."
        prompt += """

Please answer with the template below:
---template start---
Answer:
```python
# only write a code here without example instantiation
class Robot:
    def __init__(self, ...):
        ...    
    def state_handempty(self):
        ...
    def state_holding(self, objects):
        ...  
    def state_base(self):
        ...
```
Reason:
# Explain in less than 300 words why you made such robot actions
1. pick
2. place
3. push
4. fold
5. out
---template end---
"""
        return system_message, prompt

    def load_prompt_init_state(self,
                               object_dict,
                               object_python):

        system_message = ("You are going to organize the given content in a table. "
                          "These tasks are for defining initial states. ") + \
                          "Also, you should follow the template below. "

        prompt = f"We are now making initial state of the {self.task}. We get these information from the input images. \n\n"
        prompt += f"{object_dict}\n"
        prompt += f"{object_python}\n\n"

        prompt += "Using the above information, Please organize the initial state of the domain in a table. \n\n"
        prompt += """
Please answer with the template below:
---template start---
### 1. Init Table
# fill your table using objects predicates

### 2. Python Codes
# make init state into python code
# don't include the object classes or robot class, make only objects and bin 
# example  
```python
object0 = Object(index=0, name='black_3D_cuboid', color='black', shape='3D_cuboid', ...)
object1 = Object(index=1, name='white_2D_circle', color='white', shape='2D_circle', ...)
box = Box()
```
...

### 3. Notes:
# Fill your notes
---template end---
"""

        return system_message, prompt

    def load_prompt_goal_state(self, init_state_table, goals, rules):

        system_message = "You are going to organize the given content in a table. These tasks are for defining a goal state. " + \
                         "Also, you should follow the template below. "

        prompt = (f"We are now making goal state of the {self.task}. "
                  f"Your goal is to redefine the goal state given in natural language into a table. \n\n")
        prompt += f"This is an init state table. \n"
        prompt += f"{init_state_table}\n\n"
        prompt += f"Our goal is listed below. \n"
        prompt += f"{goals}\n"
        prompt += f"And, this is rules that when you do actions. \n"
        prompt += f"{rules}\n\n"

        prompt += "\nUsing the above information, Please organize the goal state of the domain in a table. \n\n"
        prompt += """
Please answer with the template below:
---template start---
### 1. Goal Table
# fill your table similar with initial state

### 2. Notes:
# Fill your notes
---template end---
"""

        return system_message, prompt

    def load_prompt_planning(self,
                             object_class_python_script: str,
                             robot_class_python_script: str,
                             init_state_python_script: str,
                             init_state_table: str,
                             goal_state_table: str,
                             rules: dict):

        system_message = (f"Your role is to create an action sequence for {self.task} similar to PDDL, "
                          f"using the given Object class (which includes types and predicates), "
                          f"the Robot class (which includes actions), as well as the initial and goal states."
                          f"The action sequence consists of actions and must start from the initial state and end at the goal state."
                          f"An action incurs a transition between states where each state describes objects using predicates and properties."
                          f"The initial state will be provided as Python code, and you need to use the action functions "
                          f"defined in the Robot class to generate an action sequence that reaches the goal state.")
        system_message += "Also, you should follow the template below. "

        prompt = "This is the Object class, which defines both object types and predicates. \n"
        prompt += f"{object_class_python_script}\n\n"
        prompt += "This is the Robot class, which includes pre-conditions and effects of actions. \n"
        prompt += f"{robot_class_python_script}\n\n"
        prompt += "This is the initial state represented in a python code. \n"
        prompt += f"{init_state_python_script}\n\n"

        # prompt += f"Your goal is {self.task_description}. \n"
        prompt += "You must follow the rules: \n"
        prompt += f"{rules}\n"

        prompt += "Make an action sequence under the if __name__ == '__main__':. \nYou must make a correct action sequence. \n"
        prompt += "An action sequence is incorrect if any of its actions with a conditional statement does not satisfy the if clause.\n"
        prompt += (f"\nThis is the initial state table of all objects. \n{init_state_table}\n\n"
                   f"And this is the goal state table of all objects. \n{goal_state_table}\n\n")

        prompt += f"""
Please answer with the template below:
---template start---

if __name__ == "__main__":
    # First, using given rules and object's states, make a task planning strategy
    
    # Second, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box, this is an example. 
    box = object5

    # Third, after making all actions, fill your reasons according to the rules
    ...
    
    # Finally, add this code    
    print("All task planning is done")
     
---template end---
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
3. Planning State (Start with [if __name__ == "__main__":])

And this is a result of the code.
{planning_output}

Here are rules and goals you should refer
rules: {rules}
goals: {goals}

All you need to do is fix the wrong action or syntax error in the given code. You have to use the goal state given in the code.
Please answer with the template below:

---template start---
# First, check the actions of robot class
a) Do pre-conditions satisfy the given rules?
b) Is the effect of action right?
c) Is there any syntax error in action codes?

# Second, check the symbolic robot action under [if __name__ == "__main__"]
d) Is the goal state right at assert part?
e) Is the order of robot action right?
f) Are there unnecessary actions?

Here, I'll give you a template.

# Wrong Part (Choose one from an error description) 
1. Object Class / 2. Robot Class / 3. Planning State

# Analysis using given error
# a) 
# b)
# c)
# d)
# e) 
# f)

# Modified Code (Make the error part only)
```python
# part 2 (example)

```
---template end---

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
                         f"{self.def_property}" + \
                         f"Answer the questions below in accordance with this criterion. Also, you should follow the template below. "

        prompt = f"\nThe first two images are original images of {object_name}. Please refer to this image and answer. \n"
        end_message = f"""Please answer with the template below:  
---template start---
Answer  # If there is no mention of the object's properties, fill it with False. 
**rigid: True or False
**soft: True or False
**foldable: True or False
**elastic: True or False

Reason:
-Describe a object and feel free to write down your reasons for each properties in less than 50 words
---template end---
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
