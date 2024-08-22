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
object0 = Object(index=0, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_fragile=False, is_elastic=True, in_box=False, out_box=True)
object1 = Object(index=1, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_fragile=True, is_elastic=False, in_box=False, out_box=True)
object2 = Object(index=2, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_fragile=False, is_elastic=True, in_box=True, out_box=False)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_fragile=False, is_elastic=False, in_box=False, out_box=False)

### 3. Notes:
# The table and Python code represent the initial state of the bin_packing domain.
# The 'object_type' field differentiates between objects and boxes.
# The 'in_bin_objects' list is empty for all objects initially.
# The 'pushed' and 'folded' predicates are set to False for all objects initially.
# The 'in_box' and 'out_box' fields are set based on the 'init_pose' from the input data.

---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    object0 = Object(index=0, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_fragile=False, is_elastic=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_fragile=True, is_elastic=False, in_box=False, out_box=True)
    object2 = Object(index=2, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_fragile=False, is_elastic=True, in_box=True, out_box=False)
    object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_fragile=False, is_elastic=False, in_box=False, out_box=False)

    # Goal state
    goal_state = {
        0: {'in_box': True, 'out_box': False},
        1: {'in_box': True, 'out_box': False},
        2: {'in_box': True, 'out_box': False},
        3: {'in_box': False, 'out_box': False}  # Box itself doesn't change
    }

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

    # c) Action sequence
    # Since object2 (yellow_3D_cuboid) is already in the box, we can proceed with placing other objects.

    # Place white_2D_loop (object0) in the box
    robot.place(object0, box)
    object0.in_box = True
    object0.out_box = False

    # Place black_2D_loop (object1) in the box
    robot.place(object1, box)
    object1.in_box = True
    object1.out_box = False

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. The yellow_3D_cuboid (object2) is already in the box, satisfying the rule that a soft object should be in the box before placing fragile or rigid objects.
    # 2. The white_2D_loop (object0) and black_2D_loop (object1) are placed in the box following the rules.
    # 3. No folding or pushing actions are required as per the current state and goal.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == False  # Box itself doesn't change

    print("All task planning is done")
