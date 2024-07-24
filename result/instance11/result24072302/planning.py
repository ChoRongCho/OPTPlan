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
        if not self.robot_handempty and self.robot_now_holding == obj:
            if obj.is_rigid:
                if any(o.is_soft for o in bin.in_bin_objects):
                    # Effects
                    self.state_handempty()
                    obj.in_box = True
                    bin.in_bin_objects.append(obj)
                    print(f"Place {obj.name in bin.name}")
                else:
                    print(f"Cannot Place {obj.name} because no soft objects in bin")
            else:
                # Effects
                self.state_handempty()
                obj.in_box = True
                bin.in_bin_objects.append(obj)
                print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.in_box and obj.is_soft:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.in_box and obj.is_elastic:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj in bin.in_bin_objects:
            # Effects
            self.state_holding(obj)
            obj.in_box = False
            bin.in_bin_objects.remove(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

# Reason:
# The robot actions are designed to follow the given rules strictly. The 'pick' action ensures the robot's hand is empty and the object is not in the bin. The 'place' action checks if the object is rigid and ensures soft objects are already in the bin before placing a rigid object. The 'push' action is used for soft objects already in the bin, and the 'fold' action is for elastic objects. The 'out' action removes an object from the bin and places it on the platform, ensuring the robot's hand is empty afterward. These actions ensure compliance with the rules and maintain the logical flow of the bin-packing task.

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='black_3D_cylinder', 
    color='black', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=True, 
    is_elastic=False, 
    is_soft=False, 
    init_pose='out_box', 
    in_box=False
)

object1 = Object(
    index=1, 
    name='white_3D_cylinder', 
    color='white', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=False, 
    is_elastic=True, 
    is_soft=True, 
    init_pose='out_box', 
    in_box=False
)

object2 = Object(
    index=2, 
    name='red_3D_polyhedron', 
    color='red', 
    shape='3D_polyhedron', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=False, 
    is_elastic=False, 
    is_soft=True, 
    init_pose='in_box', 
    in_box=True
)

white_box = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[object2], 
    is_rigid=False, 
    is_elastic=False, 
    is_soft=False, 
    init_pose='box', 
    in_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    # object0: out_box, not in box
    # object1: out_box, not in box
    # object2: in_box, in box
    # white_box: contains object2

    # Goal State
    # object0: in_box
    # object1: in_box, pushed
    # object2: out_box, not in box
    # white_box: contains object0 and object1

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Push the red_3D_polyhedron (object2) out of the way since it is soft and already in the box.
    # 2. Pick and place the white_3D_cylinder (object1) into the box.
    # 3. Push the white_3D_cylinder (object1) since it is soft.
    # 4. Pick and place the black_3D_cylinder (object0) into the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = white_box

    # c) Action sequence
    # Step 1: Push the red_3D_polyhedron (object2) out of the way
    robot.push(object2, box)
    robot.out(object2, box)

    # Step 2: Pick and place the white_3D_cylinder (object1) into the box
    robot.pick(object1, box)
    robot.place(object1, box)

    # Step 3: Push the white_3D_cylinder (object1) since it is soft
    robot.push(object1, box)

    # Step 4: Pick and place the black_3D_cylinder (object0) into the box
    robot.pick(object0, box)
    robot.place(object0, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason:
    # 1. The red_3D_polyhedron (object2) is pushed out of the way because it is soft and already in the box.
    # 2. The white_3D_cylinder (object1) is placed in the box because it is soft and can be placed without any conditions.
    # 3. The white_3D_cylinder (object1) is pushed because it is soft.
    # 4. The black_3D_cylinder (object0) is placed in the box after the white_3D_cylinder (object1) because it is rigid and requires a soft object to be in the box first.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == False
    assert object1.pushed == True
    assert object2.pushed == False
    assert object2.folded == False
    assert object1.folded == False
    assert object0.folded == False
    assert object0.pushed == False
    assert object1.pushed == True
    assert object2.pushed == False
    assert object0 in box.in_bin_objects
    assert object1 in box.in_bin_objects
    assert object2 not in box.in_bin_objects
    print("All task planning is done")