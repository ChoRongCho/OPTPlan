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
    init_pose: str
    in_box: bool


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
        if self.robot_handempty and not obj.in_box:
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
    
    def place(self, obj, bin):
        if self.robot_now_holding == obj:
            if obj.is_soft:
                self.state_handempty()
                obj.in_box = True
                bin.in_bin_objects.append(obj)
                print(f"Place {obj.name} in {bin.name}")
            else:
                soft_objects_in_bin = any(o.is_soft for o in bin.in_bin_objects)
                if soft_objects_in_bin:
                    self.state_handempty()
                    obj.in_box = True
                    bin.in_bin_objects.append(obj)
                    print(f"Place {obj.name} in {bin.name}")
                else:
                    print(f"Cannot Place {obj.name} in {bin.name} without soft object")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin):
        if self.robot_handempty and obj.is_soft and obj.in_box:
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
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_elastic=False, is_fragile=False, is_soft=False,
    init_pose='out_box', in_box=False
)

object1 = Object(
    index=1, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_elastic=False, is_fragile=False, is_soft=True,
    init_pose='out_box', in_box=False
)

object2 = Object(
    index=2, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_elastic=False, is_fragile=True, is_soft=False,
    init_pose='out_box', in_box=False
)

object3 = Object(
    index=3, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_elastic=True, is_fragile=False, is_soft=True,
    init_pose='out_box', in_box=False
)

object4 = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_elastic=False, is_fragile=False, is_soft=False,
    init_pose='box', in_box=True
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    initial_state = {
        "object0": object0,
        "object1": object1,
        "object2": object2,
        "object3": object3,
        "object4": object4
    }
    
    # Goal state
    goal_state = {
        "object0": {"in_box": True},
        "object1": {"in_box": True},
        "object2": {"in_box": True},
        "object3": {"in_box": True},
        "object4": {"in_bin_objects": [object0, object1, object2, object3]}
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick and place the soft objects first (object1 and object3).
    # 2. Pick and place the rigid and fragile objects (object0 and object2).
    # 3. Ensure the soft objects are in the box before placing rigid or fragile objects.
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object4
    
    # Action sequence
    robot.pick(object1, box)
    robot.place(object1, box)
    
    robot.pick(object3, box)
    robot.place(object3, box)
    
    robot.pick(object0, box)
    robot.place(object0, box)
    
    robot.pick(object2, box)
    robot.place(object2, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasons:
    # 1. Pick and place object1 (soft) first to satisfy the condition for placing rigid or fragile objects.
    # 2. Pick and place object3 (soft) next to ensure there are enough soft objects in the box.
    # 3. Pick and place object0 (rigid) after soft objects are in the box.
    # 4. Pick and place object2 (fragile) after soft objects are in the box.
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    # Don't include a box in the goal state. Only express objects.
    
    print("All task planning is done")
