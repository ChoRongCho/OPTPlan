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
object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=False, is_rigid=True, in_box=False, out_box=True)
object1 = Object(index=1, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=True, is_rigid=False, in_box=False, out_box=True)
object2 = Object(index=2, name='blue_2D_loop', color='blue', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=False, is_rigid=False, in_box=False, out_box=True)
object3 = Object(index=3, name='black_2D_circle', color='black', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=True, is_elastic=False, is_rigid=True, in_box=True, out_box=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=False, is_rigid=False, in_box=True, out_box=False)

### 3. Notes:
# The table and Python code represent the initial state of the bin_packing domain.
# The 'in_bin_objects' list is empty for all objects initially.
# The 'pushed' and 'folded' attributes are set to False for all objects initially.
# The 'in_box' and 'out_box' attributes are mutually exclusive and represent the initial position of the objects.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=False, is_rigid=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=True, is_rigid=False, in_box=False, out_box=True)
    object2 = Object(index=2, name='blue_2D_loop', color='blue', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=False, is_rigid=False, in_box=False, out_box=True)
    object3 = Object(index=3, name='black_2D_circle', color='black', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=True, is_elastic=False, is_rigid=True, in_box=True, out_box=False)
    object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=False, is_rigid=False, in_box=True, out_box=False)

    # Goal state
    goal_state = {
        0: {'in_box': True, 'out_box': False},
        1: {'in_box': True, 'out_box': False},
        2: {'in_box': True, 'out_box': False},
        3: {'in_box': True, 'out_box': False},
        4: {'in_box': True, 'out_box': False, 'in_bin_objects': [0, 1, 2, 3]}
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold the black_2D_circle (object3) since it is foldable.
    # 2. Place the white_2D_loop (object1) in the box since it is soft.
    # 3. Place the yellow_3D_cylinder (object0) in the box.
    # 4. Place the blue_2D_loop (object2) in the box.
    # 5. Place the black_2D_circle (object3) in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object4

    # c) Perform actions
    robot.fold(object3)  # Fold the black_2D_circle
    robot.place(object1, box)  # Place the white_2D_loop in the box
    robot.place(object0, box)  # Place the yellow_3D_cylinder in the box
    robot.place(object2, box)  # Place the blue_2D_loop in the box
    robot.place(object3, box)  # Place the black_2D_circle in the box

    # Fourth, after making all actions, fill your reasons according to the rules
    # 1. Folded the black_2D_circle because it is foldable.
    # 2. Placed the white_2D_loop first because it is a soft object.
    # 3. Placed the yellow_3D_cylinder next because it is a rigid object.
    # 4. Placed the blue_2D_loop next because it is neither soft nor rigid.
    # 5. Placed the black_2D_circle last because it is a rigid object and was folded.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_bin_objects == [0, 1, 2, 3]

    print("All task planning is done")
