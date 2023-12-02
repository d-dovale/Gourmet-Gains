import food
import math
import time

report = food.get_report()

def main_menu():
    print("WELCOME TO GOURMET GAINS!\n")
    search_food(input("Input a food item: "))


    print("Main Menu:\n")

    while True:

        print("1. Recommend food items using Dijkstra's algorithm\n2. Recommend food items using Floyd Marshall’s Algorithm \n3. Search Carbohydrates\n4. Search Protein \n5. Search Fats \n6. Exit\n")
        try:
            choice = int(input("Pick an Option: "))
        except ValueError:
            print("Invalid Input. Please enter a number.\n")
            continue

        if(choice == 1):
            dijkstra_recommendation()

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

def build_graph_for_item(selected_item, food_report, threshold=10):
    # Building the graph only for the selected item
    start_time = time.time()
    graph = {}

    for item in food_report:
        if item['Description'] != selected_item['Description']:
            difference = calculate_difference(selected_item, item)
            if difference < threshold:
                graph[selected_item['Description']] = (item['Description'], difference)
    
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
        search_food(input("Input a food item: \n"))
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
            print("\n---------------------------------------------\n")
            break
        else:
            print("INVALID SELECTION.")
        

def dijkstra(graph, start, report):
    distances = {food_item['Description']: float('infinity') for food_item in report}
    distances[start] = 0
    visited = set()

    while len(visited) < len(report):
        current_food = min((food for food in report if food['Description'] not in visited), key=lambda x: distances[x['Description']])
        visited.add(current_food['Description'])

        for neighbor, weight in graph.get(current_food['Description'], []):
            distance = distances[current_food['Description']] + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance

    return distances

def dijkstra_recommendation(graph, report):
    start_food = input("Enter the starting food item: ")

    if start_food not in [food_item['Description'] for food_item in report]:
        print("Invalid food item. Please try again.")
        return

    distances = dijkstra(graph, start_food, report)

    print("\nRecommended Food Items:")
    for food_item, distance in sorted(distances.items(), key=lambda x: x[1])[1:6]:
        if distance != float('infinity'):
            print(f"{food_item}: {distance} units away")
        else:
            print(f"{food_item}: Not reachable")

if __name__ == '__main__':
    #print("Welcome to Gourmet Gains!\n")
    #build_graph()
    build_graph_for_item(report[0], report)
    


