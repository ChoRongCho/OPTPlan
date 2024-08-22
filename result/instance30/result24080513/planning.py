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
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool




    def dummy(self):
        pass


 # Object Initial State
code
# don't include the object classes or robot class, make only objects and bin 
# example 
object0 = Object(index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_soft=True, in_box=False, out_box=True)
object1 = Object(index=1, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=True, is_soft=False, in_box=False, out_box=True)
object2 = Object(index=2, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=True, is_soft=False, in_box=True, out_box=False)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_soft=False, in_box=True, out_box=False)

### 3. Notes:
# The 'pushed' and 'folded' attributes are initialized to False as there is no information provided about these states.
# The 'in_bin_objects' list is empty for all objects as there is no information about objects being inside other objects.
# The 'is_foldable' and 'is_soft' attributes are set based on the predicates provided.
# The 'in_box' and 'out_box' attributes are set based on the 'init_pose' provided.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    object0 = Object(index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_soft=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=True, is_soft=False, in_box=False, out_box=True)
    object2 = Object(index=2, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=True, is_soft=False, in_box=True, out_box=False)
    object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_soft=False, in_box=True, out_box=False)

    # Goal state
    goal_object0 = Object(index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_soft=True, in_box=True, out_box=False)
    goal_object1 = Object(index=1, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', pushed=False, folded=True, in_bin_objects=[], is_foldable=True, is_soft=False, in_box=True, out_box=False)
    goal_object2 = Object(index=2, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', pushed=False, folded=True, in_bin_objects=[], is_foldable=True, is_soft=False, in_box=True, out_box=False)
    goal_object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[0, 1, 2], is_foldable=False, is_soft=False, in_box=True, out_box=False)

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place the soft object (object0) in the box first.
    # 2. Fold the foldable objects (object1 and object2).
    # 3. Place the folded objects (object1 and object2) in the box.
    # 4. Place the soft object (object0) in the box.
    # 5. Place all objects inside the white box (object3).

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # Action sequence
    # 1. Place the soft object (object0) in the box
    robot.place(object0, box)
    object0.in_box = True
    object0.out_box = False

    # 2. Fold the foldable objects (object1 and object2)
    robot.fold(object1)
    object1.folded = True

    robot.fold(object2)
    object2.folded = True

    # 3. Place the folded objects (object1 and object2) in the box
    robot.place(object1, box)
    object1.in_box = True
    object1.out_box = False

    robot.place(object2, box)
    object2.in_box = True
    object2.out_box = False

    # 4. Place the soft object (object0) in the box
    robot.place(object0, box)
    object0.in_box = True
    object0.out_box = False

    # 5. Place all objects inside the white box (object3)
    box.in_bin_objects.extend([object0.index, object1.index, object2.index])

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - The soft object (object0) is placed in the box first as per the rule.
    # - The foldable objects (object1 and object2) are folded before placing them in the box.
    # - All objects are placed inside the white box (object3) as per the goal state.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object1.folded == True
    assert object2.folded == True
    assert box.in_bin_objects == [0, 1, 2]

    print("All task planning is done")
