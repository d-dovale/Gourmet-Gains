import food
import math
import time
from heapq import heappush, heappop

report = food.get_report()
selected_item = None

def main_menu():
    """
    Main menu function displaying the initial options to the user.
    This function serves as the entry point for interacting with the Gourmet Gains application.

    The function offers a loop-based menu system with options to:
    - Search for food items based on specific macronutrients.
    - Enter and analyze a specific food item.
    - Exit the application.

    User input is captured and validated, and the corresponding function is called based on the user's choice.
    """

    print("WELCOME TO GOURMET GAINS!\n")
    print("- Discover food items based on your nutritional preferences.")
    print("- Explore our extensive database to find food items that match specific macronutrient profiles, such as high protein or low carbs.")
    print("- Get personalized recommendations for food items similar to your favorites based on their nutritional content.")
    print("- Whether you're looking to balance your diet or find new food options, Gourmet Gains is here to guide you!\n")
    print("-------------------------------------------------------------------------------------------------------------------------------")
    
    while True:
        print("\nMain Menu:\n")
        print("1. Search based on Specific Macronutrients\n2. Enter a Food Item\n3. Exit\n")
        try:
            main_choice = int(input("Pick an Option: "))
            print("\n-------------------------------------------------------------------------------------------------------------------------------\n")
        except ValueError:
            print("Invalid Input. Please enter a number.\n")
            continue
        
        # MAIN MENU
        if main_choice == 1:
            macronutrient_based_search()
        elif main_choice == 2:
            food_item_search()
        elif main_choice == 3:
            print("\nThank you for using Gourmet Gains!\n")
            exit()
        else:
            print("Invalid menu option. Please try again.\n")

def macronutrient_based_search():
    print("Macronutrient Based Search\n")
    print("Enter 'high', 'low', or 'any' for each macronutrient.")

    def get_valid_input(macro_name):
        while True:
            user_input = input(f"{macro_name} (high/low/any): ").lower()
            if user_input in ['high', 'low', 'any']:
                return user_input
            else:
                print("\nPlease enter a valid option (high, low, any)")

    protein_input = get_valid_input("  - Protein")
    carbs_input = get_valid_input("  - Carbohydrates")
    fats_input = get_valid_input("  - Fats")

    # Define thresholds for high and low
    high_protein_threshold = 13 
    low_protein_threshold = 4    
    high_carbs_threshold = 31    
    low_carbs_threshold = 10     
    high_fats_threshold = 13    
    low_fats_threshold = 5

    matching_items = []
    for item in report:
        if len(matching_items) >= 25:
            break

        protein = item['Data']['Protein']
        carbs = item['Data']['Carbohydrate']
        fats = item['Data']['Fat']['Total Lipid']

        if (protein_input == 'high' and protein < high_protein_threshold) or \
           (protein_input == 'low' and protein > low_protein_threshold) or \
           (carbs_input == 'high' and carbs < high_carbs_threshold) or \
           (carbs_input == 'low' and carbs > low_carbs_threshold) or \
           (fats_input == 'high' and fats < high_fats_threshold) or \
           (fats_input == 'low' and fats > low_fats_threshold):
            continue

        matching_items.append(item['Description'])

    if matching_items:
        print("\nFood items matching your criteria (up to 25 items): \n")
        for i, item in enumerate(matching_items, 1):
            print(f"{i}. {item}")
        print("\n-------------------------------------------------------------------------------------------------------------------------------")
    else:
        print("\nNo items found matching your criteria.\n")


def food_item_search():
    """
    Allows users to search for a specific food item by name.
    Users can select a food item and then choose further actions like getting recommendations.
    """

    global selected_item
    selected_item = select_food_item()

    while True:
        if not selected_item:
            selected_item = select_food_item()

        graph = build_graph_for_item(selected_item, report)
        print("\nFood Item Menu:\n")
        print("1. Recommend food items using Dijkstra's algorithm\n2. Recommend food items using K-Nearest Neighbor's Algorithm\n3. Select a Different Starting Food Item\n4. Exit\n")

        try:
            choice = int(input("Pick an Option: "))
        except ValueError:
            print("Invalid Input. Please enter a number.\n")
            continue

        # FOOD ITEM MENU   
        if(choice == 1):
            if selected_item:
                while True:
                    try:
                        num = int(input("Enter the amount of recommended food items: "))
                        break
                    except ValueError:
                        print("Invalid Input. Please enter a number.\n")
                        continue
                dijkstra_algorithm(graph, selected_item['Description'], num)
            else:
                print("No food item selected. Please select an item first.")

        elif(choice == 2):
            if selected_item:
                try:
                    num = int(input("Enter the amount of recommended food items: "))
                except ValueError:
                    print("Invalid Input. Please enter a number.\n")
                    continue
                knn_algorithm(graph, selected_item['Description'], num)
            else:
                print("No food item selected. Please select an item first.")

        elif(choice == 3):
            selected_item = select_food_item()

        elif(choice == 4):
            print("\nThank you for using Gourmet Gains!\n")
            exit()

        else:
            print("Invalid option. Please try again.\n")
            

def select_food_item():
    food_item = input("Input a food item: ")
    return search_food(food_item)


def calculate_difference(item1, item2):
    """
    Calculates the difference between two food items based on their macronutrient content.
    Uses Euclidean distance calculation for the difference.
    Returns a numerical value representing the difference.
    """

    carb_diff = abs(item1['Data']['Carbohydrate'] - item2['Data']['Carbohydrate'])
    protein_diff = abs(item1['Data']['Protein'] - item2['Data']['Protein'])
    fat_diff = abs(item1['Data']['Fat']['Total Lipid'] - item2['Data']['Fat']['Total Lipid'])

    return math.sqrt(carb_diff**2 + protein_diff**2 + fat_diff**2)

def build_graph_for_item(selected_item, food_report, threshold = 2):
    """
    Builds a graph for a specific food item, connecting it to similar items based on macronutrients.
    This is a faster version of the graph-building function, focusing only on one item.
    The connections are based on a threshold for macronutrient differences.
    """

    graph = {item['Description']: [] for item in food_report}

    for item in food_report:
        if item['Description'] != selected_item['Description']:
            difference = calculate_difference(selected_item, item)
            if difference < threshold:
                graph[selected_item['Description']].append((item['Description'], difference))
                graph[item['Description']].append((selected_item['Description'], difference))  # Add reverse edge

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
        search_food(input("Input a food item: "))
        return

    print(f"\nSelect the specific type of {food_item}:")

    for i, item in enumerate(search_results):
        print(f"{i + 1}. {item['Description']}")
    while(True):
        try:
            choice = int(input("\nEnter your choice (number): ")) - 1
        except ValueError:
            print("Invalid Input. Please enter a number.")
            continue
        if 0 <= choice < len(search_results):
            selected_item = search_results[choice]
            print("\nSelected Item:", selected_item['Description'])
            print("Macronutrients:")
            print(f"  - Carbohydrates: {selected_item['Data']['Carbohydrate']} g")
            print(f"  - Proteins: {selected_item['Data']['Protein']} g")
            print(f"  - Fats: {selected_item['Data']['Fat']['Total Lipid']} g")
            print("\n--------------------------------------------------------------------------------------------------------------------------------\n")
            
            return selected_item
        else:
            print("INVALID SELECTION.")

def dijkstra_algorithm(graph, start, n):
    """
    Implements Dijkstra's algorithm to find the closest n food items to a given start item.
    'Closest' is determined based on the macronutrient profile.
    The function outputs the n closest items and the time taken to compute.
    """

    start_time = time.time()
    shortest_distances = {node: float('infinity') for node in graph}
    shortest_distances[start] = 0
    visited = set()
    priority_queue = [(0, start)]

    closest_items = []

    while priority_queue and len(closest_items) < n + 1:
        current_distance, current_node = heappop(priority_queue)
        if current_node not in visited:
            visited.add(current_node)
            closest_items.append((current_node, current_distance))

            for neighbor, weight in graph.get(current_node, []):
                if neighbor not in visited:
                    new_distance = current_distance + weight
                    if new_distance < shortest_distances[neighbor]:
                        shortest_distances[neighbor] = new_distance
                        heappush(priority_queue, (new_distance, neighbor))

    print(f"\n{n} Closest Food Items to '{selected_item['Description']}' based on the Macronutrient profile: \n")
    count = 1
    for item in closest_items[1:]:
        
        print(f'{count}. {item[0]}')
        count +=1
    
    print(f"\n{count - 1} items found.")
    print(f"\nDijkstra's Algorithm completed in {time.time() - start_time} seconds!")

    print("\n--------------------------------------------------------------------------------------------------------------------------------\n")

def knn_algorithm(graph, selected_item, n):
    """
    Implements the K-Nearest Neighbors algorithm to recommend n food items similar to the selected item.
    Similarity is based on the macronutrient profile.
    The function outputs the n closest items and the time taken to compute.
    """

    start_time = time.time()

    # Retrieve the data for the selected item
    selected_item_data = next(item for item in report if item['Description'] == selected_item)

    # Calculate distances from the selected item to all others
    distances = []
    for item in graph:
        if item != selected_item:
            item_data = next(food_item for food_item in report if food_item['Description'] == item)
            distance = calculate_difference(selected_item_data, item_data)
            distances.append((item, distance))

    # Sort the items based on distance and pick the top n items
    nearest_neighbors = sorted(distances, key=lambda x: x[1])[:n]

    print(f"\n{n} Closest Food Items to '{selected_item}' based on the Macronutrient profile: \n")
    count = 1
    for i, (item, distance) in enumerate(nearest_neighbors, 1):
        print(f'{i}. {item}')
        count += 1  

    print(f"\n{count - 1} items found.")
    print(f"\nKNN completed in {time.time() - start_time} seconds!")
    print("\n--------------------------------------------------------------------------------------------------------------------------------\n")

# Calculates the average macronutrient values for all food items in the report
def calculate_averages(food_report): 

    total_carbs = 0
    total_fat = 0
    total_protein = 0
    total_items = len(food_report)

    for item in food_report:
        total_carbs += item['Data']['Carbohydrate']
        total_fat += item['Data']['Fat']['Total Lipid']
        total_protein += item['Data']['Protein']

    average_carbs = total_carbs / total_items
    average_fat = total_fat / total_items
    average_protein = total_protein / total_items

    return average_carbs, average_fat, average_protein

def calculate_macro_thresholds():
    avg_carbs, avg_fat, avg_protein = calculate_averages(report)

    # Multipliers for high and low values
    high_multiplier = 1.5
    low_multiplier = 0.5

    # Calculate threshold values
    high_carbs_threshold = avg_carbs * high_multiplier
    low_carbs_threshold = avg_carbs * low_multiplier

    high_fat_threshold = avg_fat * high_multiplier
    low_fat_threshold = avg_fat * low_multiplier

    high_protein_threshold = avg_protein * high_multiplier
    low_protein_threshold = avg_protein * low_multiplier

    # Print the threshold values
    print("Thresholds: \n")
    print("  - High Carbs:", high_carbs_threshold, "g")
    print("  - Low Carbs:", low_carbs_threshold, "g")
    print("  - High Fat:", high_fat_threshold, "g")
    print("  - Low Fat:", low_fat_threshold, "g")
    print("  - High Protein:", high_protein_threshold, "g")
    print("  - Low Protein:", low_protein_threshold, "g\n")

if __name__ == '__main__':
    main_menu()
    

