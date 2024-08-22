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
object0 = Object(index=0, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_soft=True, is_rigid=False, in_box=False, out_box=True)
object1 = Object(index=1, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_rigid=True, in_box=False, out_box=True)
object2 = Object(index=2, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_soft=False, is_rigid=False, in_box=True, out_box=False)
object3 = Object(index=3, name='blue_2D_loop', color='blue', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_rigid=False, in_box=True, out_box=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_rigid=False, in_box=True, out_box=False)

### 3. Notes:
# The 'in_bin_objects' list is empty for all objects initially.
# The 'pushed' and 'folded' predicates are set to False for all objects initially.
# The 'object_type' is set to 'obj' for all objects except the box, which is set to 'box'.
# The 'in_box' and 'out_box' predicates are mutually exclusive and set according to the initial pose.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    object0 = Object(index=0, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_soft=True, is_rigid=False, in_box=False, out_box=True)
    object1 = Object(index=1, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_rigid=True, in_box=False, out_box=True)
    object2 = Object(index=2, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_soft=False, is_rigid=False, in_box=True, out_box=False)
    object3 = Object(index=3, name='blue_2D_loop', color='blue', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_rigid=False, in_box=True, out_box=False)
    object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_rigid=False, in_box=True, out_box=False)

    # Goal State
    goal_state = {
        0: {'in_box': True, 'out_box': False},
        1: {'in_box': True, 'out_box': False},
        2: {'in_box': True, 'out_box': False},
        3: {'in_box': True, 'out_box': False},
        4: {'in_bin_objects': [0, 1, 2, 3]}
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place the soft object (object0) in the box first.
    # 2. Place the rigid object (object1) in the box.
    # 3. Ensure all objects are in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object4

    # Action Sequence
    # Place soft object first
    robot.place(object0, box)
    # Place rigid object
    robot.place(object1, box)
    # Ensure all objects are in the box
    robot.place(object2, box)
    robot.place(object3, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. Placing the soft object (object0) first satisfies the rule: "Before place a fragile or rigid object, soft object should be in the box if there is any soft objects."
    # 2. Placing the rigid object (object1) after the soft object satisfies the same rule.
    # 3. Placing the remaining objects (object2 and object3) ensures all objects are in the box.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_bin_objects == [0, 1, 2, 3]
    
    print("All task planning is done")
