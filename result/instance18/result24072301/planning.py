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
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    is_elastic: bool
    is_soft: bool
    
    # Object physical properties
    init_pose: str
    in_box: bool


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
        if self.robot_handempty and not obj.in_box:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj:
            if obj.is_soft and not any(o.is_elastic for o in bin.in_bin_objects):
                print(f"Cannot Place {obj.name} because no elastic object in bin")
                return
            if not obj.is_soft and not any(o.is_soft for o in bin.in_bin_objects):
                print(f"Cannot Place {obj.name} because no soft object in bin")
                return
            # Effects
            self.state_handempty()
            obj.in_box = True
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.in_box:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.in_box:
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
            bin.in_bin_objects.remove(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name}")

# Reason:
# The robot actions are designed to follow the given rules for bin packing. The preconditions ensure that the robot does not handle boxes directly, and it respects the constraints regarding the placement of soft and rigid objects. The effects update the state of the robot and objects to reflect the changes after each action. This design ensures that the robot's actions are consistent with the rules and the current state of the objects and bin.

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_soft=True, init_pose='out_box', in_box=False)
object1 = Object(index=1, name='transparent_2D_circle', color='transparent', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_soft=False, init_pose='out_box', in_box=False)
object2 = Object(index=2, name='black_2D_ring', color='black', shape='2D_ring', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_soft=True, init_pose='in_box', in_box=True)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[object2], is_elastic=False, is_soft=False, init_pose='box', in_box=False)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box, not in box
    # object1: out_box, not in box
    # object2: in_box, in box
    # object3: box, not in box (contains object2)

    # Goal State:
    # object0: in_bin, in box
    # object1: out_box, not in box
    # object2: in_bin, in box
    # object3: box, not in box (contains object0 and object2)

    # Second, using given rules and object's states, make a task planning strategy
    # Rule 1: Avoid handling and moving any box
    # Rule 2: When placing a soft object, the elastic object must be in the bin
    # Rule 3: When placing a rigid object, the soft object must be in the bin
    # Rule 4: When a rigid object is in the bin at the initial state, out of the rigid object first

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Action sequence
    # Step 1: Out the rigid object (object2) from the box (Rule 4)
    robot.out(object2, box)

    # Step 2: Pick the soft object (object0)
    robot.pick(object0, box)

    # Step 3: Place the soft object (object0) in the box (Rule 2)
    robot.place(object0, box)

    # Step 4: Pick the rigid object (object2)
    robot.pick(object2, box)

    # Step 5: Place the rigid object (object2) in the box (Rule 3)
    robot.place(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason:
    # 1. Out object2 first because it is a rigid object initially in the box (Rule 4).
    # 2. Pick and place object0 (soft) first because it needs to be in the box before placing any rigid object (Rule 2).
    # 3. Pick and place object2 (rigid) after object0 is in the box (Rule 3).

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == False
    assert object2.in_box == True
    assert object3.in_box == False
    print("All task planning is done")
