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
    is_foldable: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool




    def dummy(self):
        pass


 # Object Initial State
code
# don't include the object classes or robot class, make only objects and bin 
# example 
object0 = Object(index=0, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=True, is_foldable=False, in_box=False, out_box=True)
object1 = Object(index=1, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=True, is_foldable=True, in_box=False, out_box=True)
object2 = Object(index=2, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=False, is_foldable=True, in_box=False, out_box=True)
object3 = Object(index=3, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_elastic=True, is_foldable=False, in_box=False, out_box=True)
object4 = Object(index=4, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=True, is_foldable=False, in_box=False, out_box=True)
object5 = Object(index=5, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=False, is_foldable=False, in_box=True, out_box=False)

### 3. Notes:
# The initial state table and Python code represent the initial conditions of the objects and the bin for the bin_packing task.
# The 'in_bin_objects' list is empty for all objects initially, indicating that no objects are in the bin at the start.
# The 'pushed' and 'folded' predicates are set to False for all objects initially.
# The 'in_box' and 'out_box' predicates are mutually exclusive and indicate whether an object is inside or outside the bin.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    object0 = Object(index=0, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=True, is_foldable=False, in_box=False, out_box=True)
    object1 = Object(index=1, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=True, is_foldable=True, in_box=False, out_box=True)
    object2 = Object(index=2, name='white_3D_cuboid', color='white', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=False, is_foldable=True, in_box=False, out_box=True)
    object3 = Object(index=3, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_elastic=True, is_foldable=False, in_box=False, out_box=True)
    object4 = Object(index=4, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=True, is_foldable=False, in_box=False, out_box=True)
    object5 = Object(index=5, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_elastic=False, is_foldable=False, in_box=True, out_box=False)

    # Goal state
    goal_state = {
        0: {'in_box': True, 'out_box': False},
        1: {'in_box': True, 'out_box': False},
        2: {'in_box': True, 'out_box': False},
        3: {'in_box': True, 'out_box': False},
        4: {'in_box': True, 'out_box': False},
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place the soft object (object3) in the box first.
    # 2. Fold foldable objects (object1 and object2).
    # 3. Place the remaining objects in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object5

    # Action sequence
    # 1. Place the soft object (object3) in the box
    robot.place(object3, box)
    object3.in_box = True
    object3.out_box = False
    box.in_bin_objects.append(object3.index)

    # 2. Fold foldable objects (object1 and object2)
    robot.fold(object1)
    object1.folded = True

    robot.fold(object2)
    object2.folded = True

    # 3. Place the remaining objects in the box
    robot.place(object0, box)
    object0.in_box = True
    object0.out_box = False
    box.in_bin_objects.append(object0.index)

    robot.place(object1, box)
    object1.in_box = True
    object1.out_box = False
    box.in_bin_objects.append(object1.index)

    robot.place(object2, box)
    object2.in_box = True
    object2.out_box = False
    box.in_bin_objects.append(object2.index)

    robot.place(object4, box)
    object4.in_box = True
    object4.out_box = False
    box.in_bin_objects.append(object4.index)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasons:
    # - Placed the soft object (object3) first as per the rule.
    # - Folded foldable objects (object1 and object2) before placing them in the box.
    # - Placed all objects in the box to achieve the goal state.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_box == True

    print("All task planning is done")
