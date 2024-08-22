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
    is_rigid: bool
    is_fragile: bool
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
object0 = Object(index=0, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_fragile=True, is_elastic=False, in_box=False, out_box=True)
object1 = Object(index=1, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_fragile=False, is_elastic=False, in_box=False, out_box=True)
object2 = Object(index=2, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_fragile=False, is_elastic=True, in_box=False, out_box=True)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_fragile=False, is_elastic=False, in_box=True, out_box=False)

### 3. Notes:
# The initial state table and Python code represent the initial conditions of the objects and bin for the bin_packing task.
# The 'in_bin_objects' list is empty for all objects initially, indicating no objects are in the bin.
# The 'pushed' and 'folded' predicates are set to False for all objects as no actions have been performed yet.
# The 'in_box' and 'out_box' predicates are set according to the initial positions of the objects.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    object0 = Object(index=0, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_fragile=True, is_elastic=False, in_box=False, out_box=True)
    object1 = Object(index=1, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_fragile=False, is_elastic=False, in_box=False, out_box=True)
    object2 = Object(index=2, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_fragile=False, is_elastic=True, in_box=False, out_box=True)
    object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_fragile=False, is_elastic=False, in_box=True, out_box=False)

    # Goal state
    goal_object0 = Object(index=0, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_fragile=True, is_elastic=False, in_box=True, out_box=False)
    goal_object1 = Object(index=1, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_fragile=False, is_elastic=False, in_box=True, out_box=False)
    goal_object2 = Object(index=2, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_fragile=False, is_elastic=True, in_box=True, out_box=False)
    goal_object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[0, 1, 2], is_rigid=False, is_fragile=False, is_elastic=False, in_box=True, out_box=False)

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place the soft object (transparent_2D_circle) in the box first.
    # 2. Place the rigid and fragile object (green_3D_cylinder) in the box.
    # 3. Place the rigid object (black_3D_cylinder) in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object3

    # Action sequence
    robot.pick(object2)  # Pick transparent_2D_circle
    robot.place(object2, box)  # Place transparent_2D_circle in the box

    robot.pick(object0)  # Pick green_3D_cylinder
    robot.place(object0, box)  # Place green_3D_cylinder in the box

    robot.pick(object1)  # Pick black_3D_cylinder
    robot.place(object1, box)  # Place black_3D_cylinder in the box

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasons:
    # 1. The soft object (transparent_2D_circle) is placed in the box first as per the rule.
    # 2. The fragile object (green_3D_cylinder) is placed after the soft object.
    # 3. The rigid object (black_3D_cylinder) is placed last.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_bin_objects == [0, 1, 2]

    print("All task planning is done")
