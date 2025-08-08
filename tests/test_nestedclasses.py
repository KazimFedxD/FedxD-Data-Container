from __future__ import annotations

from typing import Any, Optional

from fxdc import Config, dumps, loads

emojis = {}


@Config.add_class
class Item:
    def __init__(self, name: str):
        self.name = name

    @property
    def max_stack(self) -> int:
        if type(self) in [Tool, Armor] or "bucket" in self.name:
            return 1
        if type(self) in [Potion]:
            return 16
        return 64

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Item):
            return False
        return self.name == other.name

    def copy(self) -> Item:
        return Item(self.name)


@Config.add_class
class Block(Item):
    def __init__(
        self,
        name: str,
        rarity: int,
        startingY: int,
        endingY: int,
        item: Optional[Item] = None,
        itemrange: tuple[int, int] | int = 1,
        hardness: int | float = 1,
    ):
        super().__init__(name)
        self.rarity = rarity
        self.startingY = startingY
        self.endingY = endingY
        self.item = item
        self.itemrange = itemrange
        self.hardness = hardness

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Block):
            return False
        return (
            self.name == other.name
            and self.rarity == other.rarity
            and self.startingY == other.startingY
            and self.endingY == other.endingY
            and self.item == other.item
            and self.itemrange == other.itemrange
            and self.hardness == other.hardness
        )

    def copy(self) -> Block:
        return Block(
            self.name,
            self.rarity,
            self.startingY,
            self.endingY,
            self.item,
            self.itemrange,
            self.hardness,
        )


@Config.add_class
class Enchantment:
    def __init__(self, name: str, level: int):
        self.name = name
        self.level = level

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Enchantment):
            return False
        return self.name == other.name and self.level == other.level

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f"{self.name} {self.level}"

    def __str__(self) -> str:
        return f"{self.name}"


@Config.add_class
class Tool(Item):
    def __init__(
        self,
        name: str,
        durability: int,
        damage: int,
        speed: int,
        enchantments: list[Enchantment] = [],
    ):
        super().__init__(name)
        self.durability = durability
        self.damage = damage
        self.speed = speed
        self.enchantments = enchantments

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tool):
            return False
        return self.name == other.name and self.enchantments == other.enchantments

    def copy(self) -> Tool:
        return Tool(
            self.name, self.durability, self.damage, self.speed, self.enchantments
        )


@Config.add_class
class Armor(Item):
    def __init__(
        self,
        name: str,
        type: str,
        durability: int,
        defense: int,
        enchantments: list[Enchantment] = [],
    ):
        super().__init__(name)
        self.type = type
        self.durability = durability
        self.defense = defense
        self.enchantments = enchantments

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Armor):
            return False
        return self.name == other.name and self.enchantments == other.enchantments

    def copy(self) -> Armor:
        return Armor(
            self.name, self.type, self.durability, self.defense, self.enchantments
        )


@Config.add_class
class Consumable(Item):
    def __init__(self, name: str, effect: str, duration: int):
        super().__init__(name)
        self.effect = effect
        self.duration = duration

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Consumable):
            return False
        return (
            self.name == other.name
            and self.effect == other.effect
            and self.duration == other.duration
        )


@Config.add_class
class Food(Consumable):
    def __init__(self, name: str, health: int, hunger: int):
        super().__init__(name, "food", 0)
        self.health = health
        self.hunger = hunger

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Food):
            return False
        return (
            self.name == other.name
            and self.health == other.health
            and self.hunger == other.hunger
        )

    def __todata__(self) -> dict[str, Any]:
        return {"name": self.name, "health": self.health, "hunger": self.hunger}


@Config.add_class
class Potion(Consumable):
    def __init__(self, name: str, effect: str, duration: int, level: int = 1):
        super().__init__(name, effect, duration)
        self.level = level

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Potion):
            return False
        return (
            self.name == other.name
            and self.effect == other.effect
            and self.duration == other.duration
            and self.level == other.level
        )


@Config.add_class
class Fluid(Item):
    def __init__(self, name: str, damage: int, rarity: int):
        super().__init__(name)
        self.damage = damage
        self.rarity = rarity

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Fluid):
            return False
        return (
            self.name == other.name
            and self.damage == other.damage
            and self.rarity == other.rarity
        )


@Config.add_class
class Stack:
    def __init__(self, item: Item, amount: int):
        self.item = item
        self.amount = amount

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Stack):
            return False
        return self.item == other.item

    def add(self):
        if self.amount < self.item.max_stack:
            self.amount += 1
            return True
        return False

    def adds(self, amount: int) -> int:
        self.amount += amount
        if self.amount > self.item.max_stack:
            remainder = self.amount - self.item.max_stack
            self.amount = self.item.max_stack
            return remainder
        return 0

    def __str__(self):
        return f"{self.item.name} x{self.amount}"

    def __repr__(self):
        return f"{self.item.name} x{self.amount}"


@Config.add_class
class Inventory:
    def __init__(self):
        self.items: list[Stack] = []
        self.max_slots = 36

    @staticmethod
    def __fromdata__(**data: Any) -> Inventory:
        inv = Inventory()
        if data.get("items"):
            inv.items = data["items"]
        if data.get("max_slots"):
            inv.max_slots = data["max_slots"]
        return inv

    def __todata__(self) -> dict[str, Any]:
        return {"items": self.items, "max_slots": self.max_slots}

    def add(self, item: Item, amount: int = 1):
        for stack in self.items:
            if stack.item == item:
                remainder = stack.adds(amount)
                if remainder == 0:
                    return
                amount = remainder
        if amount == 0:
            return
        if len(self.items) == self.max_slots:
            raise Exception("Inventory is full")
        self.items.append(Stack(item, amount))

    def remove(self, item: Item, amount: int = 1):
        for stack in self.items:
            if stack.item == item:
                stack.amount -= amount
                if stack.amount < 0:
                    remainder = abs(stack.amount)
                    amount = remainder
                    stack.amount = 0
                if stack.amount == 0:
                    self.items.remove(stack)
            if amount == 0:
                break
        if amount:
            raise Exception("Not enough items in inventory")
        else:
            return

    def __str__(self):
        return "\n".join([str(stack) for stack in self.items])

    def __repr__(self):
        return "\n".join([repr(stack) for stack in self.items])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Inventory):
            return False
        return self.items == other.items

    def __hash__(self) -> int:
        return hash(tuple(self.items))

    def copy(self) -> Inventory:
        inv = Inventory()
        inv.items = [stack for stack in self.items]
        return inv

    def __getitem__(self, item: Item) -> int:
        for stack in self.items:
            if stack.item == item:
                return stack.amount
        return 0


@Config.add_class
class Player:
    def __init__(self, name: str, inventory: Inventory):
        self.name = name
        self.inventory = inventory
        self.hunger = 20
        self.health = 20
        self.helmet = None
        self.chestplate = None
        self.leggings = None
        self.boots = None
        self.pickaxe = None
        self.sword = None
        self.reserved_armor = []
        self.reserved_tools = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: Player) -> bool:
        if not isinstance(other, Player):
            return False
        return (
            self.name == other.name
            and self.inventory == other.inventory
            and self.hunger == other.hunger
            and self.health == other.health
            and self.helmet == other.helmet
            and self.chestplate == other.chestplate
            and self.leggings == other.leggings
            and self.boots == other.boots
            and self.pickaxe == other.pickaxe
            and self.sword == other.sword
            and self.reserved_armor == other.reserved_armor
            and self.reserved_tools == other.reserved_tools
        )

    @staticmethod
    def __fromdata__(**data: Any) -> Player:
        player = Player(data["name"], data["inventory"])
        if data.get("hunger"):
            player.hunger = data["hunger"]
        if data.get("health"):
            player.health = data["health"]
        if data.get("helmet"):
            player.helmet = data["helmet"]
        if data.get("chestplate"):
            player.chestplate = data["chestplate"]
        if data.get("leggings"):
            player.leggings = data["leggings"]
        if data.get("boots"):
            player.boots = data["boots"]
        if data.get("pickaxe"):
            player.pickaxe = data["pickaxe"]
        if data.get("sword"):
            player.sword = data["sword"]
        if data.get("reserved_armor"):
            player.reserved_armor = data["reserved_armor"]
        if data.get("reserved_tools"):
            player.reserved_tools = data["reserved_tools"]
        return player


def getplayer():
    inventory = Inventory()
    inventory.add(Block("dirt", 1, 75, -100), 64)
    inventory.add(Block("stone", 1, 40, -100), 64)
    inventory.add(Item("coal"), 23)
    inventory.add(Item("iron ingot"), 51)
    inventory.add(Item("gold ingot"), 123)
    inventory.add(Food("melon slice", 0, 2), 64)
    inventory.add(Food("bread", 0, 4), 12)
    inventory.add(Potion("haste", "haste", 300), 16)
    pick = Tool("iron pickaxe", 250, 5, 2, [Enchantment("efficiency", 3)])
    sword = Tool("iron sword", 250, 7, 2, [Enchantment("sharpness", 3)])
    helmet = Armor("iron helmet", "helmet", 250, 2, [Enchantment("protection", 3)])
    chestplate = Armor(
        "iron chestplate", "chestplate", 250, 5, [Enchantment("protection", 3)]
    )
    leggings = Armor(
        "iron leggings", "leggings", 250, 3, [Enchantment("protection", 3)]
    )
    boots = Armor("iron boots", "boots", 250, 2, [Enchantment("protection", 3)])
    reserved_armor = [helmet, chestplate, leggings, boots]
    reserved_tools = [pick, sword]
    player = Player("steve", inventory)
    player.pickaxe = pick
    player.sword = sword
    player.helmet = helmet
    player.chestplate = chestplate
    player.leggings = leggings
    player.boots = boots
    player.reserved_armor = reserved_armor
    player.reserved_tools = reserved_tools
    return player


def test_nested_classes():
    player = getplayer()
    print("Player Name:", player.name)
    print("Inventory:", player.inventory)
    print("Helmet:", player.helmet)
    print("Chestplate:", player.chestplate)
    print("Leggings:", player.leggings)
    print("Boots:", player.boots)
    print("Pickaxe:", player.pickaxe)
    print("Sword:", player.sword)
    print("Reserved Armor:", player.reserved_armor)
    print("Reserved Tools:", player.reserved_tools)
    serialized_player = dumps(player)
    print("Serialized Player:", serialized_player)
    loaded_player: Player = loads(serialized_player).original
    print("Loaded Player Name:", loaded_player.name)
    print("Loaded Inventory:", loaded_player.inventory)
    print("Loaded Helmet:", loaded_player.helmet)
    print("Loaded Chestplate:", loaded_player.chestplate)
    print("Loaded Leggings:", loaded_player.leggings)
    print("Loaded Boots:", loaded_player.boots)
    print("Loaded Pickaxe:", loaded_player.pickaxe)
    print("Loaded Sword:", loaded_player.sword)
    print("Loaded Reserved Armor:", loaded_player.reserved_armor)
    print("Loaded Reserved Tools:", loaded_player.reserved_tools)

    assert player == loaded_player, "Loaded player does not match original player"
