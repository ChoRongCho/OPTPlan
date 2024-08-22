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
object0 = Object(index=0, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_soft=False, is_elastic=False, is_rigid=True, in_box=False, out_box=True)
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=True, is_elastic=True, is_rigid=False, in_box=False, out_box=True)
object2 = Object(index=2, name='yellow_2D_triangle', color='yellow', shape='2D_triangle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=True, is_elastic=True, is_rigid=False, in_box=True, out_box=False)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=False, is_elastic=False, is_rigid=False, in_box=True, out_box=False)

### 3. Notes:
# The table and Python code represent the initial state of the bin_packing domain.
# The 'in_bin_objects' list is empty for all objects as no objects are inside any bin initially.
# The 'pushed' and 'folded' predicates are set to False for all objects as no actions have been performed yet.
# The 'in_box' and 'out_box' predicates are set according to the initial positions provided in the input.

---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    object0 = Object(index=0, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_soft=False, is_elastic=False, is_rigid=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=True, is_elastic=True, is_rigid=False, in_box=False, out_box=True)
    object2 = Object(index=2, name='yellow_2D_triangle', color='yellow', shape='2D_triangle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=True, is_elastic=True, is_rigid=False, in_box=True, out_box=False)
    object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=False, is_elastic=False, is_rigid=False, in_box=True, out_box=False)

    # Goal state
    goal_object0_in_box = True
    goal_object1_in_box = True
    goal_object2_in_box = True
    goal_object3_in_bin_objects = [0, 1, 2]

    # Second, using given rules and object's states, make a task planning strategy
    # Rules:
    # 1. Place: Before placing a fragile or rigid object, a soft object should be in the box if there is any soft object.
    # 2. Pick: None
    # 3. Fold: Fold objects only if they are foldable.
    # 4. Push: Only push soft objects after placing items in the bin.
    # 5. Out: None

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # Action sequence
    # 1. Place the soft object (object1) in the box first
    robot.pick(object1)
    robot.place(object1, box)

    # 2. Place the fragile object (object0) in the box
    robot.pick(object0)
    robot.place(object0, box)

    # 3. Place the already in-box object (object2) in the box (no action needed as it's already in the box)

    # 4. Update the box's in_bin_objects list
    box.in_bin_objects = [object0.index, object1.index, object2.index]

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - Placed the soft object (object1) first to satisfy the rule that soft objects should be placed before fragile or rigid objects.
    # - Placed the fragile object (object0) after the soft object.
    # - No need to place object2 as it is already in the box.
    # - Updated the box's in_bin_objects list to reflect the final state.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == goal_object0_in_box
    assert object1.in_box == goal_object1_in_box
    assert object2.in_box == goal_object2_in_box
    assert box.in_bin_objects == goal_object3_in_bin_objects

    print("All task planning is done")
