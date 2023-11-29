import food

report = food.get_report()

print("WELCOME TO GOURMET GAINS!\n")
print("Main Menu:\n")

while True:
    print("Please enter a food item to search for, or type 'quit' to exit.")
    print("1. Input Item\n2. Search Single Macronutrient\n3. Search All Macronutrients\n4. Search Single Nutrient\n4. Exit\n")
    choice = input("Pick an Option: ")

