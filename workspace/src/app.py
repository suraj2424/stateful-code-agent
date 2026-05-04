# Level 0 : buggy code
def calculate_average(numbers):

    if not numbers:
        return 0
    
    total = sum(numbers)
    return total / len(numbers)

result = calculate_average([])
print(result)

# Level 1 : buggy code
# This tests if the agent can handle a logic error that doesn't cause a crash but produces wrong data.
def get_user_status(age):
    # Task: Return 'Minor' for < 18, 'Adult' for 18-65, 'Senior' for > 65
    # BUG 1: The logic for 18 is wrong (returns Minor)
    # BUG 2: Input 'age' might come in as a string from a form
    if age < 18:
        return "Minor"
    elif age > 18 and age < 65:
        return "Adult"
    else:
        return "Senior"

# Test cases
print(f"Test 18: {get_user_status(18)}")   # Expected: Adult
print(f"Test '20': {get_user_status('20')}") # Expected: Adult (Currently crashes)

# Level 2 : buggy code
# This tests if the agent can understand how to fix a function that relies on another broken function.
import json

def parse_config(json_str):
    # BUG: If json_str is empty or invalid, this crashes.
    return json.loads(json_str)

def get_database_url(config_str):
    # Task: Extract the 'db_url' from a JSON string safely.
    config = parse_config(config_str)
    return config['db_url'] # BUG: Will crash if 'db_url' key is missing

# Test
print(get_database_url('{"db_url": "postgres://localhost"}'))
print(get_database_url('{}')) # Should return None or Error, not crash

# Level 3 : buggy code
# This is the hardest. It requires the agent to optimize a "Naive" solution that is extremely slow or inefficient.
def find_duplicates(items):
    """
    Task: Return a list of duplicate items.
    """
    duplicates = []
    # BUG: O(n^2) complexity. If 'items' has 1 million entries, this hangs.
    # Also, it adds the same duplicate multiple times to the list.
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:
                duplicates.append(items[i])
    return duplicates

# Test
print(find_duplicates([1, 2, 3, 1, 2, 4])) # Expected: [1, 2]