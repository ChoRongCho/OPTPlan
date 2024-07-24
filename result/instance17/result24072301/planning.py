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
    is_packed: bool
    
    # Object physical properties 
    is_elastic: bool
    is_soft: bool
    is_foldable: bool


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
        if self.robot_handempty and not obj.in_box:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj:
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
        if self.robot_handempty and obj.is_foldable:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj.in_box and obj in bin.in_bin_objects:
            # Effects
            self.state_holding(obj)
            obj.in_box = False
            bin.in_bin_objects.remove(obj)
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

# Reason:
# The robot actions are designed to follow the given rules strictly. The 'pick' action ensures the robot's hand is empty and the object is not already in the bin. The 'place' action checks that the robot is holding the object before placing it in the bin. The 'push' action ensures that only soft objects already in the bin can be pushed. The 'fold' action ensures that only foldable objects can be folded. The 'out' action allows the robot to remove objects from the bin, ensuring they are in the bin before doing so. These actions ensure the robot follows the rules for bin packing, such as not picking and placing boxes, pushing soft objects before packing, and handling rigid objects correctly

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='yellow_3D_cuboid', 
    color='yellow', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=False, 
    is_packed=False, 
    is_elastic=True, 
    is_soft=True, 
    is_foldable=False
)

object1 = Object(
    index=1, 
    name='white_2D_ring', 
    color='white', 
    shape='2D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=False, 
    is_packed=False, 
    is_elastic=True, 
    is_soft=False, 
    is_foldable=False
)

object2 = Object(
    index=2, 
    name='blue_2D_ring', 
    color='blue', 
    shape='2D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=False, 
    is_packed=False, 
    is_elastic=False, 
    is_soft=False, 
    is_foldable=False
)

object3 = Object(
    index=3, 
    name='white_2D_circle', 
    color='white', 
    shape='2D_circle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=True, 
    is_packed=False, 
    is_elastic=True, 
    is_soft=False, 
    is_foldable=True
)

object4 = Object(
    index=4, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=False, 
    is_packed=False, 
    is_elastic=False, 
    is_soft=False, 
    is_foldable=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state is already described in the given data

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Out the white_2D_circle from the box
    # 2. Push the yellow_3D_cuboid (since it is soft) before placing it in the box
    # 3. Place the white_2D_ring in the box
    # 4. Fold the white_2D_circle and place it back in the box

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box, this is an example. 
    box = object4

    # Action sequence
    # 1. Out the white_2D_circle from the box
    robot.out(object3, box)
    
    # 2. Push the yellow_3D_cuboid (since it is soft) before placing it in the box
    robot.pick(object0, box)
    robot.place(object0, box)
    robot.push(object0, box)
    
    # 3. Place the white_2D_ring in the box
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # 4. Fold the white_2D_circle and place it back in the box
    robot.fold(object3, box)
    robot.pick(object3, box)
    robot.place(object3, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason:
    # 1. The white_2D_circle was initially in the box and needed to be taken out and placed back in after folding.
    # 2. The yellow_3D_cuboid is soft, so it needed to be pushed before being packed in the bin.
    # 3. The white_2D_ring is a rigid object and can be directly placed in the box.
    # 4. The white_2D_circle is foldable and needed to be folded before being placed back in the box.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object0.pushed == True
    assert object1.in_box == True
    assert object2.in_box == False
    assert object3.in_box == True
    assert object3.folded == True
    assert object4.in_box == False
    print("All task planning is done")
