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
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_soft=True, is_rigid=False, in_box=False, out_box=True)
object1 = Object(index=1, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_rigid=True, in_box=False, out_box=True)
object2 = Object(index=2, name='blue_2D_loop', color='blue', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_rigid=False, in_box=False, out_box=True)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_rigid=False, in_box=True, out_box=False)

### 3. Notes:
# The table and Python code represent the initial state of the objects and their properties for the bin_packing task.
# The 'in_bin_objects' list is empty for all objects initially.
# The 'pushed' and 'folded' properties are set to False for all objects initially.
# The 'in_box' and 'out_box' properties are mutually exclusive and set according to the initial pose provided.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_soft=True, is_rigid=False, in_box=False, out_box=True)
    object1 = Object(index=1, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_rigid=True, in_box=False, out_box=True)
    object2 = Object(index=2, name='blue_2D_loop', color='blue', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_rigid=False, in_box=False, out_box=True)
    object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_rigid=False, in_box=True, out_box=False)

    # Goal state
    goal_object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_soft=True, is_rigid=False, in_box=True, out_box=False)
    goal_object1 = Object(index=1, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_rigid=True, in_box=True, out_box=False)
    goal_object2 = Object(index=2, name='blue_2D_loop', color='blue', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_rigid=False, in_box=True, out_box=False)
    goal_object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[0, 1, 2], is_elastic=False, is_soft=False, is_rigid=False, in_box=True, out_box=False)

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Place the soft object (yellow_3D_cuboid) in the box first
    # 2. Place the rigid object (black_3D_cylinder) in the box
    # 3. Place the non-rigid, non-soft object (blue_2D_loop) in the box

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object3

    # Action sequence
    robot.pick(object0)
    robot.place(object0, box)
    robot.pick(object1)
    robot.place(object1, box)
    robot.pick(object2)
    robot.place(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. The soft object (yellow_3D_cuboid) is placed first as per the rule.
    # 2. The rigid object (black_3D_cylinder) is placed after the soft object.
    # 3. The non-rigid, non-soft object (blue_2D_loop) is placed last.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_bin_objects == [0, 1, 2]
    
    print("All task planning is done")
