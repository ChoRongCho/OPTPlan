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
    is_foldable: bool
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
object0 = Object(index=0, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_soft=False, is_rigid=False, is_elastic=True, in_box=False, out_box=True)
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_soft=True, is_rigid=False, is_elastic=True, in_box=False, out_box=True)
object2 = Object(index=2, name='translucent_2D_circle', color='translucent', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=True, is_soft=False, is_rigid=True, is_elastic=False, in_box=False, out_box=True)
object3 = Object(index=3, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_soft=False, is_rigid=True, is_elastic=False, in_box=True, out_box=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_soft=False, is_rigid=False, is_elastic=False, in_box=True, out_box=False)

### 3. Notes:
# The table and Python code represent the initial state of the objects and their properties for the bin_packing task.
# The 'in_bin_objects' list is empty for all objects initially, indicating no objects are inside any bin.
# The 'pushed' and 'folded' properties are set to False for all objects as initial states.
# The 'in_box' and 'out_box' properties are mutually exclusive and indicate the initial position of the objects.

---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    object0 = Object(index=0, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_soft=False, is_rigid=False, is_elastic=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_soft=True, is_rigid=False, is_elastic=True, in_box=False, out_box=True)
    object2 = Object(index=2, name='translucent_2D_circle', color='translucent', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=True, is_soft=False, is_rigid=True, is_elastic=False, in_box=False, out_box=True)
    object3 = Object(index=3, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_soft=False, is_rigid=True, is_elastic=False, in_box=True, out_box=False)
    object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_soft=False, is_rigid=False, is_elastic=False, in_box=True, out_box=False)

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
    # 1. Place the soft object (object1) in the box first.
    # 2. Place the foldable object (object2) in the box.
    # 3. Place the rigid object (object0) in the box.
    # 4. Place the already in-box object (object3) in the box.
    # 5. Push the soft object (object1) if needed.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object4

    # c) Action sequence
    # Place the soft object (object1) in the box
    robot.place(object1, box)
    # Place the foldable object (object2) in the box
    robot.place(object2, box)
    # Place the rigid object (object0) in the box
    robot.place(object0, box)
    # Place the already in-box object (object3) in the box
    robot.place(object3, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. Placed the soft object (object1) first as per the rule.
    # 2. Placed the foldable object (object2) next.
    # 3. Placed the rigid object (object0) after the soft object.
    # 4. Placed the already in-box object (object3) last.
    # 5. No need to push the soft object (object1) as it is already in the box.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_bin_objects == [0, 1, 2, 3]

    print("All task planning is done")
