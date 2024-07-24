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
        # pick an {object} not in the {bin}, it does not include 'place' action
        if self.robot_handempty and not obj.in_box:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
            obj.in_box = False
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if self.robot_now_holding == obj and obj.object_type != 'box':
            if obj.is_soft and not obj.pushed:
                print(f"Cannot Place {obj.name} because it is soft and not pushed")
            else:
                print(f"Place {obj.name} in {bin.name}")
                bin.in_bin_objects.append(obj)
                obj.in_box = True
                self.state_handempty()
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.in_box:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and obj.in_box:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj.in_box and obj in bin.in_bin_objects:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_holding(obj)
        else:
            print(f"Cannot Out {obj.name}")

# Reason:
# The robot actions are designed to follow the given rules strictly. The 'pick' action ensures the robot can only pick objects not already in the bin and when its hand is empty. The 'place' action includes a check to ensure soft objects are pushed before being placed in the bin, adhering to rule 3. The 'push' and 'fold' actions require the robot's hand to be empty and the object to be in the bin, ensuring proper handling of objects. The 'out' action allows the robot to remove objects from the bin, which is necessary for handling rigid objects as per rule 4. These actions ensure the robot operates within the constraints provided, maintaining a clear and logical flow for the bin_packing task.

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_soft=True, init_pose='out_box', in_box=False)
object1 = Object(index=1, name='white_2D_ring', color='white', shape='2D_ring', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_soft=False, init_pose='out_box', in_box=False)
object2 = Object(index=2, name='blue_2D_ring', color='blue', shape='2D_ring', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, init_pose='out_box', in_box=False)
object3 = Object(index=3, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_soft=False, init_pose='in_box', in_box=True)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, init_pose='box', in_box=True)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    # object0: out_box, not in box, not pushed, not folded
    # object1: out_box, not in box, not pushed, not folded
    # object2: out_box, not in box, not pushed, not folded
    # object3: in_box, in box, not pushed, not folded
    # object4: box, in box, not pushed, not folded

    # Final State
    # object0: in_bin, in box, pushed, not folded
    # object1: in_bin, in box, not pushed, not folded
    # object2: out_bin, not in box, not pushed, not folded
    # object3: in_bin, in box, not pushed, not folded
    # object4: box, in box, not pushed, not folded

    # Second, using given rules and object's states, make a task planning strategy
    # Rule 1: Never pick and place a box
    # Rule 3: When placing a soft object, it must be pushed before being packed in the bin
    # Rule 4: When a rigid object is in the bin at the initial state, remove it and replace it into the bin

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object4

    # c) Action sequence
    # Step 1: Out the rigid object (object3) from the box and place it back
    robot.out(object3, box)
    robot.place(object3, box)

    # Step 2: Pick and place the yellow_3D_cuboid (object0) after pushing it
    robot.pick(object0, box)
    robot.place(object0, box)
    robot.push(object0, box)

    # Step 3: Pick and place the white_2D_ring (object1)
    robot.pick(object1, box)
    robot.place(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason:
    # 1. The robot first removes the rigid object (object3) from the box and places it back to satisfy Rule 4.
    # 2. The robot picks and places the soft object (object0) and pushes it before placing it in the box to satisfy Rule 3.
    # 3. The robot picks and places the non-soft object (object1) directly into the box.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object0.pushed == True
    assert object1.in_box == True
    assert object2.in_box == False
    assert object3.in_box == True
    assert object4.in_box == True
    print("All task planning is done")
