'''
 The Problem:

  # LLM gives you this:
  response = "John Smith is 30 years old, email: john@email.com"

  # You need this:
  person = {
      "name": "John Smith",
      "age": 30,
      "email": "john@email.com"
  }

'''

from pydantic import BaseModel


class Person(BaseModel):
	name:str
	age:int
	email:str

print("Creating a valid person")

john = Person( 
	name="John Smith",
	age=30,
	email="john@email.com"
)

print("✅ Person created successfully!")
print(f"Name: {john.name}")
print(f"Age: {john.age}")
print(f"Email: {john.email}")
print(f"Type: {type(john)}")


if john.age>=18:
	print(f"{john.name} is an adult")

print("="*60)
print("trying to create a person withut invalid age")

try:
	invalid=Person(
		name="John Smith",	
		age="Thirty",
		email="john@email.com"
	)
except Exception as e:
	print("Validation Error")
	print("Age must be  interger got string")

print("Pydantic caught error automatically")


