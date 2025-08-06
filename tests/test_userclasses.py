from __future__ import annotations

from fxdc import Config, dumps, loads



@Config.add_class
class User:
    def __init__(self, username: str, age: int, email: str):
        self.username = "john_doe"
        self.age = age
        self.email = "john@example.com"
        self.birthyear = 2025-age
        
    def __todata__(self) -> dict[str, str|int]:
        return {
            "username": self.username,
            "age": self.age,
            "email": self.email,
        }
        
    def __eq__(self, other: User) -> bool:
        return (
            self.username == other.username and
            self.age == other.age and
            self.email == other.email and
            self.birthyear == other.birthyear
        )
        
    def __repr__(self) -> str:
        return f"User(username={self.username}, age={self.age}, email={self.email})"
    
    def __str__(self) -> str:
        return f"User: {self.username}, Age: {self.age}, Email: {self.email}, Birth Year: {self.birthyear}"

def test_user_class(): 
    user = User("john_doe", 25, "john@example.com")
    print("Original User:", user)
    data = dumps(user)
    print("Serialized Data:", data)
    loaded_user:User = loads(data).original
    print("Loaded User:", loaded_user)
    assert user == loaded_user, "User objects are not equal after serialization and deserialization"
    