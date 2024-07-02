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
    is_fragile: bool
    is_foldable: bool
    is_elastic: bool
    is_soft: bool

    # bin_packing predicates expressed as a boolean (max 2)
    is_in_box: bool
    is_heavy: bool

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
    
    def pick(self, obj):
        # Preconditions
        assert self.robot_handempty, "Robot hand must be empty to pick an object."
        assert not obj.is_in_box, "Object must not be in the bin to be picked."
        assert obj.object_type != 'box', "You should never pick a box."
        
        # Effects
        self.state_holding(obj)
        obj.is_in_box = False
        print(f"Pick {obj.name}")
        
    def place(self, obj, bins):
        # Preconditions
        assert not self.robot_handempty, "Robot hand must not be empty to place an object."
        assert obj.object_type != 'box', "You should never place a box."
        if not obj.is_soft:
            assert any(o.is_soft and o.is_in_box for o in bins), "Soft objects must be in the bin before placing rigid objects."
        
        # Effects
        self.state_handempty()
        obj.is_in_box = True
        print(f"Place {obj.name} in {bins.name}")
    
    def push(self, obj):
        # Preconditions
        assert self.robot_handempty, "Robot hand must be empty when pushing."
        assert obj.is_soft, "Only soft objects can be pushed."
        assert not any(o.is_fragile and o.is_in_box for o in bins), "Must not push if there is a fragile object on the soft object."
        
        # Effects
        print(f"Push {obj.name}")
    
    def fold(self, obj):
        # Preconditions
        assert self.robot_handempty, "Robot hand must be empty when folding."
        assert obj.is_foldable, "Object must be foldable."
        assert any(o.is_fragile and o.is_in_box for o in bins), "Fragile objects must be in the bin when folding a foldable object."
        
        # Effects
        print(f"Fold {obj.name}")
    
    def out(self, obj, bins):
        # Preconditions
        assert obj.is_in_box, "Object must be in the bin to be taken out."
        
        # Effects
        self.state_holding(obj)
        obj.is_in_box = False
        print(f"Out {obj.name} from {bins.name}")
    def dummy(self):
        pass


# Create objects based on the initial state table
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', is_fragile=False, is_foldable=True, is_elastic=False, is_soft=True, is_in_box=False, is_heavy=False)
object1 = Object(index=1, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', is_fragile=True, is_foldable=False, is_elastic=False, is_soft=False, is_in_box=False, is_heavy=False)
object2 = Object(index=2, name='blue_1D_ring', color='blue', shape='1D_ring', object_type='obj', is_fragile=True, is_foldable=False, is_elastic=True, is_soft=False, is_in_box=False, is_heavy=False)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', is_fragile=False, is_foldable=False, is_elastic=False, is_soft=True, is_in_box=True, is_heavy=False)

# List of objects
objects = [object0, object1, object2, object3]

# Create the robot
robot = Robot()

```python
if __name__ == '__main__':
    # Step-by-step plan to pack all objects into the bin following the rules

    # Step 1: Pick and place the yellow_3D_cuboid (soft object)
    robot.pick(object0)
    robot.place(object0, object3)

    # Step 2: Pick and place the black_3D_cylinder (fragile object)
    robot.pick(object1)
    robot.place(object1, object3)

    # Step 3: Pick and place the blue_1D_ring (fragile and elastic object)
    robot.pick(object2)
    robot.place(object2, object3)

    # All objects are now packed into the bin
```

This plan follows the rules and ensures that all objects are packed into the bin in the correct order. The soft object (yellow_3D_cuboid) is placed first, followed by the fragile objects (black_3D_cylinder and blue_1D_ring).
