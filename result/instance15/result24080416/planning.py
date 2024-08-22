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
            # Check if there are any soft objects that need to be placed first
            soft_objects = [o for o in bin.in_bin_objects if o.is_soft]
            if obj.is_fragile or obj.is_rigid:
                if soft_objects:
                    print(f"Cannot Place {obj.name} before placing soft objects")
                    return
            # Effects
            self.state_handempty()
            obj.in_box = True
            obj.out_box = False
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if obj.is_soft and self.robot_handempty:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if obj.is_elastic and self.robot_handempty:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj.in_box:
            # Effects
            self.state_holding(obj)
            obj.in_box = False
            obj.out_box = True
            bin.in_bin_objects.remove(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_rigid=False,
    is_elastic=True, is_soft=True, in_box=False, out_box=True
)

object1 = Object(
    index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_rigid=False,
    is_elastic=True, is_soft=True, in_box=False, out_box=True
)

object2 = Object(
    index=2, name='blue_1D_linear', color='blue', shape='1D_linear', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_rigid=True,
    is_elastic=False, is_soft=False, in_box=False, out_box=True
)

object3 = Object(
    index=3, name='green_3D_sphere', color='green', shape='3D_sphere', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_rigid=False,
    is_elastic=True, is_soft=False, in_box=True, out_box=False
)

object4 = Object(
    index=4, name='white_2D_ring', color='white', shape='2D_ring', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_rigid=False,
    is_elastic=True, is_soft=False, in_box=True, out_box=False
)

object5 = Object(
    index=5, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[object3, object4], is_fragile=False, is_rigid=False,
    is_elastic=False, is_soft=False, in_box=True, out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state is already described in the given data

    # Second, using given rules and object's states, make a task planning strategy
    # We need to place all objects in the box, ensuring soft objects are placed before fragile or rigid objects

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object5

    # Action sequence
    # 1. Pick and place soft objects first
    robot.pick(object0, box)
    robot.place(object0, box)
    
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # 2. Pick and place the fragile and rigid object
    robot.pick(object2, box)
    robot.place(object2, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason: Soft objects (object0 and object1) are placed first to ensure the fragile object (object2) is not damaged.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_box == True
    assert object5.in_bin_objects == [object3, object4, object0, object1, object2]
    
    print("All task planning is done")
