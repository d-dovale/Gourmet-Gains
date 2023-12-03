import food
import math
import time
from heapq import heappush, heappop

report = food.get_report()
selected_item = None

def main_menu():
    print("WELCOME TO GOURMET GAINS!\n")

    print("- You can either enter a food item you're interested in or search based on specific macronutrients.")
    print("- Choose various options to find similar food items or explore their macronutrient content.")
    print("- Feel free to select a different food item at any time to start a new search.\n")
    
    while True:
        print("\nMain Menu:\n")
        print("1. Search Based on Specific Macronutrients\n2. Enter a Food Item\n3. Exit\n")
        try:
            main_choice = int(input("Pick an Option: "))
            print("\n-------------------------------------------------------------")
        except ValueError:
            print("Invalid Input. Please enter a number.\n")
            continue

        if main_choice == 1:
            macronutrient_based_search()
        elif main_choice == 2:
            food_item_search()
        elif main_choice == 3:
            print("\nThank you for using Gourmet Gains!\n")
            break
        else:
            print("Invalid option. Please try again.\n")

def macronutrient_based_search():
    print("\nMacronutrient Based Search\n")
    print("Enter 'high', 'low', or 'any' for each macronutrient.")

    protein_input = input("Protein (high/low/any): ").lower()
    carbs_input = input("Carbohydrates (high/low/any): ").lower()
    fats_input = input("Fats (high/low/any): ").lower()

    # Define thresholds for high and low
    high_protein_threshold = 20  
    low_protein_threshold = 5    
    high_carbs_threshold = 50    
    low_carbs_threshold = 15     
    high_fats_threshold = 20    
    low_fats_threshold = 5

    matching_items = []
    for item in report:
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
        print("\nFood items matching your criteria:")
        for i, item in enumerate(matching_items, 1):
            print(f"{i}. {item}")
    else:
        print("No items found matching your criteria.\n")

def food_item_search():
    global selected_item
    selected_item = select_food_item()

    while True:
        if not selected_item:
            selected_item = select_food_item()

        graph = build_graph_for_item(selected_item, report)
        print("\nFood Item Menu:\n")
        print("1. Recommend food items using Dijkstra's algorithm\n2. Recommend food items using Floyd Warshall's Algorithm\n3. Select a Different Starting Food Item\n4. Exit\n")

        try:
            choice = int(input("Pick an Option: "))
        except ValueError:
            print("Invalid Input. Please enter a number.\n")
            continue

        if choice == 1:
            recommend_food_items_dijkstra(graph, selected_item)
        elif choice == 2:
            recommend_food_items_floyd_warshall(graph, selected_item)
        # Implement other options (3 to 5) as needed.
        elif choice == 3:
            selected_item = select_food_item()
        elif choice == 4:
            print("\nExiting the Food Item Menu.\n")
            break
        else:
            print("Invalid option. Please try again.")

def select_food_item():
    food_item = input("Input a food item: ")
    return search_food(food_item)


def calculate_difference(item1, item2):
    # Example: Euclidean distance based on macronutrients
    carb_diff = abs(item1['Data']['Carbohydrate'] - item2['Data']['Carbohydrate'])
    protein_diff = abs(item1['Data']['Protein'] - item2['Data']['Protein'])
    fat_diff = abs(item1['Data']['Fat']['Total Lipid'] - item2['Data']['Fat']['Total Lipid'])

    return math.sqrt(carb_diff**2 + protein_diff**2 + fat_diff**2)

# Slower version of graph that takes about 30 seconds to run

def build_graph(threshold = 0.5):
    start_time = time.time()
    food_report = food.get_report()
    graph = {}

    for i in range(len(food_report)):
        for j in range(i + 1, len(food_report)):
            item1 = food_report[i]
            item2 = food_report[j]
            difference = calculate_difference(item1, item2)
            if difference < threshold:
                graph[(item1['Description'], item2['Description'])] = difference

    end_time = time.time()
    print(f"Graph built in {time.time() - start_time} seconds.")
    return graph

# Faster version of graph that takes in a specific item and builds a graph for that item

def build_graph_for_item(selected_item, food_report, threshold = 2):
    graph = {item['Description']: [] for item in food_report}  # Initialize graph with all food items

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

    print("\nSelect the specific type of", food_item)

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
            print("\n-------------------------------------------------------------\n")
            
            return selected_item
        else:
            print("INVALID SELECTION.")

def dijkstra_algorithm(graph, start, n):
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

    print("-------------------------------------------------------------")

def knn_algorithm(graph, selected_item, n):
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

    print(f"\n{n} Closest Food Items to '{selected_item}' based on the Macronutrient profile using KNN: \n")
    count = 1
    for i, (item, distance) in enumerate(nearest_neighbors, 1):
        print(f'{i}. {item}')
        count += 1  

    print(f"\n{count - 1} items found.")
    print(f"\nKNN completed in {time.time() - start_time} seconds!")
    print("\n-------------------------------------------------------------\n")

if __name__ == '__main__':
    main_menu()
   

