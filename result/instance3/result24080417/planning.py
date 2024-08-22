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
    is_rigid: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool




    def dummy(self):
        pass


 # Object Initial State
code
# don't include the object classes or robot class, make only objects and bin 
# example 
object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_rigid=True, in_box=False, out_box=True)
object1 = Object(index=1, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_soft=False, is_rigid=False, in_box=False, out_box=True)
object2 = Object(index=2, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=True, is_rigid=False, in_box=False, out_box=True)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_rigid=False, in_box=True, out_box=False)

### 3. Notes:
# The initial state table and Python code represent the initial conditions of the objects and the box in the bin_packing domain.
# The 'in_bin_objects' list is empty for all objects initially, indicating that no objects are inside the box at the start.
# The 'pushed' and 'folded' predicates are set to False for all objects, as these actions have not been performed yet.
# The 'in_box' and 'out_box' predicates are mutually exclusive and indicate the initial position of each object.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_rigid=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_soft=False, is_rigid=False, in_box=False, out_box=True)
    object2 = Object(index=2, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=True, is_rigid=False, in_box=False, out_box=True)
    object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_rigid=False, in_box=True, out_box=False)

    # Goal state
    goal_object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_rigid=True, in_box=True, out_box=False)
    goal_object1 = Object(index=1, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_soft=False, is_rigid=False, in_box=True, out_box=False)
    goal_object2 = Object(index=2, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=True, is_rigid=False, in_box=True, out_box=False)
    goal_object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[0, 1, 2], is_elastic=False, is_soft=False, is_rigid=False, in_box=True, out_box=False)

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place the soft object (red_3D_polyhedron) in the box first.
    # 2. Place the rigid object (yellow_3D_cylinder) in the box.
    # 3. Place the elastic object (white_2D_loop) in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Action sequence
    robot.pick(object2)  # Pick red_3D_polyhedron
    robot.place(object2, box)  # Place red_3D_polyhedron in the box

    robot.pick(object0)  # Pick yellow_3D_cylinder
    robot.place(object0, box)  # Place yellow_3D_cylinder in the box

    robot.pick(object1)  # Pick white_2D_loop
    robot.place(object1, box)  # Place white_2D_loop in the box

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. The soft object (red_3D_polyhedron) is placed first as per the rule.
    # 2. The rigid object (yellow_3D_cylinder) is placed after the soft object.
    # 3. The elastic object (white_2D_loop) is placed last.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_bin_objects == [0, 1, 2]

    print("All task planning is done")
