import food

report = food.get_report()

def main_menu():
    print("WELCOME TO GOURMET GAINS!\n")
    food_item = input("Input a food item: \n")
    print("Food item nutrients: \n")
    print("Main Menu:\n")

    while True:

        print("1. Recommend food items using Dijkstra's algorithm\n2. Recommend food items using Floyd Marshall’s Algorithm \n3. Search Carbohydrates\n4. Search Protein \n5. Search Fats \n6. Exit")
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
            pass

    
        elif(choice == 6):
            print("\nThank you for using Gourmet Gains!\n")  
            break

def search_food(food_item):
    food_report = food.get_report()
    search_results = [item for item in food_report if food_item.lower() in item['Category'].lower()]
    return search_results

if __name__ == '__main__':
    #search_food("Milk")
    main_menu()

