import random

random.seed(42)

destinations = [
    "Kerala",
    "Goa",
    "Rajasthan",
    "Manali",
    "Karnataka",
    "Tamil Nadu",
    "Maharashtra",
    "Himachal Pradesh",
    "Uttarakhand",
    "Andhra Pradesh",
    "Telangana",
    "Punjab",
    "West Bengal",
    "Odisha",
    "Gujarat",
    "Sikkim",
    "Meghalaya",
    "Assam",
    "Madhya Pradesh",
    "Uttar Pradesh"
]


interests = [
    "Nature",
    "Adventure",
    "Beaches",
    "Food",
    "Culture",
    "History",
    "Shopping",
    "Relaxation"
]


budgets = [
    10000,
    15000,
    20000,
    25000,
    30000,
    40000,
    50000
]


days_options = [
    2,
    3,
    4,
    5,
    7
]


test_cases = []


for i in range(250):

    destination = random.choice(destinations)

    days = random.choice(days_options)

    budget = random.choice(budgets)

    number_of_interests = random.randint(1, 3)

    selected_interests = random.sample(
        interests,
        number_of_interests
    )

    test_case = {
        "test_id": i + 1,
        "destination": destination,
        "days": days,
        "budget": budget,
        "interests": selected_interests
    }

    test_cases.append(test_case)


if __name__ == "__main__":

    print(
        "Total test cases:",
        len(test_cases)
    )

    for test in test_cases[:10]:

        print(test)