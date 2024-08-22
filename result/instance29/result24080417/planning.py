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
    is_elastic: bool
    is_rigid: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    init_pose: str
    in_box: bool




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='red_3D_polyhedron', 
    color='red', 
    shape='3D_polyhedron', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_soft=True, 
    is_elastic=False, 
    is_rigid=False, 
    init_pose='out_box', 
    in_box=False
)

object1 = Object(
    index=1, 
    name='white_3D_cylinder', 
    color='white', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_soft=True, 
    is_elastic=True, 
    is_rigid=False, 
    init_pose='out_box', 
    in_box=False
)

object2 = Object(
    index=2, 
    name='black_2D_loop', 
    color='black', 
    shape='2D_loop', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_soft=False, 
    is_elastic=False, 
    is_rigid=True, 
    init_pose='out_box', 
    in_box=False
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
    is_soft=False, 
    is_elastic=False, 
    is_rigid=False, 
    init_pose='box', 
    in_box=True
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    initial_state = {
        'object0': {'init_pose': 'out_box', 'in_box': False},
        'object1': {'init_pose': 'out_box', 'in_box': False},
        'object2': {'init_pose': 'out_box', 'in_box': False},
        'object3': {'init_pose': 'box', 'in_box': True}
    }
    
    goal_state = {
        'object0': {'goal_pose': 'in_box', 'in_box': True},
        'object1': {'goal_pose': 'in_box', 'in_box': True},
        'object2': {'goal_pose': 'in_box', 'in_box': True},
        'object3': {'goal_pose': 'box', 'in_box': True}
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Rules:
    # 1. Place soft objects first if there are any before placing fragile or rigid objects.
    # 2. Fold objects only if they are foldable.
    # 3. Only push soft objects after placing items in the bin.
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object3
    
    # Action sequence
    # 1. Place red_3D_polyhedron (soft) in the box
    robot.place(object0, box)
    
    # 2. Place white_3D_cylinder (soft and elastic) in the box
    robot.place(object1, box)
    
    # 3. Place black_2D_loop (rigid) in the box
    robot.place(object2, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - Placed red_3D_polyhedron first because it is soft.
    # - Placed white_3D_cylinder next because it is also soft and elastic.
    # - Placed black_2D_loop last because it is rigid and should be placed after soft objects.
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    
    print("All task planning is done")
