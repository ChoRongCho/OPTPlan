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
    is_rigid: bool
    is_elastic: bool
    is_soft: bool
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool


class Robot:
    # Define skills
    def __init__(self,
                 name: str = "UR5",
                 goal: str = None,
                 actions: dict = None):
        self.name = name
        self.goal = goal
        self.actions = actions
    
        self.robot_handempty = True
        self.robot_now_holding = None
        self.robot_base_pose = True
    
    # basic state
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_base_pose = False
    
    # basic state
    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj
        self.robot_base_pose = False
    
    # basic state
    def state_base(self):
        self.robot_base_pose = True
    
    def pick(self, obj, bin):
        # Preconditions
        if obj.out_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.out_box = False
            obj.in_box = False
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj:
            # Check if there are any soft objects in the bin
            soft_objects_in_bin = any(o.is_soft for o in bin.in_bin_objects)
            if obj.is_fragile or obj.is_rigid:
                if soft_objects_in_bin:
                    # Effects
                    self.state_handempty()
                    obj.in_box = True
                    obj.out_box = False
                    bin.in_bin_objects.append(obj)
                    print(f"Place {obj.name} in {bin.name}")
                else:
                    print(f"Cannot place {obj.name} in {bin.name} without soft objects")
            else:
                # Effects
                self.state_handempty()
                obj.in_box = True
                obj.out_box = False
                bin.in_bin_objects.append(obj)
                print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if obj.is_soft and self.robot_handempty:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if obj.is_elastic and self.robot_handempty:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj.in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.in_box = False
            obj.out_box = True
            bin.in_bin_objects.remove(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_rigid=False, is_elastic=False, is_soft=True,
    in_box=False, out_box=True
)

object1 = Object(
    index=1, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_rigid=True, is_elastic=False, is_soft=False,
    in_box=False, out_box=True
)

object2 = Object(
    index=2, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_rigid=True, is_elastic=False, is_soft=False,
    in_box=False, out_box=True
)

object3 = Object(
    index=3, name='white_2D_ring', color='white', shape='2D_ring', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_rigid=False, is_elastic=True, is_soft=False,
    in_box=True, out_box=False
)

white_box = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_rigid=False, is_elastic=False, is_soft=False,
    in_box=False, out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    initial_state = {
        "object0": {"in_box": False, "out_box": True},
        "object1": {"in_box": False, "out_box": True},
        "object2": {"in_box": False, "out_box": True},
        "object3": {"in_box": True, "out_box": False},
        "white_box": {"in_bin_objects": []}
    }
    
    # Goal state
    goal_state = {
        "object0": {"in_box": True, "out_box": False},
        "object1": {"in_box": True, "out_box": False},
        "object2": {"in_box": True, "out_box": False},
        "object3": {"in_box": True, "out_box": False},
        "white_box": {"in_bin_objects": [object0, object1, object2, object3]}
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick and place the soft object (object0) first.
    # 2. Pick and place the fragile and rigid objects (object1 and object2) after the soft object is in the box.
    # 3. Ensure the already in-box object (object3) remains in the box.
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = white_box
    
    # c) Action sequence
    # Pick and place the soft object first
    robot.pick(object0, box)
    robot.place(object0, box)
    
    # Pick and place the fragile and rigid objects
    robot.pick(object1, box)
    robot.place(object1, box)
    
    robot.pick(object2, box)
    robot.place(object2, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. The soft object (object0) is placed first to satisfy the rule that fragile or rigid objects can only be placed if there is a soft object in the box.
    # 2. The fragile and rigid objects (object1 and object2) are placed after the soft object to ensure they are placed safely.
    # 3. The already in-box object (object3) remains in the box as it is already in the goal state.
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert set(box.in_bin_objects) == {object0, object1, object2, object3}
    
    print("All task planning is done")
