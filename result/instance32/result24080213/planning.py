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
object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_fragile=False, is_elastic=False, is_rigid=True, in_box=False, out_box=True)
object1 = Object(index=1, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_fragile=True, is_elastic=False, is_rigid=False, in_box=False, out_box=True)
object2 = Object(index=2, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_fragile=False, is_elastic=True, is_rigid=False, in_box=False, out_box=True)
object3 = Object(index=3, name='green_3D_sphere', color='green', shape='3D_sphere', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_fragile=False, is_elastic=False, is_rigid=False, in_box=True, out_box=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[3], is_soft=False, is_fragile=False, is_elastic=False, is_rigid=False, in_box=True, out_box=False)

### 3. Notes:
# The table and Python code represent the initial state of the bin_packing domain.
# Each object has been initialized with its properties and predicates based on the given input.
# The 'in_bin_objects' list for the box contains the index of the object that is inside the box.
# The 'in_box' and 'out_box' predicates indicate the initial position of each object.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_fragile=False, is_elastic=False, is_rigid=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_fragile=True, is_elastic=False, is_rigid=False, in_box=False, out_box=True)
    object2 = Object(index=2, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_fragile=False, is_elastic=True, is_rigid=False, in_box=False, out_box=True)
    object3 = Object(index=3, name='green_3D_sphere', color='green', shape='3D_sphere', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_fragile=False, is_elastic=False, is_rigid=False, in_box=True, out_box=False)
    object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[3], is_soft=False, is_fragile=False, is_elastic=False, is_rigid=False, in_box=True, out_box=False)

    # Goal state
    goal_state = {
        0: {'in_box': True, 'out_box': False},
        1: {'in_box': True, 'out_box': False},
        2: {'in_box': True, 'out_box': False},
        3: {'in_box': True, 'out_box': False},
        4: {'in_bin_objects': [0, 1, 2, 3]}
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Rules:
    # 1. Place soft objects in the box first if there are any.
    # 2. Place fragile or rigid objects after soft objects.
    # 3. Fold objects only if they are foldable.
    # 4. Only push soft objects after placing items in the bin.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object4

    # c) Action sequence
    # Place the soft object (object3) first
    robot.place(object3, box)

    # Place the rigid object (object0)
    robot.place(object0, box)

    # Place the fragile object (object1)
    robot.place(object1, box)

    # Place the elastic object (object2)
    robot.place(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. Placed the soft object (object3) first as per the rule.
    # 2. Placed the rigid object (object0) next.
    # 3. Placed the fragile object (object1) after the soft object.
    # 4. Placed the elastic object (object2) last.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_bin_objects == [0, 1, 2, 3]

    print("All task planning is done")