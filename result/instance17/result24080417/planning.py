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
    is_elastic: bool
    is_soft: bool
    is_fragile: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    init_pose: str
    in_box: bool




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_soft=True, is_fragile=False, init_pose='out_box', in_box=False)
object1 = Object(index=1, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_soft=False, is_fragile=False, init_pose='out_box', in_box=False)
object2 = Object(index=2, name='blue_2D_loop', color='blue', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_fragile=False, init_pose='out_box', in_box=False)
object3 = Object(index=3, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_fragile=True, init_pose='in_box', in_box=True)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_fragile=False, init_pose='box', in_box=False)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    initial_state = {
        0: {'name': 'yellow_3D_cuboid', 'in_box': False},
        1: {'name': 'white_2D_loop', 'in_box': False},
        2: {'name': 'blue_2D_loop', 'in_box': False},
        3: {'name': 'white_2D_circle', 'in_box': True},
        4: {'name': 'white_box', 'in_box': False}
    }
    
    goal_state = {
        0: {'name': 'yellow_3D_cuboid', 'in_box': True},
        1: {'name': 'white_2D_loop', 'in_box': True},
        2: {'name': 'blue_2D_loop', 'in_box': True},
        3: {'name': 'white_2D_circle', 'in_box': True},
        4: {'name': 'white_box', 'in_box': False, 'in_bin_objects': [0, 1, 2, 3]}
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Rules:
    # 1. Place soft objects before fragile or rigid objects.
    # 2. Fold objects only if they are foldable.
    # 3. Only push soft objects after placing items in the bin.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object4

    # c) Action sequence
    # Place the soft object first
    robot.place(object0, box)
    
    # Place the other objects
    robot.place(object1, box)
    robot.place(object2, box)
    
    # The fragile object is already in the box, so no need to place it again

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. Placed the soft object (yellow_3D_cuboid) first as per the rule.
    # 2. Placed the other objects (white_2D_loop and blue_2D_loop) after the soft object.
    # 3. The fragile object (white_2D_circle) was already in the box, so no action was needed for it.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_bin_objects == [0, 1, 2, 3]
    
    print("All task planning is done")
