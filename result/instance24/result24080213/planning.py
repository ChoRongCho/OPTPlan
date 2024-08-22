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
    is_elastic: bool
    is_foldable: bool
    is_rigid: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='yellow_2D_rectangle', 
    color='yellow', 
    shape='2D_rectangle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=False, 
    is_foldable=True, 
    is_rigid=False, 
    in_box=False, 
    out_box=True
)

object1 = Object(
    index=1, 
    name='transparent_2D_circle', 
    color='transparent', 
    shape='2D_circle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=True, 
    is_foldable=False, 
    is_rigid=False, 
    in_box=False, 
    out_box=True
)

object2 = Object(
    index=2, 
    name='yellow_3D_cylinder', 
    color='yellow', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_elastic=False, 
    is_foldable=False, 
    is_rigid=True, 
    in_box=False, 
    out_box=True
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
    is_elastic=False, 
    is_foldable=False, 
    is_rigid=False, 
    in_box=True, 
    out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    initial_state = {
        "object0": {"in_box": False, "out_box": True, "folded": False, "pushed": False},
        "object1": {"in_box": False, "out_box": True, "folded": False, "pushed": False},
        "object2": {"in_box": False, "out_box": True, "folded": False, "pushed": False},
        "object3": {"in_box": True, "out_box": False, "in_bin_objects": []}
    }
    
    goal_state = {
        "object0": {"in_box": True, "out_box": False, "folded": False, "pushed": False},
        "object1": {"in_box": True, "out_box": False, "folded": False, "pushed": False},
        "object2": {"in_box": True, "out_box": False, "folded": False, "pushed": False},
        "object3": {"in_box": True, "out_box": False, "in_bin_objects": [0, 1, 2]}
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Rules:
    # 1. Place a soft object before placing a fragile or rigid object if there is any soft object.
    # 2. Fold objects only if they are foldable.
    # 3. Only push soft objects after placing items in the bin.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object3

    # Action sequence
    # 1. Place the soft object (transparent_2D_circle) in the box first
    robot.pick(object1)
    robot.place(object1, box)
    
    # 2. Place the foldable object (yellow_2D_rectangle) in the box
    robot.pick(object0)
    robot.fold(object0)
    robot.place(object0, box)
    
    # 3. Place the rigid object (yellow_3D_cylinder) in the box
    robot.pick(object2)
    robot.place(object2, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - Placed the soft object (object1) first to satisfy the rule of placing soft objects before rigid or fragile ones.
    # - Folded the foldable object (object0) before placing it in the box.
    # - Placed the rigid object (object2) last.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_bin_objects == [0, 1, 2]
    
    print("All task planning is done")