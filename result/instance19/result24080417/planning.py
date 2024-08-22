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
    is_rigid: bool
    is_elastic: bool
    is_foldable: bool
    is_soft: bool
    is_fragile: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='yellow_3D_cylinder', 
    color='yellow', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=True, 
    is_elastic=False, 
    is_foldable=False, 
    is_soft=False, 
    is_fragile=False, 
    in_box=False, 
    out_box=True
)

object1 = Object(
    index=1, 
    name='brown_3D_cuboid', 
    color='brown', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=False, 
    is_elastic=True, 
    is_foldable=False, 
    is_soft=True, 
    is_fragile=False, 
    in_box=False, 
    out_box=True
)

object2 = Object(
    index=2, 
    name='green_3D_cylinder', 
    color='green', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=True, 
    is_elastic=False, 
    is_foldable=False, 
    is_soft=False, 
    is_fragile=True, 
    in_box=False, 
    out_box=True
)

object3 = Object(
    index=3, 
    name='black_2D_circle', 
    color='black', 
    shape='2D_circle', 
    object_type='obj', 
    pushed=False, 
    folded=True, 
    in_bin_objects=[], 
    is_rigid=False, 
    is_elastic=False, 
    is_foldable=True, 
    is_soft=False, 
    is_fragile=False, 
    in_box=True, 
    out_box=False
)

object4 = Object(
    index=4, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=False, 
    is_elastic=False, 
    is_foldable=False, 
    is_soft=False, 
    is_fragile=False, 
    in_box=True, 
    out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    initial_state = {
        0: {'in_box': False, 'out_box': True},
        1: {'in_box': False, 'out_box': True},
        2: {'in_box': False, 'out_box': True},
        3: {'in_box': True, 'out_box': False},
        4: {'in_box': True, 'out_box': False}
    }
    
    goal_state = {
        0: {'in_box': True, 'out_box': False},
        1: {'in_box': True, 'out_box': False},
        2: {'in_box': True, 'out_box': False},
        3: {'in_box': True, 'out_box': False},
        4: {'in_box': True, 'out_box': False}
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Rules:
    # 1. Place soft object before placing fragile or rigid objects.
    # 2. Fold objects only if they are foldable.
    # 3. Only push soft objects after placing items in the bin.
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object4
    
    # c) Action sequence
    # Place the soft object first
    robot.pick(object1)
    robot.place(object1, box)
    
    # Then place the rigid and fragile objects
    robot.pick(object0)
    robot.place(object0, box)
    
    robot.pick(object2)
    robot.place(object2, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. Placed the soft object (brown_3D_cuboid) first as per the rule.
    # 2. Placed the rigid (yellow_3D_cylinder) and fragile (green_3D_cylinder) objects after the soft object.
    # 3. No need to fold or push any objects as per the rules.
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_box == True
    
    print("All task planning is done")
