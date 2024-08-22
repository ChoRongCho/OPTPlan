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
    is_fragile: bool
    is_soft: bool
    is_rigid: bool
    is_elastic: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool




    def dummy(self):
        pass


 # Object Initial State
code
# don't include the object classes or robot class, make only objects and bin 
# example 
object0 = Object(index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=True, is_rigid=False, is_elastic=True, in_box=False, out_box=True)
object1 = Object(index=1, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_soft=False, is_rigid=True, is_elastic=False, in_box=False, out_box=True)
object2 = Object(index=2, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=True, is_rigid=False, is_elastic=False, in_box=False, out_box=True)
object3 = Object(index=3, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=False, is_rigid=True, is_elastic=False, in_box=False, out_box=True)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=False, is_rigid=False, is_elastic=False, in_box=True, out_box=False)

### 3. Notes:
# The table and the Python code represent the initial state of the bin_packing domain.
# Each object has been initialized with its properties and predicates as per the given information.
# The 'in_bin_objects' list is empty for all objects initially.
# The 'in_box' and 'out_box' predicates are mutually exclusive and have been set according to the 'init_pose' provided.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    object0 = Object(index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=True, is_rigid=False, is_elastic=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_soft=False, is_rigid=True, is_elastic=False, in_box=False, out_box=True)
    object2 = Object(index=2, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=True, is_rigid=False, is_elastic=False, in_box=False, out_box=True)
    object3 = Object(index=3, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=False, is_rigid=True, is_elastic=False, in_box=False, out_box=True)
    object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=False, is_rigid=False, is_elastic=False, in_box=True, out_box=False)

    # Goal state
    goal_state = {
        0: {'in_box': True, 'out_box': False},
        1: {'in_box': True, 'out_box': False},
        2: {'in_box': True, 'out_box': False},
        3: {'in_box': True, 'out_box': False},
        4: {'in_box': True, 'out_box': False, 'in_bin_objects': [0, 1, 2, 3]}
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place soft objects first (object0, object2)
    # 2. Place fragile and rigid objects after soft objects (object1, object3)

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object4

    # c) Action sequence
    # Place soft objects first
    robot.pick(object0)
    robot.place(object0, box)
    robot.pick(object2)
    robot.place(object2, box)

    # Place fragile and rigid objects after soft objects
    robot.pick(object1)
    robot.place(object1, box)
    robot.pick(object3)
    robot.place(object3, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasons:
    # 1. Soft objects (object0, object2) are placed first to satisfy the rule: "Before placing a fragile or rigid object, soft object should be in the box if there are any soft objects."
    # 2. Fragile and rigid objects (object1, object3) are placed after soft objects.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_bin_objects == [0, 1, 2, 3]

    print("All task planning is done")
