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
    is_rigid: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    init_pose: str
    in_box: bool




    def dummy(self):
        pass


 # Object Initial State
code
# don't include the object classes or robot class, make only objects and bin 
# example 
object0 = Object(index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=True, is_rigid=False, init_pose='out_box', in_box=False)
object1 = Object(index=1, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_soft=False, is_rigid=True, init_pose='out_box', in_box=False)
object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=False, is_rigid=False, init_pose='box', in_box=True)

### 3. Notes:
# The table and the Python code represent the initial state of the bin_packing domain.
# The 'in_bin_objects' list is empty for all objects initially.
# The 'init_pose' indicates the initial position of the objects.
# The 'in_box' boolean indicates whether the object is initially in the box or not.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    object0 = Object(index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=True, is_rigid=False, init_pose='out_box', in_box=False)
    object1 = Object(index=1, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_soft=False, is_rigid=True, init_pose='out_box', in_box=False)
    object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=False, is_rigid=False, init_pose='box', in_box=True)

    # Goal state
    goal_object0 = Object(index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=True, is_rigid=False, init_pose='in_box', in_box=True)
    goal_object1 = Object(index=1, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_soft=False, is_rigid=True, init_pose='in_box', in_box=True)
    goal_object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[0, 1], is_fragile=False, is_soft=False, is_rigid=False, init_pose='box', in_box=True)

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place the soft object (object0) in the box first.
    # 2. Place the fragile and rigid object (object1) in the box.
    # 3. Update the box's in_bin_objects list to include both objects.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object2

    # c) Action sequence
    # Place the soft object in the box
    robot.pick(object0)
    robot.place(object0, box)
    object0.in_box = True
    object0.init_pose = 'in_box'
    box.in_bin_objects.append(object0.index)

    # Place the fragile and rigid object in the box
    robot.pick(object1)
    robot.place(object1, box)
    object1.in_box = True
    object1.init_pose = 'in_box'
    box.in_bin_objects.append(object1.index)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. The soft object (object0) is placed in the box first to satisfy the rule that soft objects should be placed before fragile or rigid objects.
    # 2. The fragile and rigid object (object1) is placed in the box after the soft object.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_bin_objects == [0, 1]

    print("All task planning is done")
