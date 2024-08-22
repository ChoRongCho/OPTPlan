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
    
    # Pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool




    def dummy(self):
        pass


 # Object Initial State
code
# don't include the object classes or robot class, make only objects and bin 
# example 
object0 = Object(index=0, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_elastic=True, in_box=False, out_box=True)
object1 = Object(index=1, name='transparent_3D_cuboid', color='transparent', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=True, in_box=False, out_box=True)
object2 = Object(index=2, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=True, in_box=False, out_box=True)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=False, in_box=True, out_box=False)

### 3. Notes:
# The initial state is defined based on the input images and the properties of each object.
# The 'in_bin_objects' list is empty for all objects initially.
# The 'pushed' and 'folded' properties are set to False for all objects initially.
# The 'in_box' and 'out_box' properties are mutually exclusive and set according to the 'init_pose' from the input.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    object0 = Object(index=0, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_elastic=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='transparent_3D_cuboid', color='transparent', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=True, in_box=False, out_box=True)
    object2 = Object(index=2, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=True, in_box=False, out_box=True)
    object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=False, in_box=True, out_box=False)

    # Goal state
    goal_state = {
        0: {'in_box': True, 'out_box': False},
        1: {'in_box': True, 'out_box': False},
        2: {'in_box': True, 'out_box': False},
        3: {'in_bin_objects': [0, 1, 2]}
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
    box = object3

    # Action sequence
    # 1. Place the soft object (object0) in the box
    robot.pick(object0)
    robot.place(object0, box)
    object0.in_box = True
    object0.out_box = False
    box.in_bin_objects.append(object0.index)

    # 2. Place the rigid object (object1) in the box
    robot.pick(object1)
    robot.place(object1, box)
    object1.in_box = True
    object1.out_box = False
    box.in_bin_objects.append(object1.index)

    # 3. Place the rigid object (object2) in the box
    robot.pick(object2)
    robot.place(object2, box)
    object2.in_box = True
    object2.out_box = False
    box.in_bin_objects.append(object2.index)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - Placed the soft object (object0) first as per the rule.
    # - Placed the rigid objects (object1 and object2) after the soft object.
    # - No foldable objects in this scenario.
    # - No push action required as all objects are placed in the box.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert box.in_bin_objects == [0, 1, 2]

    print("All task planning is done")
