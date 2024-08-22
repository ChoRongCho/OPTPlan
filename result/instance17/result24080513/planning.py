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
object0 = Object(index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_rigid=False, is_elastic=True, in_box=False, out_box=True)
object1 = Object(index=1, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_rigid=True, is_elastic=False, in_box=False, out_box=True)
object2 = Object(index=2, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_rigid=False, is_elastic=True, in_box=False, out_box=True)
object3 = Object(index=3, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_rigid=False, is_elastic=True, in_box=True, out_box=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_rigid=False, is_elastic=False, in_box=True, out_box=False)

### 3. Notes:
# The table and the Python code represent the initial state of the bin_packing domain.
# The 'in_bin_objects' list is empty for all objects initially.
# The 'pushed' and 'folded' predicates are set to False for all objects.
# The 'in_box' and 'out_box' predicates are mutually exclusive and set according to the initial pose.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    initial_state = {
        0: Object(index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_rigid=False, is_elastic=True, in_box=False, out_box=True),
        1: Object(index=1, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_rigid=True, is_elastic=False, in_box=False, out_box=True),
        2: Object(index=2, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_rigid=False, is_elastic=True, in_box=False, out_box=True),
        3: Object(index=3, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_rigid=False, is_elastic=True, in_box=True, out_box=False),
        4: Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_rigid=False, is_elastic=False, in_box=True, out_box=False)
    }

    goal_state = {
        0: Object(index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_rigid=False, is_elastic=True, in_box=True, out_box=False),
        1: Object(index=1, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_rigid=True, is_elastic=False, in_box=True, out_box=False),
        2: Object(index=2, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_rigid=False, is_elastic=True, in_box=True, out_box=False),
        3: Object(index=3, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_rigid=False, is_elastic=True, in_box=True, out_box=False),
        4: Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[0, 1, 2, 3], is_soft=False, is_rigid=False, is_elastic=False, in_box=True, out_box=False)
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Rules:
    # 1. Place soft object first if there is any soft object.
    # 2. Fold objects only if they are foldable.
    # 3. Only push soft objects after placing items in the bin.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = initial_state[4]

    # Action sequence
    # 1. Place the soft object (object0) in the box
    robot.place(initial_state[0], box)
    # 2. Place the rigid object (object1) in the box
    robot.place(initial_state[1], box)
    # 3. Place the elastic object (object2) in the box
    robot.place(initial_state[2], box)
    # 4. Ensure the already in-box object (object3) remains in the box
    # 5. Push the soft object (object0) to ensure it is properly placed
    robot.push(initial_state[0], box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - Placed the soft object first as per the rule.
    # - Placed the rigid object next.
    # - Placed the elastic object after the rigid object.
    # - Pushed the soft object after placing all items in the bin.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert initial_state[0].in_box == True
    assert initial_state[1].in_box == True
    assert initial_state[2].in_box == True
    assert initial_state[3].in_box == True
    assert initial_state[4].in_bin_objects == [0, 1, 2, 3]

    print("All task planning is done")
