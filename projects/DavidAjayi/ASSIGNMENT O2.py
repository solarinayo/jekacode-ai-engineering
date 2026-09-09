# Assignment Week 2 - Class Statistics
dct = {
    'Daniel': 89,
    'John': 49,
    'Poju': 87,
    'Jake': 74,
    'David': 85,
    'Nike': 43
}
def class_statistics(scores):
    values = scores.values()

    average = sum(values) / len(values)
    highest = max(values)
    lowest = min(values)

    return average, highest, lowest


average, highest, lowest = class_statistics(dct)

print("Class Average:", average)
print("Highest Score:", highest)
print("Lowest Score:", lowest)

for name, score in dct.items():
    if score >= 50:
        print(name, ":", score, "- Pass")
    else:
        print(name, ":", score, "- Fail")
        prompt = f"""
        The class average is {average},
        The highest score is {highest},
        The lowest score is {lowest},
        
        Write a one line paragraph summary of the class performance in plain english.
        """

        
        

