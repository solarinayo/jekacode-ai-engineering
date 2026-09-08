students =[
    {"name":"Dara", "score": 48},
    {"name":"Tolu", "score": 75},
    {"name":"Teju", "score":57},
    {"name":"Shina", "score":90},
    {"name":"Jack", "score":65},
    {"name":"Mason", "score":39},
    {"name":"Paul", "score":79}
]

def calculate_stats(students):
    scores = [students["score"] for students in students]
    average =sum(scores) / len(scores)
    highest =max(scores)
    lowest=min(scores)
    return average,highest,lowest

average, highest, lowest = calculate_stats(students)
print(calculate_stats(students))
print("-----------------------------")
print("Average:", average)
print("Highest:", highest)
print("Lowest:", lowest)

for student in students:
    if student["score"] >= 50:
        print(student["name"], student["score"], "- PASS")
    else:
        print(student["name"], student["score"], "-FAIL")

        prompt = f"""
        The class average is {average},
The highest score is {highest},
The lowest score is {lowest},
Write a one-paragraph summary of the class performance in plain english.
"""