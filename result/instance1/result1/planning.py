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
    is_flexible: bool = False
    is_elastic: bool = False

    # bin_packing predicates expressed as a boolean (max 2)
    is_in_box: bool = False
    is_out_box: bool = True

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
        if obj.object_type != "box" and obj.is_out_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.is_out_box = False
            obj.is_in_box = False
            print(f"Pick {obj.name}")
    
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and obj.object_type != "box":
            # Effects
            self.state_handempty()
            obj.is_in_box = True
            obj.is_out_box = False
            print(f"Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if obj.is_soft and self.robot_handempty and not obj.is_rigid and not obj.is_elastic:
            # Effects
            print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_flexible:
            # Effects
            print(f"Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and obj.object_type != "box":
            # Effects
            self.state_holding(obj)
            obj.is_in_box = False
            obj.is_out_box = True
            print(f"Out {obj.name} from {bin.name}")
    def dummy(self):
        pass


# Initialize objects
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', is_soft=True, is_out_box=True)
object1 = Object(index=1, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', is_rigid=True, is_out_box=True)
object2 = Object(index=2, name='blue_1D_ring', color='blue', shape='1D_ring', object_type='obj', is_elastic=True, is_flexible=True, is_out_box=True)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', is_in_box=True, is_out_box=False)

# Initialize robot
robot = Robot()

if __name__ == "__main__":
    # Using goal table, Describe the final state of each object
    # Goal: 
    # yellow_3D_cuboid (soft) -> in_box
    # black_3D_cylinder (rigid) -> in_box
    # blue_1D_ring (elastic, flexible) -> out_box
    # white_box -> box (unchanged)

    # make your order
    # Step 1: Push the yellow_3D_cuboid (soft) to make space in the box
    robot.push(object0, object3)
    
    # Step 2: Pick and place the yellow_3D_cuboid (soft) in the box
    robot.pick(object0, object3)
    robot.place(object0, object3)
    
    # Step 3: Pick and place the blue_1D_ring (elastic, flexible) out of the box
    robot.pick(object2, object3)
    robot.out(object2, object3)
    
    # Step 4: Pick and place the black_3D_cylinder (rigid) in the box
    robot.pick(object1, object3)
    robot.place(object1, object3)
    
    # after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. Never attempt to pick up and set down an object named box: Followed, no actions on white_box.
    # 2. When placing a rigid object in the bin, the soft objects must be in the bin before: Followed, yellow_3D_cuboid (soft) is placed before black_3D_cylinder (rigid).
    # 3. Do not place a fragile object if there is no elastic object in the bin: Not applicable, no fragile objects.
    # 4. You must push a soft object to make more space in the bin, however, if there is a fragile object on the soft object, you must not push the object when pushing an object, neither fragile nor rigid objects are permitted: Followed, pushed yellow_3D_cuboid (soft) first.

    # check if the goal state is satisfied using goal state table
    assert object0.is_in_box == True and object0.is_out_box == False
    assert object1.is_in_box == True and object1.is_out_box == False
    assert object2.is_in_box == False and object2.is_out_box == True
    assert object3.is_in_box == True and object3.is_out_box == False

    print("Goal state achieved.")
