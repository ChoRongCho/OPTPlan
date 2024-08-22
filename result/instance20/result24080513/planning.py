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
    in_box: bool
    out_box: bool




    def dummy(self):
        pass


 # Object Initial State
code
# don't include the object classes or robot class, make only objects and bin 
# example 
object0 = Object(index=0, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_elastic=True, in_box=False, out_box=True)
object1 = Object(index=1, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_elastic=True, in_box=False, out_box=True)
object2 = Object(index=2, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_elastic=True, in_box=False, out_box=True)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=False, in_box=True, out_box=False)

### 3. Notes:
# The initial state table and Python code represent the initial conditions of the objects and the box in the bin_packing task.
# The 'pushed' and 'folded' attributes are set to False for all objects as there is no information indicating otherwise.
# The 'in_bin_objects' list is empty for all objects and the box initially.
# The 'in_box' and 'out_box' attributes are set based on the 'init_pose' provided in the input data.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    object0 = Object(index=0, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_elastic=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_elastic=True, in_box=False, out_box=True)
    object2 = Object(index=2, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_elastic=True, in_box=False, out_box=True)
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
    # 1. Place soft objects first if there are any soft objects.
    # 2. Fold objects only if they are foldable.
    # 3. Only push soft objects after placing items in the bin.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # Action sequence
    # 1. Place white_3D_cylinder (soft object) in the box
    robot.place(object0, box)
    object0.in_box = True
    object0.out_box = False
    box.in_bin_objects.append(object0.index)

    # 2. Place yellow_3D_cuboid (soft object) in the box
    robot.place(object1, box)
    object1.in_box = True
    object1.out_box = False
    box.in_bin_objects.append(object1.index)

    # 3. Place brown_3D_cuboid (soft object) in the box
    robot.place(object2, box)
    object2.in_box = True
    object2.out_box = False
    box.in_bin_objects.append(object2.index)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - Placed all soft objects first as per the rule.
    # - No foldable objects in this scenario.
    # - No need to push any objects as all are placed in the box.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert box.in_bin_objects == [0, 1, 2]

    print("All task planning is done")
