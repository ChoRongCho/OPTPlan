from dataclasses import dataclass

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj

    # Object physical properties predicates
    is_rigid: bool = False
    is_soft: bool = False
    is_fragile: bool = False

    # bin_packing predicates expressed as a boolean (max 2)
    is_in_box: bool = False
    is_packable: bool = True


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
        if self.robot_handempty and not obj.is_in_box and obj.object_type != 'box':
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and obj.object_type != 'box':
            # Effects
            obj.is_in_box = True
            self.state_handempty()
            print(f"Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_soft and not obj.is_fragile and not obj.is_rigid:
            # Effects
            obj.is_in_box = True
            print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_packable:
            # Effects
            obj.is_packable = False
            print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and not self.robot_handempty:
            # Effects
            obj.is_in_box = False
            self.state_handempty()
            print(f"Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


object0 = Object(index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', is_soft=True, is_in_box=False)
object1 = Object(index=1, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', is_rigid=True, is_fragile=True, is_in_box=False)
object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', is_in_box=True)

if __name__ == "__main__":
    # Initialize the robot
    robot = Robot()

    # First, using goal table, describe the final state of each object
    goal_state = {
        object0.name: 'in_box',
        object1.name: 'in_box',
        object2.name: 'box'  # The box itself remains as a box
    }

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'.
    # According to the rules:
    # 1. Don't pick and place a box called bin.
    # 2. When placing a rigid object in the bin, the soft objects must be in the bin before.
    # 3. When folding an object, the object must be foldable.
    # 4. When pushing an object, neither fragile nor rigid objects are permitted, but only soft objects are permitted.

    # Step 1: Push the soft object (red_3D_polyhedron) into the box
    robot.push(object0, object2)

    # Step 2: Pick and place the rigid and fragile object (green_3D_cylinder) into the box
    robot.pick(object1, object2)
    robot.place(object1, object2)

    # after making all actions, fill your reasons according to the rules
    # Reason for Step 1: According to rule 4, we can push the soft object (red_3D_polyhedron) into the box.
    # Reason for Step 2: According to rule 2, we can place the rigid object (green_3D_cylinder) into the box only after the soft object is in the box.

    # check if the goal state is satisfying goal state table
    assert object0.is_in_box == True, f"{object0.name} is not in the box"
    assert object1.is_in_box == True, f"{object1.name} is not in the box"
    assert object2.is_in_box == True, f"{object2.name} is not in the box"  # The box itself should remain as a box

    print("All objects are in the correct final state.")
