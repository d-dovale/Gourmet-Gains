import food
import math
import time
from heapq import heappush, heappop

report = food.get_report()
selected_item = None

def main_menu():
    global selected_item
    print("WELCOME TO GOURMET GAINS!\n")
    food_item = input("Input a food item: ")
    selected_item = search_food(food_item)

     # Check if an item was actually selected
    if not selected_item:
        return

    print("Main Menu:\n")

    while True:
        graph = build_graph_for_item(selected_item, report)

        print("1. Recommend food items using Dijkstra's algorithm\n2. Recommend food items using Floyd Marshall’s Algorithm \n3. Search Carbohydrates\n4. Search Protein \n5. Search Fats \n6. Exit\n")
        try:
            choice = int(input("Pick an Option: "))
        except ValueError:
            print("Invalid Input. Please enter a number.\n")
            continue

        if(choice == 1):
            if selected_item:
                 dijkstra(graph, selected_item['Description'], 20)
            else:
                print("No food item selected. Please select an item first.")

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
    start_time = time.time()
    graph = {item['Description']: [] for item in food_report}  # Initialize graph with all food items

    for item in food_report:
        if item['Description'] != selected_item['Description']:
            difference = calculate_difference(selected_item, item)
            if difference < threshold:
                graph[selected_item['Description']].append((item['Description'], difference))
                graph[item['Description']].append((selected_item['Description'], difference))  # Add reverse edge
    
    end_time = time.time()
    print(f"Graph built in {time.time() - start_time} seconds.")

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

def dijkstra(graph, start, n):
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
    print("\n")

def printdijkstra(closest_n_items, num):
    print(f"{num} Closest Food Items to '{selected_item['Description']}' based on Macronutrient profile: \n")
    count = 1
    for item in closest_items[1:]:  # Skip first item since it will be the selected item itself
        
        print(f'{count}. {item[0]}:')
        count +=1
    
    print(f"\nDijkstra's algorithm completed in {time.time() - start_time} seconds.")
    print("\n------------------------------------------------------------\n")


if __name__ == '__main__':
    # report = food.get_report()
    # selected_item = report[0]  # Assuming this is human milk
    # graph = build_graph_for_item(selected_item, report)

    # closest_n_items = dijkstra(graph, selected_item['Description'], 20)  # Find 10 closest items
    # print("10 Closest Food Items to", selected_item['Description'], ":\n", closest_n_items)

    main_menu()

