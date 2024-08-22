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
    pushed: bool
    folded: bool
    
    # Predicates for box
    in_bin_objects: list
    
    # Object physical properties 
    is_soft: bool
    is_rigid: bool
    is_elastic: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_rigid=False, is_elastic=True, in_box=False, out_box=True)
object1 = Object(index=1, name='green_2D_circle', color='green', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_rigid=True, is_elastic=False, in_box=False, out_box=True)
object2 = Object(index=2, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_rigid=False, is_elastic=True, in_box=False, out_box=True)
object3 = Object(index=3, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_rigid=True, is_elastic=False, in_box=True, out_box=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_rigid=False, is_elastic=False, in_box=True, out_box=False)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    initial_state = {
        0: {'name': 'brown_3D_cuboid', 'in_box': False, 'out_box': True},
        1: {'name': 'green_2D_circle', 'in_box': False, 'out_box': True},
        2: {'name': 'white_3D_cylinder', 'in_box': False, 'out_box': True},
        3: {'name': 'yellow_3D_cylinder', 'in_box': True, 'out_box': False},
        4: {'name': 'white_box', 'in_box': True, 'out_box': False, 'in_bin_objects': []}
    }

    goal_state = {
        0: {'name': 'brown_3D_cuboid', 'in_box': True, 'out_box': False},
        1: {'name': 'green_2D_circle', 'in_box': True, 'out_box': False},
        2: {'name': 'white_3D_cylinder', 'in_box': True, 'out_box': False},
        3: {'name': 'yellow_3D_cylinder', 'in_box': True, 'out_box': False},
        4: {'name': 'white_box', 'in_box': True, 'out_box': False, 'in_bin_objects': [0, 1, 2, 3]}
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Rules:
    # 1. Place soft objects first if there are any before placing rigid objects.
    # 2. Fold objects only if they are foldable.
    # 3. Only push soft objects after placing items in the bin.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object4

    # Action sequence
    # 1. Place soft objects first
    robot.place(object0, box)  # Place brown_3D_cuboid
    robot.place(object2, box)  # Place white_3D_cylinder

    # 2. Place rigid objects
    robot.place(object1, box)  # Place green_2D_circle
    robot.place(object3, box)  # Place yellow_3D_cylinder

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - Placed soft objects (object0 and object2) first as per the rule.
    # - Placed rigid objects (object1 and object3) after soft objects were placed.
    # - No foldable objects in this scenario.
    # - No push action required as per the rules.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_bin_objects == [0, 1, 2, 3]

    print("All task planning is done")
