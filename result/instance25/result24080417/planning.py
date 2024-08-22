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
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_elastic=True, init_pose='out_box', in_box=False)
object1 = Object(index=1, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=True, init_pose='out_box', in_box=False)
object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=False, init_pose='box', in_box=True)

### 3. Notes:
# The table and the Python code represent the initial state of the objects for the bin_packing task.
# The 'in_bin_objects' list is empty for all objects initially.
# The 'pushed' and 'folded' predicates are set to False for all objects initially.
# The 'init_pose' and 'in_box' fields are set according to the initial positions of the objects.
# The 'is_soft' and 'is_elastic' properties are set based on the given predicates.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_elastic=True, init_pose='out_box', in_box=False)
    object1 = Object(index=1, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=True, init_pose='out_box', in_box=False)
    object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=False, init_pose='box', in_box=True)

    # Goal state
    goal_object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_elastic=True, init_pose='in_box', in_box=True)
    goal_object1 = Object(index=1, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=True, init_pose='in_box', in_box=True)
    goal_object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[0, 1], is_soft=False, is_elastic=False, init_pose='box', in_box=True)

    # Second, using given rules and object's states, make a task planning strategy
    # According to the rules:
    # 1. Place the soft object (object0) first.
    # 2. Place the rigid object (object1) next.
    # 3. Ensure both objects are in the box (object2).

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object2

    # c) Action sequence
    # Place the soft object (object0) in the box
    robot.pick(object0)
    robot.place(object0, box)

    # Place the rigid object (object1) in the box
    robot.pick(object1)
    robot.place(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. The soft object (object0) is placed first as per the rule: "Before placing a fragile or rigid object, a soft object should be in the box if there are any soft objects."
    # 2. The rigid object (object1) is placed next.
    # 3. Both objects are placed in the box (object2).

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_bin_objects == [0, 1]

    print("All task planning is done")
