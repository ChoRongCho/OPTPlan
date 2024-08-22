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
    is_foldable: bool
    is_soft: bool
    is_elastic: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    init_pose: str
    in_box: bool




    def dummy(self):
        pass


 # Object Initial State
code
# don't include the object classes or robot class, make only objects and bin 
# example 
object0 = Object(index=0, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_foldable=True, is_soft=False, is_elastic=False, init_pose='out_box', in_box=False)
object1 = Object(index=1, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_foldable=False, is_soft=True, is_elastic=True, init_pose='out_box', in_box=False)
object2 = Object(index=2, name='blue_1D_loop', color='blue', shape='1D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_foldable=True, is_soft=False, is_elastic=False, init_pose='out_box', in_box=False)
object3 = Object(index=3, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_foldable=False, is_soft=True, is_elastic=False, init_pose='in_box', in_box=True)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_foldable=False, is_soft=False, is_elastic=False, init_pose='box', in_box=False)

### 3. Notes:
# The table and the Python code represent the initial state of the bin_packing domain.
# The 'in_bin_objects' list is empty for all objects initially.
# The 'pushed' and 'folded' predicates are set to False for all objects initially.
# The 'init_pose' and 'in_box' fields are set according to the given input data.
# The 'object_type' field differentiates between 'obj' and 'box'.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    object0 = Object(index=0, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_foldable=True, is_soft=False, is_elastic=False, init_pose='out_box', in_box=False)
    object1 = Object(index=1, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_foldable=False, is_soft=True, is_elastic=True, init_pose='out_box', in_box=False)
    object2 = Object(index=2, name='blue_1D_loop', color='blue', shape='1D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_foldable=True, is_soft=False, is_elastic=False, init_pose='out_box', in_box=False)
    object3 = Object(index=3, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_foldable=False, is_soft=True, is_elastic=False, init_pose='in_box', in_box=True)
    object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_foldable=False, is_soft=False, is_elastic=False, init_pose='box', in_box=False)

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
    box = object4

    # Action sequence
    # 1. Place the soft object (brown_3D_cuboid) in the box first
    robot.pick(object1)
    robot.place(object1, box)
    
    # 2. Place the fragile object (blue_1D_loop) in the box
    robot.pick(object2)
    robot.place(object2, box)
    
    # 3. Place the foldable object (yellow_2D_rectangle) in the box
    robot.pick(object0)
    robot.place(object0, box)
    
    # 4. Push the soft object (red_3D_polyhedron) in the box
    robot.push(object3, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - The brown_3D_cuboid is placed first because it is a soft object.
    # - The blue_1D_loop is placed next because it is a fragile object and the soft object is already in the box.
    # - The yellow_2D_rectangle is placed next because it is foldable and needs to be in the box.
    # - The red_3D_polyhedron is pushed into the box because it is a soft object and all other objects are already in the box.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    
    print("All task planning is done")
