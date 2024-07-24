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
    is_rigid: bool
    is_foldable: bool
    
    # Object physical properties
    init_pose: str
    in_bin: bool


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
        # pick an {object} not in the {bin}, it does not include 'place' action
        if self.robot_handempty and not obj.in_bin and obj.object_type != 'box':
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if self.robot_now_holding == obj and obj.object_type != 'box':
            if obj.is_rigid:
                if all(o.is_rigid or o.pushed for o in bin.in_bin_objects):
                    bin.in_bin_objects.append(obj)
                    obj.in_bin = True
                    self.state_handempty()
                    print(f"Place {obj.name in bin.name}")
                else:
                    print(f"Cannot Place {obj.name} in {bin.name} due to soft objects not being pushed")
            else:
                bin.in_bin_objects.append(obj)
                obj.in_bin = True
                self.state_handempty()
                print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.in_bin and not obj.is_rigid:
            if not any(o.is_rigid for o in bin.in_bin_objects if o != obj):
                obj.pushed = True
                print(f"Push {obj.name}")
            else:
                print(f"Cannot Push {obj.name} due to fragile objects on top")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and obj.is_foldable:
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj.in_bin and obj in bin.in_bin_objects:
            bin.in_bin_objects.remove(obj)
            obj.in_bin = False
            self.state_holding(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='yellow_2D_rectangle', 
    color='yellow', 
    shape='2D_rectangle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=False, 
    is_foldable=True, 
    init_pose='out_box', 
    in_bin=False
)

object1 = Object(
    index=1, 
    name='yellow_3D_cylinder', 
    color='yellow', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=True, 
    is_foldable=False, 
    init_pose='out_box', 
    in_bin=False
)

object2 = Object(
    index=2, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=False, 
    is_foldable=False, 
    init_pose='box', 
    in_bin=True
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0 (yellow_2D_rectangle): out_box, not in bin
    # object1 (yellow_3D_cylinder): out_box, not in bin
    # object2 (white_box): in_box, in bin, empty

    # Goal State:
    # object0 (yellow_2D_rectangle): in_box, in bin, pushed
    # object1 (yellow_3D_cylinder): in_box, in bin
    # object2 (white_box): in_box, in bin, contains object0 and object1

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Pick and place the yellow_2D_rectangle (soft object) in the white_box
    # 2. Push the yellow_2D_rectangle to make space
    # 3. Pick and place the yellow_3D_cylinder (rigid object) in the white_box

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object2

    # c) Action sequence
    # Step 1: Pick yellow_2D_rectangle
    robot.pick(object0, box)
    # Step 2: Place yellow_2D_rectangle in white_box
    robot.place(object0, box)
    # Step 3: Push yellow_2D_rectangle to make space
    robot.push(object0, box)
    # Step 4: Pick yellow_3D_cylinder
    robot.pick(object1, box)
    # Step 5: Place yellow_3D_cylinder in white_box
    robot.place(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason for Step 1: Pick the soft object (yellow_2D_rectangle) to place it in the box.
    # Reason for Step 2: Place the soft object in the box to make space for the rigid object.
    # Reason for Step 3: Push the soft object to make more space in the box.
    # Reason for Step 4: Pick the rigid object (yellow_3D_cylinder) to place it in the box.
    # Reason for Step 5: Place the rigid object in the box after the soft object has been pushed.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_bin == True
    assert object0.pushed == True
    assert object1.in_bin == True
    assert object2.in_bin_objects == [object0, object1]
    print("All task planning is done")
