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
    is_fragile: bool
    is_soft: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool


class Robot:
    def __init__(self,
                 name: str = "OpenManipulator",
                 goal: str = None,
                 actions: dict = None):
        self.name = name
        self.goal = goal
        self.actions = actions
    
        self.robot_handempty = True
        self.robot_now_holding = None
        self.robot_base_pose = True
    
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_base_pose = False
    
    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj
        self.robot_base_pose = False
    
    def state_base(self):
        self.robot_base_pose = True
    
    def pick(self, obj, bin):
        if obj.out_box and self.robot_handempty:
            self.state_holding(obj)
            obj.out_box = False
            obj.in_box = False
            print(f"Picked {obj.name}")
        else:
            print(f"Cannot pick {obj.name}")
        
    def place(self, obj, bin):
        if self.robot_now_holding == obj:
            self.state_handempty()
            obj.in_box = True
            obj.out_box = False
            bin.in_bin_objects.append(obj)
            print(f"Placed {obj.name} in {bin.name}")
        else:
            print(f"Cannot place {obj.name}")
    
    def push(self, obj, bin): 
        if self.robot_handempty and obj.is_soft and obj.in_box:
            obj.pushed = True
            print(f"Pushed {obj.name}")
        else:
            print(f"Cannot push {obj.name}")
    
    def fold(self, obj, bin):
        if self.robot_handempty and obj.is_elastic:
            obj.folded = True
            print(f"Folded {obj.name}")
        else:
            print(f"Cannot fold {obj.name}")
    
    def out(self, obj, bin):
        if obj.in_box and self.robot_handempty:
            self.state_holding(obj)
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            obj.out_box = True
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_elastic=False, is_fragile=False, is_soft=False,
    in_box=False, out_box=True
)

object1 = Object(
    index=1, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_elastic=False, is_fragile=False, is_soft=True,
    in_box=False, out_box=True
)

object2 = Object(
    index=2, name='black_2D_circle', color='black', shape='2D_circle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_elastic=True, is_fragile=True, is_soft=False,
    in_box=True, out_box=False
)

object3 = Object(
    index=3, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_elastic=True, is_fragile=False, is_soft=False,
    in_box=True, out_box=False
)

object4 = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_elastic=False, is_fragile=False, is_soft=False,
    in_box=True, out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    initial_state = {
        "object0": {"in_box": False, "out_box": True},
        "object1": {"in_box": False, "out_box": True},
        "object2": {"in_box": True, "out_box": False},
        "object3": {"in_box": True, "out_box": False},
        "object4": {"in_box": True, "out_box": False, "in_bin_objects": []}
    }
    
    # Goal state
    goal_state = {
        "object0": {"in_box": True, "out_box": False},
        "object1": {"in_box": True, "out_box": False},
        "object2": {"in_box": True, "out_box": False},
        "object3": {"in_box": True, "out_box": False},
        "object4": {"in_box": True, "out_box": False, "in_bin_objects": [0, 1, 2, 3]}
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick and place the soft object (object1) first.
    # 2. Pick and place the rigid object (object0).
    # 3. Pick and place the fragile object (object2).
    # 4. Pick and place the elastic object (object3).

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object4

    # Action sequence
    robot.pick(object1, box)  # Pick red_3D_polyhedron
    robot.place(object1, box)  # Place red_3D_polyhedron in white_box

    robot.pick(object0, box)  # Pick yellow_3D_cylinder
    robot.place(object0, box)  # Place yellow_3D_cylinder in white_box

    robot.pick(object2, box)  # Pick black_2D_circle
    robot.place(object2, box)  # Place black_2D_circle in white_box

    robot.pick(object3, box)  # Pick white_2D_loop
    robot.place(object3, box)  # Place white_2D_loop in white_box

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasons:
    # 1. Placed the soft object (object1) first as per the rule.
    # 2. Placed the rigid object (object0) after the soft object.
    # 3. Placed the fragile object (object2) after the soft object.
    # 4. Placed the elastic object (object3) last.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_bin_objects == [object0, object1, object2, object3]
    
    print("All task planning is done")
