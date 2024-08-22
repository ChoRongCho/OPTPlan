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
    is_elastic: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='brown_3D_cuboid', 
    color='brown', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_fragile=False, 
    is_soft=True, 
    is_elastic=True, 
    in_box=False, 
    out_box=True
)

object1 = Object(
    index=1, 
    name='white_2D_circle', 
    color='white', 
    shape='2D_circle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_fragile=True, 
    is_soft=False, 
    is_elastic=False, 
    in_box=False, 
    out_box=True
)

object2 = Object(
    index=2, 
    name='black_2D_loop', 
    color='black', 
    shape='2D_loop', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_fragile=False, 
    is_soft=False, 
    is_elastic=True, 
    in_box=True, 
    out_box=False
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_fragile=False, 
    is_soft=False, 
    is_elastic=False, 
    in_box=False, 
    out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    initial_state = {
        'object0': {'in_box': False, 'out_box': True},
        'object1': {'in_box': False, 'out_box': True},
        'object2': {'in_box': True, 'out_box': False},
        'object3': {'in_box': False, 'out_box': False}
    }
    
    goal_state = {
        'object0': {'in_box': True, 'out_box': False},
        'object1': {'in_box': True, 'out_box': False},
        'object2': {'in_box': True, 'out_box': False},
        'object3': {'in_box': False, 'out_box': False}  # Box itself doesn't change
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Rules:
    # 1. Place soft object before fragile or rigid objects.
    # 2. Fold objects only if they are foldable.
    # 3. Only push soft objects after placing items in the bin.
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object3
    
    # c) Action sequence
    # Place the soft object (object0) first
    robot.pick(object0)
    robot.place(object0, box)
    
    # Then place the fragile object (object1)
    robot.pick(object1)
    robot.place(object1, box)
    
    # No need to place object2 as it is already in the box
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. Placed the soft object (object0) first to satisfy the rule of placing soft objects before fragile or rigid objects.
    # 2. Placed the fragile object (object1) after the soft object.
    # 3. No need to fold or push any objects as per the given rules and current scenario.
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == False  # Box itself doesn't change
    
    print("All task planning is done")
