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
        if self.robot_handempty and obj.is_out_box and obj.object_type != 'box':
            # Effects
            self.state_holding(obj)
            obj.is_out_box = False
            obj.is_in_box = False
            print(f"Pick {obj.name}")
    
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj:
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
        if self.robot_handempty and obj.is_soft:
            # Effects
            print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and not self.robot_handempty and self.robot_now_holding == obj:
            # Effects
            self.state_handempty()
            obj.is_in_box = False
            obj.is_out_box = True
            print(f"Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


# Create objects based on the initial state table
object0 = Object(index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', is_soft=True, is_out_box=True)
object1 = Object(index=1, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', is_rigid=True, is_out_box=True)
object2 = Object(index=2, name='white_1D_ring', color='white', shape='1D_ring', object_type='obj', is_elastic=True, is_out_box=True)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', is_in_box=True, is_out_box=False)

# Create a bin object (assuming bin is also an object)
bin = Object(index=4, name='bin', color='gray', shape='box', object_type='box')

if __name__ == "__main__":
    # Initialize the robot
    robot = Robot()

    # First, using goal table, describe the final state of each object
    goal_state = {
        object0.name: {'is_in_box': True, 'is_out_box': False},
        object1.name: {'is_in_box': True, 'is_out_box': False},
        object2.name: {'is_in_box': False, 'is_out_box': True},
        object3.name: {'is_in_box': True, 'is_out_box': False},
    }

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'.
    # According to rule 4, we should pick the rigid object first if it's not in the bin initially.
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # Now, we can pick and place the soft object
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # The elastic object should remain out of the box, so no action is needed for object2

    # The box (object3) is already in the bin, so no action is needed for object3

    # after making all actions, fill your reasons according to the rules
    # Reason for picking and placing object1 first: Rule 4 states that when a rigid object is not in the bin at the initial state, pick a rigid object first.
    # Reason for picking and placing object0 next: After handling the rigid object, we can handle the soft object.
    # No action for object2: The goal state indicates it should remain out of the box.
    # No action for object3: The box is already in the bin as per the initial state.

    # check if the goal state is satisfying goal state table
    assert object0.is_in_box == goal_state[object0.name]['is_in_box']
    assert object0.is_out_box == goal_state[object0.name]['is_out_box']
    assert object1.is_in_box == goal_state[object1.name]['is_in_box']
    assert object1.is_out_box == goal_state[object1.name]['is_out_box']
    assert object2.is_in_box == goal_state[object2.name]['is_in_box']
    assert object2.is_out_box == goal_state[object2.name]['is_out_box']
    assert object3.is_in_box == goal_state[object3.name]['is_in_box']
    assert object3.is_out_box == goal_state[object3.name]['is_out_box']

    print("All objects are in their goal states.")
