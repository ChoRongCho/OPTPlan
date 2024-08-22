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
    is_soft: bool
    is_rigid: bool
    is_foldable: bool
    is_fragile: bool
    
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
        self.robot_now_holding = None
        self.robot_base_pose = True
    
    # basic state
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_now_holding = None
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
        if self.robot_handempty and not obj.in_box:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and obj.is_packable:
            # Check if there are any soft objects that need to be placed first
            soft_objects = [o for o in bin.in_bin_objects if o.is_soft]
            if not soft_objects or all(o.in_box for o in soft_objects):
                # Effects
                self.state_handempty()
                obj.in_box = True
                bin.in_bin_objects.append(obj)
                print(f"Place {obj.name} in {bin.name}")
            else:
                print(f"Cannot Place {obj.name} before soft objects")
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
        if self.robot_handempty and obj.is_foldable:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj in bin.in_bin_objects:
            # Effects
            self.state_holding(obj)
            obj.in_box = False
            bin.in_bin_objects.remove(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_rigid=True,
    is_foldable=False, is_fragile=False, in_box=False, is_packable=True
)

object1 = Object(
    index=1, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_rigid=True,
    is_foldable=False, is_fragile=True, in_box=False, is_packable=True
)

object2 = Object(
    index=2, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_soft=True, is_rigid=False,
    is_foldable=False, is_fragile=False, in_box=False, is_packable=True
)

object3 = Object(
    index=3, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_rigid=True,
    is_foldable=True, is_fragile=False, in_box=False, is_packable=True
)

object4 = Object(
    index=4, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_soft=False, is_rigid=False,
    is_foldable=False, is_fragile=False, in_box=False, is_packable=True
)

object5 = Object(
    index=5, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_rigid=False,
    is_foldable=False, is_fragile=False, in_box=True, is_packable=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    initial_state = {
        object0.name: object0.in_box,
        object1.name: object1.in_box,
        object2.name: object2.in_box,
        object3.name: object3.in_box,
        object4.name: object4.in_box,
        object5.name: object5.in_bin_objects
    }
    
    # Goal state
    goal_state = {
        object0.name: True,
        object1.name: True,
        object2.name: True,
        object3.name: True,
        object4.name: True,
        object5.name: [object0, object1, object2, object3, object4]
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object5
    
    # Action sequence
    robot.pick(object2, box)  # Pick white_3D_cylinder (soft object)
    robot.place(object2, box)  # Place white_3D_cylinder in the box
    
    robot.pick(object0, box)  # Pick black_3D_cylinder
    robot.place(object0, box)  # Place black_3D_cylinder in the box
    
    robot.pick(object1, box)  # Pick green_3D_cylinder (fragile object)
    robot.place(object1, box)  # Place green_3D_cylinder in the box
    
    robot.pick(object3, box)  # Pick white_2D_circle (foldable object)
    robot.fold(object3, box)  # Fold white_2D_circle
    robot.place(object3, box)  # Place white_2D_circle in the box
    
    robot.pick(object4, box)  # Pick transparent_2D_circle
    robot.place(object4, box)  # Place transparent_2D_circle in the box
    robot.push(object4, box)  # Push transparent_2D_circle (elastic object)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # - Placed the soft object first (white_3D_cylinder) to satisfy the rule for placing fragile or rigid objects.
    # - Folded the foldable object (white_2D_circle) before placing it in the box.
    # - Pushed the elastic object (transparent_2D_circle) after placing it in the box.
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_box == True
    assert object5.in_bin_objects == [object0, object1, object2, object3, object4]
    
    print("All task planning is done")
