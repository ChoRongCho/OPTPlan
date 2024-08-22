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
    is_fragile: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool




    def dummy(self):
        pass


 # Object Initial State
code
# don't include the object classes or robot class, make only objects and bin 
# example 
object0 = Object(index=0, name='transparent_3D_cuboid', color='transparent', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=True, is_elastic=True, is_rigid=False, is_fragile=False, in_box=False, out_box=True)
object1 = Object(index=1, name='black_2D_circle', color='black', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=False, is_rigid=True, is_fragile=False, in_box=False, out_box=True)
object2 = Object(index=2, name='blue_1D_loop', color='blue', shape='1D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=True, is_elastic=False, is_rigid=False, is_fragile=True, in_box=False, out_box=True)
object3 = Object(index=3, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=True, is_elastic=False, is_rigid=False, is_fragile=False, in_box=True, out_box=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=False, is_rigid=False, is_fragile=False, in_box=True, out_box=False)

### 3. Notes:
# The table and the Python code represent the initial state of the bin_packing domain.
# Each object is defined with its properties and initial state.
# The 'in_bin_objects' list is empty for all objects initially.
# The 'in_box' and 'out_box' flags are set according to the initial positions provided in the input.

---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    object0 = Object(index=0, name='transparent_3D_cuboid', color='transparent', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=True, is_elastic=True, is_rigid=False, is_fragile=False, in_box=False, out_box=True)
    object1 = Object(index=1, name='black_2D_circle', color='black', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=False, is_rigid=True, is_fragile=False, in_box=False, out_box=True)
    object2 = Object(index=2, name='blue_1D_loop', color='blue', shape='1D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=True, is_elastic=False, is_rigid=False, is_fragile=True, in_box=False, out_box=True)
    object3 = Object(index=3, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=True, is_elastic=False, is_rigid=False, is_fragile=False, in_box=True, out_box=False)
    object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=False, is_rigid=False, is_fragile=False, in_box=True, out_box=False)

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold the foldable objects if necessary.
    # 2. Place the soft objects (non-rigid, non-fragile) first.
    # 3. Place the fragile objects next.
    # 4. Place the rigid objects last.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object4

    # Action sequence
    # 1. Fold the transparent_3D_cuboid (object0) since it is foldable
    robot.fold(object0)
    
    # 2. Place the yellow_2D_rectangle (object3) in the box (already in the box)
    # No action needed as it is already in the box

    # 3. Place the transparent_3D_cuboid (object0) in the box
    robot.place(object0, box)

    # 4. Place the blue_1D_loop (object2) in the box
    robot.place(object2, box)

    # 5. Place the black_2D_circle (object1) in the box
    robot.place(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # - Folded object0 because it is foldable.
    # - Placed object3 first because it is already in the box.
    # - Placed object0 next because it is soft (non-rigid, non-fragile).
    # - Placed object2 next because it is fragile.
    # - Placed object1 last because it is rigid.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_box == True  # The box itself should be in the box

    print("All task planning is done")
