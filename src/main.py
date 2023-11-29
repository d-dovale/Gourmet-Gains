import food

report = food.get_report()

def main_menu():
    print("WELCOME TO GOURMET GAINS!\n")
    print("Main Menu:")

    while True:
        print("\n1. Input Item\n2. Search Single Macronutrient\n3. Search All Macronutrients\n4. Search Single Nutrient\n5. Exit\n")
        choice = int(input("Pick an Option: "))

        if(choice == 1):
            search_food(input("Enter a food item: "))

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
    search_terms = food_item.lower().split()

    # Update the search to check if all search terms are in the description
    search_results = [item for item in food_report if all(term in item['Description'].lower() for term in search_terms)]

    if not search_results:
        print("No items found.")
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

