from dataclasses import dataclass

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj
    
    # Basic effect predicates for obj
    pushed: bool = False
    folded: bool = False
    
    # Predicates for box
    in_bin_objects: list = None
    
    # Object physical properties 
    is_soft: bool = False
    is_elastic: bool = False
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool = False
    out_box: bool = True




    def dummy(self):
        pass


 # Object Initial State
code
# don't include the object classes or robot class, make only objects and bin 
# example 
object0 = Object(index=0, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', is_soft=True, is_elastic=True, in_box=False, out_box=True)
object1 = Object(index=1, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', is_elastic=True, in_box=False, out_box=True)
object2 = Object(index=2, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', is_elastic=True, in_box=False, out_box=True)
object3 = Object(index=3, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', is_soft=True, is_elastic=True, in_box=True, out_box=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', in_bin_objects=[], in_box=True, out_box=False)

### 3. Notes:
# The initial state table and Python code reflect the properties and initial positions of the objects as described in the input.
# The 'in_bin_objects' list for the box is initialized as empty since no objects are specified to be inside the box initially.
# The 'in_box' and 'out_box' flags are set according to the 'init_pose' provided in the input.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    object0 = Object(index=0, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', is_soft=True, is_elastic=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', is_elastic=True, in_box=False, out_box=True)
    object2 = Object(index=2, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', is_elastic=True, in_box=False, out_box=True)
    object3 = Object(index=3, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', is_soft=True, is_elastic=True, in_box=True, out_box=False)
    object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', in_bin_objects=[], in_box=True, out_box=False)

    # Goal state
    goal_state = {
        0: {'in_box': True, 'out_box': False},
        1: {'in_box': True, 'out_box': False},
        2: {'in_box': True, 'out_box': False},
        3: {'in_box': True, 'out_box': False},
        4: {'in_bin_objects': [0, 1, 2, 3]}
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Rules:
    # 1. Place soft objects first if there are any.
    # 2. Fold objects only if they are foldable.
    # 3. Only push soft objects after placing items in the bin.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object4

    # Action sequence
    # 1. Place soft objects first
    robot.place(object0, box)  # Place white_3D_cylinder
    robot.place(object3, box)  # Place yellow_3D_cuboid

    # 2. Place remaining objects
    robot.place(object1, box)  # Place transparent_3D_cylinder
    robot.place(object2, box)  # Place transparent_2D_circle

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - Placed soft objects (object0 and object3) first as per the rule.
    # - Placed remaining objects (object1 and object2) after soft objects.
    # - No folding or pushing actions were required as per the rules.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_bin_objects == [0, 1, 2, 3]

    print("All task planning is done")
