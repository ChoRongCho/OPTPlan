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
    is_rigid: bool
    is_fragile: bool
    is_elastic: bool
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    is_packable: bool


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
        self.robot_now_holding = False
        self.robot_base_pose = True
    
    # basic state
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_base_pose = False
    
    # basic state
    def state_holding(self, objects):
        self.robot_handempty = False
        self.robot_now_holding = objects
        self.robot_base_pose = False
    
    # basic state
    def state_base(self):
        self.robot_base_pose = True
    
    def pick(self, obj, bin):
        # Preconditions
        if self.robot_handempty and not obj.in_box:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and obj.is_packable:
            # Check if there are any soft objects not in the box
            soft_objects_not_in_box = any(o.is_soft and not o.in_box for o in bin.in_bin_objects)
            if not soft_objects_not_in_box or obj.is_soft:
                # Effects
                self.state_handempty()
                obj.in_box = True
                bin.in_bin_objects.append(obj)
                print(f"Place {obj.name} in {bin.name}")
            else:
                print(f"Cannot Place {obj.name} before placing soft objects")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_soft and obj.in_box:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_packable:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj in bin.in_bin_objects:
            # Effects
            self.state_handempty()
            obj.in_box = False
            bin.in_bin_objects.remove(obj)
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_rigid=False, is_fragile=False, is_elastic=False,
    in_box=False, is_packable=True
)

object1 = Object(
    index=1, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_rigid=True, is_fragile=False, is_elastic=False,
    in_box=False, is_packable=True
)

object2 = Object(
    index=2, name='green_2D_circle', color='green', shape='2D_circle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_rigid=False, is_fragile=True, is_elastic=False,
    in_box=False, is_packable=True
)

object3 = Object(
    index=3, name='white_2D_ring', color='white', shape='2D_ring', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_rigid=False, is_fragile=False, is_elastic=True,
    in_box=False, is_packable=True
)

object4 = Object(
    index=4, name='black_1D_linear', color='black', shape='1D_linear', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_rigid=False, is_fragile=False, is_elastic=True,
    in_box=True, is_packable=True
)

white_box = Object(
    index=5, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_rigid=False, is_fragile=False, is_elastic=False,
    in_box=False, is_packable=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state is already described in the given data

    # Second, using given rules and object's states, make a task planning strategy
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = white_box
    
    # Action sequence
    # 1. Pick and place the soft object first
    robot.pick(object0, box)
    robot.place(object0, box)
    
    # 2. Pick and place the rigid object
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # 3. Pick and place the fragile object
    robot.pick(object2, box)
    robot.place(object2, box)
    
    # 4. Pick and place the elastic object
    robot.pick(object3, box)
    robot.place(object3, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # - The soft object (red_3D_polyhedron) is placed first to satisfy the rule that soft objects should be placed before rigid or fragile objects.
    # - The rigid object (yellow_3D_cylinder) is placed next.
    # - The fragile object (green_2D_circle) is placed after the rigid object.
    # - The elastic object (white_2D_ring) is placed last.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_box == True  # Already in the box initially
    assert object5.in_bin_objects == [object0, object1, object2, object3, object4]
    
    print("All task planning is done")
