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
    is_elastic: bool = False
    is_soft: bool = False
    is_rigid: bool = False
    
    # Pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool = False
    out_box: bool = False




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='white_3D_cylinder', 
    color='white', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=None, 
    is_elastic=True, 
    is_soft=True, 
    is_rigid=False, 
    in_box=False, 
    out_box=True
)

object1 = Object(
    index=1, 
    name='black_3D_cylinder', 
    color='black', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=None, 
    is_elastic=False, 
    is_soft=False, 
    is_rigid=True, 
    in_box=False, 
    out_box=True
)

object2 = Object(
    index=2, 
    name='yellow_3D_cuboid', 
    color='yellow', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=None, 
    is_elastic=True, 
    is_soft=True, 
    is_rigid=False, 
    in_box=True, 
    out_box=False
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=False, 
    is_soft=False, 
    is_rigid=False, 
    in_box=True, 
    out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    initial_state = {
        0: {'in_box': False, 'out_box': True, 'is_soft': True, 'is_rigid': False},
        1: {'in_box': False, 'out_box': True, 'is_soft': False, 'is_rigid': True},
        2: {'in_box': True, 'out_box': False, 'is_soft': True, 'is_rigid': False},
        3: {'in_box': True, 'out_box': False, 'in_bin_objects': []}
    }
    
    # Goal State
    goal_state = {
        0: {'in_box': True, 'out_box': False},
        1: {'in_box': True, 'out_box': False},
        2: {'in_box': True, 'out_box': False},
        3: {'in_box': True, 'out_box': False, 'in_bin_objects': [0, 1, 2]}
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place the soft object (white_3D_cylinder) in the box first.
    # 2. Place the rigid object (black_3D_cylinder) in the box.
    # 3. Ensure the yellow_3D_cuboid remains in the box.
    # 4. Update the white_box to include all objects.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object3

    # c) Action sequence
    # Place the soft object (white_3D_cylinder) in the box
    robot.place(object0, box)
    object0.in_box = True
    object0.out_box = False
    box.in_bin_objects.append(object0.index)

    # Place the rigid object (black_3D_cylinder) in the box
    robot.place(object1, box)
    object1.in_box = True
    object1.out_box = False
    box.in_bin_objects.append(object1.index)

    # Ensure the yellow_3D_cuboid remains in the box (already in the box)
    # No action needed for object2

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. The white_3D_cylinder is soft and should be placed in the box before the rigid object.
    # 2. The black_3D_cylinder is rigid and can be placed after the soft object is in the box.
    # 3. The yellow_3D_cuboid is already in the box and does not need to be moved.
    # 4. The white_box should contain all objects as per the goal state.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_bin_objects == [0, 1, 2]
    
    print("All task planning is done")
