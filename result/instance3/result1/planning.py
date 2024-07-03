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
        if obj.object_type != 'box' and obj.is_out_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.is_out_box = False
            obj.is_in_box = False
            print(f"Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and not obj.is_in_box:
            # Effects
            self.state_handempty()
            obj.is_in_box = True
            obj.is_out_box = False
            print(f"Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_in_box:
            # Effects
            print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_flexible:
            # Effects
            print(f"Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and obj.is_rigid:
            # Effects
            self.state_holding(obj)
            obj.is_in_box = False
            obj.is_out_box = True
            print(f"Out {obj.name} from {bin.name}")
    def dummy(self):
        pass


object0 = Object(index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', is_soft=True, is_out_box=True, is_in_box=False)
object1 = Object(index=1, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', is_rigid=True, is_out_box=True, is_in_box=False)
object2 = Object(index=2, name='white_1D_ring', color='white', shape='1D_ring', object_type='obj', is_elastic=True, is_flexible=True, is_out_box=True, is_in_box=False)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', is_out_box=False, is_in_box=True)

if __name__ == '__main__':
    # Initialize the robot
    robot = Robot()

    # Step 1: Out the rigid object (yellow_3D_cylinder) from the box and replace it into the box
    robot.out(object1, object3)  # Out yellow_3D_cylinder from white_box
    robot.place(object1, object3)  # Place yellow_3D_cylinder in white_box

    # Step 2: Pick and place the soft object (red_3D_polyhedron) into the box
    robot.pick(object0, object3)  # Pick red_3D_polyhedron
    robot.place(object0, object3)  # Place red_3D_polyhedron in white_box

    # Step 3: Fold the flexible object (white_1D_ring) (Note: This step is not necessary for the goal but included for completeness)
    robot.fold(object2, object3)  # Fold white_1D_ring

    # Final state of each object
    print(f"Final state of {object0.name}: in_box={object0.is_in_box}, out_box={object0.is_out_box}")
    print(f"Final state of {object1.name}: in_box={object1.is_in_box}, out_box={object1.is_out_box}")
    print(f"Final state of {object2.name}: in_box={object2.is_in_box}, out_box={object2.is_out_box}")
    print(f"Final state of {object3.name}: in_box={object3.is_in_box}, out_box={object3.is_out_box}")

    # Check if the goal state is satisfied
    goal_state = {
        object0.name: object0.is_in_box,
        object1.name: object1.is_in_box,
        object2.name: object2.is_out_box,
        object3.name: object3.is_in_box
    }

    expected_goal_state = {
        'red_3D_polyhedron': True,
        'yellow_3D_cylinder': True,
        'white_1D_ring': False,
        'white_box': True
    }

    if goal_state == expected_goal_state:
        print("Goal state is satisfied.")
    else:
        print("Goal state is not satisfied.")
