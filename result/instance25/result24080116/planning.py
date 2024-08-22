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
    is_elastic: bool
    is_soft: bool
    is_rigid: bool
    
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
        if self.robot_handempty and obj.out_box:
            self.state_holding(obj)
            obj.out_box = False
            obj.in_box = True
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        if self.robot_now_holding == obj:
            if obj.is_fragile or obj.is_rigid:
                if any(o.is_soft for o in bin.in_bin_objects):
                    self.state_handempty()
                    obj.in_box = True
                    obj.out_box = False
                    bin.in_bin_objects.append(obj)
                    print(f"Place {obj.name} in {bin.name}")
                else:
                    print(f"Cannot Place {obj.name} in {bin.name} without soft object")
            else:
                self.state_handempty()
                obj.in_box = True
                obj.out_box = False
                bin.in_bin_objects.append(obj)
                print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        if self.robot_handempty and obj.is_soft:
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        if self.robot_handempty and obj.is_elastic:
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        if obj in bin.in_bin_objects:
            self.state_holding(obj)
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            obj.out_box = True
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='black_3D_cuboid', color='black', shape='3D_cuboid', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_elastic=True, is_soft=False, is_rigid=False,
    in_box=False, out_box=True
)

object1 = Object(
    index=1, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_elastic=False, is_soft=False, is_rigid=True,
    in_box=False, out_box=True
)

object2 = Object(
    index=2, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_elastic=True, is_soft=True, is_rigid=False,
    in_box=False, out_box=True
)

object3 = Object(
    index=3, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_elastic=True, is_soft=False, is_rigid=False,
    in_box=True, out_box=False
)

object4 = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_elastic=False, is_soft=False, is_rigid=False,
    in_box=True, out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    initial_state = {
        "object0": {"in_box": False, "out_box": True},
        "object1": {"in_box": False, "out_box": True},
        "object2": {"in_box": False, "out_box": True},
        "object3": {"in_box": True, "out_box": False},
        "object4": {"in_box": True, "out_box": False, "in_bin_objects": []}
    }
    
    # Goal State
    goal_state = {
        "object0": {"in_box": True, "out_box": False},
        "object1": {"in_box": True, "out_box": False},
        "object2": {"in_box": True, "out_box": False},
        "object3": {"in_box": True, "out_box": False},
        "object4": {"in_box": True, "out_box": False, "in_bin_objects": [0, 1, 2, 3]}
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick and place the soft object (object2) first.
    # 2. Pick and place the fragile object (object0) after the soft object is in the box.
    # 3. Pick and place the rigid object (object1) after the soft object is in the box.
    # 4. Ensure all objects are placed in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object4

    # c) Action sequence
    # Pick and place the soft object (object2)
    robot.pick(object2, box)
    robot.place(object2, box)
    
    # Pick and place the fragile object (object0)
    robot.pick(object0, box)
    robot.place(object0, box)
    
    # Pick and place the rigid object (object1)
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. The soft object (object2) is placed first to satisfy the condition for placing fragile and rigid objects.
    # 2. The fragile object (object0) is placed after the soft object to ensure it is cushioned.
    # 3. The rigid object (object1) is placed after the soft object to ensure it is cushioned.
    # 4. All objects are placed in the box to meet the goal state.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_bin_objects == [object0, object1, object2, object3]
    
    print("All task planning is done")
