import food

report = food.get_report()

def main_menu():
    print("WELCOME TO GOURMET GAINS!\n")
    search_food(input("Input a food item: \n"))


    print("Main Menu:\n")

    while True:

        print("1. Recommend food items using Dijkstra's algorithm\n2. Recommend food items using Floyd Marshall’s Algorithm \n3. Search Carbohydrates\n4. Search Protein \n5. Search Fats \n6. Exit\n")
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
    search_terms = food_item.lower().split()

    # Update the search to check if all search terms are in the description
    search_results = [item for item in food_report if all(term in item['Description'].lower() for term in search_terms)]

    if not search_results:
        print("No items found.\n")
        search_food(input("Input a food item: \n"))
        return

    print("\nSelect the specific type of", food_item)

    for i, item in enumerate(search_results):
        print(f"{i + 1}. {item['Description']}")

    choice = int(input("\nEnter your choice (number): ")) - 1

    if 0 <= choice < len(search_results):
        selected_item = search_results[choice]
        print("\nSelected Item:", selected_item['Description'])
        print("Macronutrients:")
        print(f"  - Carbohydrates: {selected_item['Data']['Carbohydrate']} g")
        print(f"  - Proteins: {selected_item['Data']['Protein']} g")
        print(f"  - Fats: {selected_item['Data']['Fat']['Total Lipid']} g")

    else:
        print("Invalid selection.")

if __name__ == '__main__':
    main_menu()

