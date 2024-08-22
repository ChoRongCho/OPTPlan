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
    is_foldable: bool
    is_elastic: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool




    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=True, is_elastic=False, in_box=False, out_box=True)
object1 = Object(index=1, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=True, in_box=False, out_box=True)
object2 = Object(index=2, name='beige_2D_loop', color='beige', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=True, in_box=False, out_box=True)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_foldable=False, is_elastic=False, in_box=True, out_box=False)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    initial_state = {
        "object0": {"in_box": False, "folded": False, "pushed": False},
        "object1": {"in_box": False, "folded": False, "pushed": False},
        "object2": {"in_box": False, "folded": False, "pushed": False},
        "object3": {"in_box": True, "folded": False, "pushed": False, "in_bin_objects": []}
    }
    
    goal_state = {
        "object0": {"in_box": True, "folded": True, "pushed": False},
        "object1": {"in_box": True, "folded": False, "pushed": False},
        "object2": {"in_box": True, "folded": False, "pushed": True},
        "object3": {"in_box": True, "folded": False, "pushed": False, "in_bin_objects": [0, 1, 2]}
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold the foldable object (object0).
    # 2. Place the elastic objects (object1 and object2) in the box.
    # 3. Push the soft object (object2) after placing it in the box.
    # 4. Place the rigid object (object0) in the box.
    # 5. Ensure all objects are in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object3

    # Action sequence
    robot.fold(object0)  # Fold the foldable object
    robot.place(object1, box)  # Place the elastic object1 in the box
    robot.place(object2, box)  # Place the elastic object2 in the box
    robot.push(object2)  # Push the soft object2
    robot.place(object0, box)  # Place the rigid object0 in the box

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. Fold object0 because it is foldable.
    # 2. Place object1 and object2 in the box before placing the rigid object0.
    # 3. Push object2 after placing it in the box because it is soft.
    # 4. Place object0 in the box last because it is rigid.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object0.folded == True
    assert object1.in_box == True
    assert object1.folded == False
    assert object2.in_box == True
    assert object2.pushed == True
    assert object3.in_bin_objects == [0, 1, 2]
    
    print("All task planning is done")
