import food

report = food.get_report()

def main_menu():
    print("WELCOME TO GOURMET GAINS!\n")
    print("Main Menu:")

    while True:
        print("\n1. Input Item\n2. Search Single Macronutrient\n3. Search All Macronutrients\n4. Search Single Nutrient\n5. Exit\n")
        choice = int(input("Pick an Option: "))

        if(choice == 1):
            pass

        elif(choice == 2):
            pass

        elif(choice == 3):
            pass

        elif(choice == 4):
            pass

        elif(choice == 5):
            print("\nThank you for using Gourmet Gains!\n")  
            break

def search_food(food_item):
    food_report = food.get_report()
    search_results = [item for item in food_report if food_item.lower() in item['Description'].lower()]
    return search_results

if __name__ == '__main__':
    print("hello world")



 
