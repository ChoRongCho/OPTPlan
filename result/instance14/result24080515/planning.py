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
    is_elastic: bool
    
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
        # Preconditions: Object is out of the box and robot hand is empty
        if obj.out_box and self.robot_handempty:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
            obj.out_box = False
            obj.in_box = False
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions: Robot is holding the object
        if self.robot_now_holding == obj:
            # Check if there are any soft objects that need to be placed first
            soft_objects = [o for o in bin.in_bin_objects if o.is_soft]
            if obj.is_soft or (not obj.is_soft and not soft_objects):
                print(f"Place {obj.name} in {bin.name}")
                bin.in_bin_objects.append(obj)
                self.state_handempty()
                obj.in_box = True
                obj.out_box = False
            else:
                print(f"Cannot place {obj.name} before placing soft objects")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions: Object is soft and in the box, and robot hand is empty
        if obj.is_soft and obj.in_box and self.robot_handempty:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions: Object is foldable and robot hand is empty
        if obj.is_elastic and self.robot_handempty:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions: Object is in the box
        if obj.in_box:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            self.state_handempty()
            obj.in_box = False
            obj.out_box = True
        else:
            print(f"Cannot Out {obj.name}")

# Reason:
# The robot actions are designed to follow the given rules for a bin_packing task. The preconditions ensure that actions are only performed when the state of the robot and objects meet specific criteria, such as the robot's hand being empty or the object being in or out of the box. The effects update the state of the robot and objects to reflect the changes made by the actions. This approach ensures that the robot performs tasks in a logical and efficient manner, adhering to the constraints provided. For example, placing rigid objects only after soft objects ensures that fragile items are not damaged

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_rigid=False, is_elastic=True, in_box=False, out_box=True)
object1 = Object(index=1, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_rigid=True, is_elastic=False, in_box=False, out_box=True)
object2 = Object(index=2, name='black_2D_ring', color='black', shape='2D_ring', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_rigid=False, is_elastic=False, in_box=True, out_box=False)
object3 = Object(index=3, name='white_2D_ring', color='white', shape='2D_ring', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_rigid=False, is_elastic=True, in_box=True, out_box=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[object2, object3], is_soft=False, is_rigid=False, is_elastic=False, in_box=True, out_box=False)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    print("Initial State:")
    print(f"{object0.name}: in_box={object0.in_box}, out_box={object0.out_box}")
    print(f"{object1.name}: in_box={object1.in_box}, out_box={object1.out_box}")
    print(f"{object2.name}: in_box={object2.in_box}, out_box={object2.out_box}")
    print(f"{object3.name}: in_box={object3.in_box}, out_box={object3.out_box}")
    print(f"{object4.name}: in_box={object4.in_box}, out_box={object4.out_box}, in_bin_objects={[obj.name for obj in object4.in_bin_objects]}")
    
    # Goal state
    print("\nGoal State:")
    print(f"{object0.name}: in_box=True, out_box=False")
    print(f"{object1.name}: in_box=True, out_box=False")
    print(f"{object2.name}: in_box=True, out_box=False")
    print(f"{object3.name}: in_box=True, out_box=False")
    print(f"{object4.name}: in_box=True, out_box=False, in_bin_objects=['white_3D_cylinder', 'black_3D_cylinder', 'black_2D_ring', 'white_2D_ring']")

    # Second, using given rules and object's states, make a task planning strategy
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object4
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'.
    # Pick and place white_3D_cylinder (soft and elastic)
    robot.pick(object0, box)
    robot.place(object0, box)
    
    # Pick and place black_3D_cylinder (rigid)
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason: The white_3D_cylinder (soft) is placed first, followed by the black_3D_cylinder (rigid) as per the rule.
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_box == True
    assert object0.out_box == False
    assert object1.out_box == False
    assert object2.out_box == False
    assert object3.out_box == False
    assert object4.out_box == False
    assert object0 in object4.in_bin_objects
    assert object1 in object4.in_bin_objects
    assert object2 in object4.in_bin_objects
    assert object3 in object4.in_bin_objects
    
    print("All task planning is done")
