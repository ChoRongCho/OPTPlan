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
    is_elastic: bool
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
object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_elastic=False, is_rigid=True, in_box=False, out_box=True)
object1 = Object(index=1, name='blue_2D_loop', color='blue', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_elastic=False, is_rigid=False, in_box=False, out_box=True)
object2 = Object(index=2, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_elastic=True, is_rigid=False, in_box=False, out_box=True)
object3 = Object(index=3, name='green_3D_sphere', color='green', shape='3D_sphere', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_elastic=False, is_rigid=True, in_box=True, out_box=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_elastic=False, is_rigid=False, in_box=True, out_box=False)

### 3. Notes:
# The table and Python code represent the initial state of the bin_packing domain.
# Each object has been initialized with its respective properties and predicates.
# The 'in_bin_objects' list is empty for all objects initially.
# The 'in_box' and 'out_box' predicates are mutually exclusive and set according to the initial poses provided.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_elastic=False, is_rigid=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='blue_2D_loop', color='blue', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_elastic=False, is_rigid=False, in_box=False, out_box=True)
    object2 = Object(index=2, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_elastic=True, is_rigid=False, in_box=False, out_box=True)
    object3 = Object(index=3, name='green_3D_sphere', color='green', shape='3D_sphere', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_elastic=False, is_rigid=True, in_box=True, out_box=False)
    object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_elastic=False, is_rigid=False, in_box=True, out_box=False)

    # Goal state
    goal_object0_in_box = True
    goal_object1_in_box = True
    goal_object2_in_box = True
    goal_object3_in_box = True
    goal_object4_in_bin_objects = [0, 1, 2, 3]

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place the white_2D_loop (soft object) in the box first.
    # 2. Place the yellow_3D_cylinder (rigid object) in the box.
    # 3. Place the blue_2D_loop (non-rigid, non-elastic object) in the box.
    # 4. Ensure the green_3D_sphere (fragile object) is already in the box.
    # 5. Push the white_box to include all objects.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object4

    # Action sequence
    robot.pick(object2)  # Pick white_2D_loop
    robot.place(object2, box)  # Place white_2D_loop in the box

    robot.pick(object0)  # Pick yellow_3D_cylinder
    robot.place(object0, box)  # Place yellow_3D_cylinder in the box

    robot.pick(object1)  # Pick blue_2D_loop
    robot.place(object1, box)  # Place blue_2D_loop in the box

    # green_3D_sphere is already in the box, no action needed

    robot.push(box)  # Push the box to include all objects

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. Placed white_2D_loop (soft object) first as per the rule.
    # 2. Placed yellow_3D_cylinder (rigid object) after the soft object.
    # 3. Placed blue_2D_loop (non-rigid, non-elastic object) next.
    # 4. green_3D_sphere (fragile object) was already in the box.
    # 5. Pushed the box to include all objects.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == goal_object0_in_box
    assert object1.in_box == goal_object1_in_box
    assert object2.in_box == goal_object2_in_box
    assert object3.in_box == goal_object3_in_box
    assert box.in_bin_objects == goal_object4_in_bin_objects

    print("All task planning is done")
