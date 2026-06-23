from pydantic import BaseModel, Field, EmailStr, conint

class User(BaseModel):
    username: str = Field(..., title="Username", max_length=30, description="The user's chosen username.")
    email: EmailStr = Field(..., example="user@example.com", description="The user's email address.")
    age: int = Field(..., title="Age", description="The user's age, must be greater than 0.")
    bio: str = Field(default="No bio provided", max_length=200, description="A short biography of the user.")
    is_active: bool = Field(default=True, description="Is the user active?")

# Example of creating an instance with valid data
if __name__ == "__main__":
    try:
        user = User(username="john_doe", email="john@example.com", age=25)
        print(user)

        user = {
            "username": "john_doe",
            "age": 30,

            "bio": "A software developer."
        }
        user2 = User(**user)
        print(user2)
    except ValueError as e:
        print(f"Error: {e}")

    # Example with invalid data
    try:
        user_invalid = User(username="jane_doe", email="invalid_email", age=-5)
    except ValueError as e:
        print(f"Error: {e}")
        