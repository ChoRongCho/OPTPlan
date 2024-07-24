from dataclasses import dataclass, field

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj
    
    # Basic effect predicates for obj
    pushed: bool = False
    folded: bool = False
    
    # Predicates for box
    in_bin_objects: list = field(default_factory=list)
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    is_rigid: bool = False
    is_foldable: bool = False
    
    # Object physical properties
    init_pose: str = 'out_box'


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
        if self.robot_handempty and obj.init_pose == 'out_box' and obj.object_type != 'box':
            # Effects
            self.state_holding(obj)
            obj.init_pose = 'in_hand'
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and obj.object_type != 'box':
            if obj.is_rigid:
                if all(o.is_rigid or o.init_pose == 'in_bin' for o in bin.in_bin_objects):
                    # Effects
                    self.state_handempty()
                    obj.init_pose = 'in_bin'
                    bin.in_bin_objects.append(obj)
                    print(f"Place {obj.name in bin.name}")
                else:
                    print(f"Cannot Place {obj.name} because not all soft objects are in the bin")
            else:
                # Effects
                self.state_handempty()
                obj.init_pose = 'in_bin'
                bin.in_bin_objects.append(obj)
                print(f"Place {obj.name in bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.init_pose == 'in_bin' and not obj.is_rigid:
            if not any(o.init_pose == 'on_top' for o in bin.in_bin_objects):
                # Effects
                obj.pushed = True
                print(f"Push {obj.name}")
            else:
                print(f"Cannot Push {obj.name} because there is a fragile object on top")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.init_pose == 'in_bin' and obj.is_foldable:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj.init_pose == 'in_bin' and obj in bin.in_bin_objects:
            # Effects
            self.state_holding(obj)
            obj.init_pose = 'out_box'
            bin.in_bin_objects.remove(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', init_pose='out_box', is_foldable=True)
object1 = Object(index=1, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', init_pose='out_box', is_rigid=True)
object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', init_pose='box')

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    print("Initial State:")
    print(f"{object0.name}: {object0.init_pose}")
    print(f"{object1.name}: {object1.init_pose}")
    print(f"{object2.name}: {object2.init_pose}")

    # Goal state
    print("\nGoal State:")
    print(f"{object0.name}: in_box, Pushed: True, Folded: True")
    print(f"{object1.name}: in_box")
    print(f"{object2.name}: box, In Bin Objects: [{object0.name}, {object1.name}]")

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Pick and place the yellow_2D_rectangle (soft object) in the box
    # 2. Push the yellow_2D_rectangle to make space
    # 3. Fold the yellow_2D_rectangle
    # 4. Pick and place the yellow_3D_cylinder (rigid object) in the box

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object2

    # Action sequence
    robot.pick(object0, box)  # Pick yellow_2D_rectangle
    robot.place(object0, box)  # Place yellow_2D_rectangle in the box
    robot.push(object0, box)  # Push yellow_2D_rectangle to make space
    robot.fold(object0, box)  # Fold yellow_2D_rectangle
    robot.pick(object1, box)  # Pick yellow_3D_cylinder
    robot.place(object1, box)  # Place yellow_3D_cylinder in the box

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. Pick and place the yellow_2D_rectangle first because it is a soft object and must be in the box before placing the rigid object.
    # 2. Push the yellow_2D_rectangle to make more space in the box.
    # 3. Fold the yellow_2D_rectangle as it is foldable.
    # 4. Pick and place the yellow_3D_cylinder after the soft object is already in the box.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.init_pose == 'in_bin'
    assert object0.pushed == True
    assert object0.folded == True
    assert object1.init_pose == 'in_bin'
    assert object2.in_bin_objects == [object0, object1]
    print("All task planning is done")
