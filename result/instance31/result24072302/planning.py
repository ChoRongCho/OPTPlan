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
    is_elastic: bool
    is_foldable: bool
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
        # Preconditions: Robot hand must be empty, object must not be in the bin
        if self.robot_handempty and not obj.in_box:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions: Robot must be holding the object
        if self.robot_now_holding == obj:
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin_objects.append(obj)
            obj.in_box = True
            self.state_handempty()
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions: Robot hand must be empty, object must be in the bin
        if self.robot_handempty and obj.in_box:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions: Robot hand must be empty, object must be foldable
        if self.robot_handempty and obj.is_foldable:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions: Object must be in the bin
        if obj.in_box:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_holding(obj)
            self.state_handempty()
        else:
            print(f"Cannot Out {obj.name}")

# Reason:
# The robot actions are designed to follow the given rules strictly. The preconditions ensure that actions are only performed when the robot is in the correct state and the objects meet the necessary criteria. For example, the robot cannot pick an object if it is already holding something, and it cannot fold an object unless it is foldable. These constraints ensure that the robot operates within the defined rules, preventing actions that would violate the task requirements. The effects update the state of the robot and objects to reflect the changes made by each action, ensuring consistency in the task planning process.

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_elastic=False, is_foldable=False, in_box=False)
object1 = Object(index=1, name='white_2D_ring', color='white', shape='2D_ring', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_elastic=True, is_foldable=False, in_box=False)
object2 = Object(index=2, name='blue_1D_linear', color='blue', shape='1D_linear', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_elastic=False, is_foldable=True, in_box=False)
object3 = Object(index=3, name='black_2D_ring', color='black', shape='2D_ring', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_elastic=True, is_foldable=False, in_box=True)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[object3], is_rigid=False, is_elastic=False, is_foldable=False, in_box=False)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state is already described in the given table.
    # Final state:
    # object0: in_box = True
    # object1: in_box = True
    # object2: in_box = True
    # object3: in_box = True
    # object4: in_bin_objects = [object0, object1, object2, object3]

    # Second, using given rules and object's states, make a task planning strategy
    # Rule 1: It is prohibited to lift and relocate a container.
    # Rule 2: When fold an object, the object must be foldable.
    # Rule 3: When place a fragile object, the soft objects must be in the bin.
    # Rule 4: When a soft object is in the bin at the initial state, out of the soft object and replace it into the bin.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object4

    # c) Action sequence
    # Step 1: Out the black_2D_ring (object3) from the box (Rule 4)
    robot.out(object3, box)

    # Step 2: Pick and place the yellow_3D_cylinder (object0) into the box
    robot.pick(object0, box)
    robot.place(object0, box)

    # Step 3: Pick and place the white_2D_ring (object1) into the box
    robot.pick(object1, box)
    robot.place(object1, box)

    # Step 4: Fold the blue_1D_linear (object2) and place it into the box (Rule 2)
    robot.fold(object2, box)
    robot.pick(object2, box)
    robot.place(object2, box)

    # Step 5: Place the black_2D_ring (object3) back into the box (Rule 4)
    robot.pick(object3, box)
    robot.place(object3, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason for Step 1: Rule 4 requires us to out the soft object initially in the bin and replace it.
    # Reason for Step 2: We need to place the yellow_3D_cylinder into the box to achieve the goal state.
    # Reason for Step 3: We need to place the white_2D_ring into the box to achieve the goal state.
    # Reason for Step 4: The blue_1D_linear is foldable, and we need to fold it before placing it into the box.
    # Reason for Step 5: Rule 4 requires us to replace the black_2D_ring back into the box after other objects are placed.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_bin_objects == [object0, object1, object2, object3]
    print("All task planning is done")
