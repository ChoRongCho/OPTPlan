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
    in_box: bool
    out_box: bool
    
    # Object physical properties
    is_fragile: bool
    is_foldable: bool
    is_elastic: bool
    is_soft: bool
    is_rigid: bool


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
        if obj.object_type != 'box' and obj.out_box and self.robot_handempty:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
            obj.out_box = False
            obj.in_box = False
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if obj.object_type != 'box' and self.robot_now_holding == obj:
            if obj.is_rigid:
                if any(o.is_soft for o in bin.in_bin_objects):
                    print(f"Place {obj.name} in {bin.name}")
                    bin.in_bin_objects.append(obj)
                    self.state_handempty()
                    obj.in_box = True
                    obj.out_box = False
                else:
                    print(f"Cannot place {obj.name} in {bin.name} without a soft object")
            else:
                print(f"Place {obj.name} in {bin.name}")
                bin.in_bin_objects.append(obj)
                self.state_handempty()
                obj.in_box = True
                obj.out_box = False
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
        if self.robot_handempty and obj.is_foldable and not obj.in_box:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj.in_box and obj in bin.in_bin_objects:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            self.state_holding(obj)
            obj.in_box = False
            obj.out_box = True
            self.state_handempty()
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='white_3D_cylinder', 
    color='white', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=False, 
    out_box=True, 
    is_fragile=False, 
    is_foldable=False, 
    is_elastic=True, 
    is_soft=True, 
    is_rigid=False
)

object1 = Object(
    index=1, 
    name='green_3D_cylinder', 
    color='green', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=False, 
    out_box=True, 
    is_fragile=True, 
    is_foldable=False, 
    is_elastic=False, 
    is_soft=False, 
    is_rigid=True
)

object2 = Object(
    index=2, 
    name='yellow_2D_rectangle', 
    color='yellow', 
    shape='2D_rectangle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=True, 
    out_box=False, 
    is_fragile=False, 
    is_foldable=True, 
    is_elastic=False, 
    is_soft=False, 
    is_rigid=False
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=False, 
    out_box=False, 
    is_fragile=False, 
    is_foldable=False, 
    is_elastic=False, 
    is_soft=False, 
    is_rigid=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0: in_box=True, pushed=True
    # object1: in_box=True, pushed=True
    # object2: in_box=True, pushed=True, folded=True
    # object3: box, no change

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Fold the yellow_2D_rectangle (object2) since it is foldable and not in the bin.
    # 2. Pick and place the white_3D_cylinder (object0) into the box.
    # 3. Push the white_3D_cylinder (object0) in the box.
    # 4. Pick and place the green_3D_cylinder (object1) into the box.
    # 5. Push the green_3D_cylinder (object1) in the box.
    # 6. Pick and place the yellow_2D_rectangle (object2) into the box.
    # 7. Push the yellow_2D_rectangle (object2) in the box.

    # Third, make your order, you should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # Fourth, after making all actions, fill your reasons according to the rules
    # Rule 3: Fold the foldable object (yellow_2D_rectangle) on the platform
    robot.fold(object2, box)

    # Rule 5: Pick, place, and push the soft object (white_3D_cylinder) into the bin
    robot.pick(object0, box)
    robot.place(object0, box)
    robot.push(object0, box)

    # Rule 2: Place the rigid object (green_3D_cylinder) into the bin after a soft object is already in the bin
    robot.pick(object1, box)
    robot.place(object1, box)
    robot.push(object1, box)

    # Rule 5: Pick, place, and push the foldable object (yellow_2D_rectangle) into the bin
    robot.pick(object2, box)
    robot.place(object2, box)
    robot.push(object2, box)

    # Finally, check if the goal state is satisfying goal state table
    assert object0.in_box == True
    assert object0.pushed == True
    assert object1.in_box == True
    assert object1.pushed == True
    assert object2.in_box == True
    assert object2.pushed == True
    assert object2.folded == True
    assert object3.in_box == False  # The box itself should not be in another box

    print("All task planning is done")
