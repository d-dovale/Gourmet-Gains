import food

report = food.get_report()

def main_menu():
    print("WELCOME TO GOURMET GAINS!\n")
    search_food(input("Input a food item: "))


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
        else:
            print("Invalid option. Please try again.\n")
            continue

def calculate_difference(item1, item2):
    # Example: Euclidean distance based on macronutrients
    carb_diff = item1['Data']['Carbohydrate'] - item2['Data']['Carbohydrate']
    protein_diff = item1['Data']['Protein'] - item2['Data']['Protein']
    fat_diff = item1['Data']['Fat']['Total Lipid'] - item2['Data']['Fat']['Total Lipid']

    return math.sqrt(carb_diff**2 + protein_diff**2 + fat_diff**2)

def build_graph():
    food_report = food.get_report()
    graph = {}

    for i in range(len(food_report)):
        for j in range(i+1, len(food_report)):
            item1 = food_report[i]
            item2 = food_report[j]
            difference = calculate_difference(item1, item2)
            graph[(item1['Description'], item2['Description'])] = difference

    return graph

def search_food(food_item):
    food_report = food.get_report()
    food_item_lower = food_item.lower()

    # Prioritize matches where the food item is at the beginning of the description
    primary_matches = [item for item in food_report if item['Description'].lower().startswith(food_item_lower)]

    # If no primary matches, find broader matches
    if not primary_matches:
        search_terms = food_item_lower.split()
        secondary_matches = [item for item in food_report if all(term in item['Description'].lower() for term in search_terms)]
        search_results = secondary_matches
    else:
        search_results = primary_matches

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
        print("\n---------------------------------------------\n")

    else:
        print("Invalid selection.\n")
        choice = int(input("Enter your choice (number): ")) - 1

if __name__ == '__main__':
    main_menu()

