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
object0 = Object(index=0, name='black_2D_circle', color='black', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=False, is_rigid=True, in_box=False, out_box=True)
object1 = Object(index=1, name='blue_1D_loop', color='blue', shape='1D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=False, is_rigid=True, in_box=False, out_box=True)
object2 = Object(index=2, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=True, is_rigid=False, in_box=False, out_box=True)
object3 = Object(index=3, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=True, is_elastic=False, is_rigid=False, in_box=True, out_box=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=False, is_rigid=False, in_box=True, out_box=False)

### 3. Notes:
# The table and Python code represent the initial state of the bin_packing domain.
# Each object has been initialized with its properties and predicates.
# The 'in_bin_objects' list is empty for all objects initially.
# The 'pushed' and 'folded' properties are set to False for all objects.
# The 'in_box' and 'out_box' properties are set according to the initial positions provided.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    object0 = Object(index=0, name='black_2D_circle', color='black', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=False, is_rigid=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='blue_1D_loop', color='blue', shape='1D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=False, is_rigid=True, in_box=False, out_box=True)
    object2 = Object(index=2, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=True, is_rigid=False, in_box=False, out_box=True)
    object3 = Object(index=3, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=True, is_elastic=False, is_rigid=False, in_box=True, out_box=False)
    object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=False, is_rigid=False, in_box=True, out_box=False)

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold the yellow_2D_rectangle since it is foldable.
    # 2. Place the transparent_3D_cylinder (soft object) in the box first.
    # 3. Place the black_2D_circle and blue_1D_loop (rigid objects) in the box.
    # 4. Push the yellow_2D_rectangle into the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object4

    # Action sequence
    robot.fold(object3)  # Fold yellow_2D_rectangle
    robot.place(object2, box)  # Place transparent_3D_cylinder in the box
    robot.place(object0, box)  # Place black_2D_circle in the box
    robot.place(object1, box)  # Place blue_1D_loop in the box
    robot.push(object3, box)  # Push yellow_2D_rectangle into the box

    # Fourth, after making all actions, fill your reasons according to the rules
    # 1. Fold yellow_2D_rectangle because it is foldable.
    # 2. Place transparent_3D_cylinder first because it is a soft object.
    # 3. Place black_2D_circle and blue_1D_loop after the soft object.
    # 4. Push yellow_2D_rectangle into the box after placing other items.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_bin_objects == [0, 1, 2, 3]
    
    print("All task planning is done")
