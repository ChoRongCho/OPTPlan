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
    pushed: bool = False
    folded: bool = False
    
    # Predicates for box
    in_bin_objects: list = None
    
    # Object physical properties 
    is_elastic: bool = False
    is_soft: bool = False
    is_fragile: bool = False
    is_rigid: bool = False
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool = False
    out_box: bool = True




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='brown_3D_cuboid', 
    color='brown', 
    shape='3D_cuboid', 
    object_type='obj', 
    is_elastic=True, 
    is_soft=True, 
    in_box=False, 
    out_box=True
)

object1 = Object(
    index=1, 
    name='black_2D_loop', 
    color='black', 
    shape='2D_loop', 
    object_type='obj', 
    is_rigid=True, 
    in_box=False, 
    out_box=True
)

object2 = Object(
    index=2, 
    name='transparent_3D_cuboid', 
    color='transparent', 
    shape='3D_cuboid', 
    object_type='obj', 
    is_fragile=True, 
    in_box=True, 
    out_box=False
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    in_bin_objects=[], 
    in_box=False, 
    out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    initial_state = {
        'object0': {'in_box': False, 'out_box': True},
        'object1': {'in_box': False, 'out_box': True},
        'object2': {'in_box': True, 'out_box': False},
        'object3': {'in_box': False, 'out_box': False, 'in_bin_objects': []}
    }
    
    goal_state = {
        'object0': {'in_box': True, 'out_box': False},
        'object1': {'in_box': True, 'out_box': False},
        'object2': {'in_box': True, 'out_box': False}
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Rules:
    # 1. Place a soft object before placing a fragile or rigid object.
    # 2. Fold objects only if they are foldable.
    # 3. Only push soft objects after placing items in the bin.
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object3
    
    # c) Action sequence
    # 1. Place the soft object (object0) in the box
    robot.place(object0, box)
    
    # 2. Place the rigid object (object1) in the box
    robot.place(object1, box)
    
    # 3. The fragile object (object2) is already in the box, no action needed
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - Placed the soft object (object0) first to satisfy the rule of placing soft objects before fragile or rigid objects.
    # - Placed the rigid object (object1) after the soft object.
    # - No need to place the fragile object (object2) as it is already in the box.
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    
    print("All task planning is done")
