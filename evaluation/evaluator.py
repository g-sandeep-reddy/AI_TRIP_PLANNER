import time
import requests
import os
import json

from dotenv import load_dotenv
from evaluation.test_cases import test_cases


API_URL = "http://127.0.0.1:8001"

RESULTS_FILE = "evaluation/results.json"

# Run only the first 50 test cases
MAX_TESTS = 50

# How many times to retry a rate-limited request
MAX_RETRIES = 5

# Wait time after 429
RETRY_WAIT = 30


load_dotenv()

EVAL_USERNAME = os.getenv("EVAL_USERNAME")
EVAL_PASSWORD = os.getenv("EVAL_PASSWORD")


def check_trip_result(test_case, result):

    checks = {
        "destination": False,
        "days": False,
        "interests": False,
        "budget": False,
        "activities": False
    }

    trip_plan = result.get("trip_plan")

    if not trip_plan:
        return checks

    # -----------------------------
    # Check destination
    # -----------------------------

    destination = trip_plan.get("destination", "")

    if destination.lower() == test_case["destination"].lower():
        checks["destination"] = True

    # -----------------------------
    # Check number of days
    # -----------------------------

    days = trip_plan.get("days", [])

    if len(days) == test_case["days"]:
        checks["days"] = True

    # -----------------------------
    # Check interests
    # -----------------------------

    trip_text = str(trip_plan).lower()

    found_interests = 0

    for interest in test_case["interests"]:

        if interest.lower() in trip_text:
            found_interests += 1

    if found_interests == len(test_case["interests"]):
        checks["interests"] = True

    # -----------------------------
    # Check budget
    # -----------------------------

    estimated_budget = trip_plan.get("estimated_budget")

    if estimated_budget is not None:

        if estimated_budget <= test_case["budget"]:
            checks["budget"] = True

    # -----------------------------
    # Check activities
    # -----------------------------

    activities_count = 0

    for day in days:

        activities = day.get("activities", [])

        activities_count += len(activities)

    if activities_count > 0:
        checks["activities"] = True

    return checks


def get_auth_token():

    if not EVAL_USERNAME or not EVAL_PASSWORD:

        raise ValueError(
            "EVAL_USERNAME or EVAL_PASSWORD "
            "is missing from .env"
        )

    response = requests.post(
        f"{API_URL}/login",
        json={
            "username": EVAL_USERNAME,
            "password": EVAL_PASSWORD
        },
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    return data["access_token"]


def call_plan_trip(test_case, headers):

    retry_count = 0

    while retry_count < MAX_RETRIES:

        try:

            response = requests.post(
                f"{API_URL}/plan-trip",
                json={
                    "destination": test_case["destination"],
                    "days": test_case["days"],
                    "budget": test_case["budget"],
                    "interests": test_case["interests"]
                },
                headers=headers,
                timeout=180
            )

            # -----------------------------
            # Handle rate limit
            # -----------------------------

            if response.status_code == 429:

                retry_count += 1

                print(
                    f"Rate limit reached. "
                    f"Retry {retry_count}/{MAX_RETRIES} "
                    f"after {RETRY_WAIT} seconds..."
                )

                time.sleep(RETRY_WAIT)

                continue

            return response

        except requests.exceptions.Timeout:

            retry_count += 1

            print(
                f"Request timed out. "
                f"Retry {retry_count}/{MAX_RETRIES}..."
            )

            time.sleep(10)

        except requests.exceptions.RequestException as e:

            print(
                f"Request error: {e}"
            )

            return None

    print(
        "Maximum retries reached."
    )

    return None


def save_results(results):

    with open(
        RESULTS_FILE,
        "w"
    ) as file:

        json.dump(
            results,
            file,
            indent=4
        )


def run_evaluation():

    print("\nGetting authentication token...")

    token = get_auth_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    print("Authentication successful.")

    # --------------------------------
    # Use first 50 test cases
    # --------------------------------

    selected_tests = test_cases[:MAX_TESTS]

    total_tests = len(selected_tests)

    passed = 0
    failed = 0

    total_latency = 0

    results = []

    print(
        f"\nStarting evaluation "
        f"for {total_tests} test cases...\n"
    )

    for index, test_case in enumerate(
        selected_tests,
        start=1
    ):

        print(
            f"Running test "
            f"{index}/{total_tests} "
            f"(Test ID: {test_case['test_id']})..."
        )

        start_time = time.time()

        try:

            response = call_plan_trip(
                test_case,
                headers
            )

            latency = time.time() - start_time

            total_latency += latency

            # --------------------------------
            # Request completely failed
            # --------------------------------

            if response is None:

                failed += 1

                results.append({

                    "test_id": test_case["test_id"],

                    "test_case": test_case,

                    "status": "FAIL",

                    "latency": latency,

                    "reason": "Request failed or timed out"

                })

                save_results(results)

                continue

            # --------------------------------
            # HTTP error
            # --------------------------------

            if response.status_code != 200:

                failed += 1

                results.append({

                    "test_id": test_case["test_id"],

                    "test_case": test_case,

                    "status": "FAIL",

                    "latency": latency,

                    "reason": (
                        f"HTTP {response.status_code}"
                    ),

                    "response": response.text

                })

                save_results(results)

                continue

            # --------------------------------
            # Parse response
            # --------------------------------

            data = response.json()

            checks = check_trip_result(
                test_case,
                data
            )

            generated_trip = data.get(
                "trip_plan"
            )

            # --------------------------------
            # Count checks
            # --------------------------------

            valid_checks = 0
            passed_checks = 0

            for key in checks:

                if checks[key] is not None:

                    valid_checks += 1

                    if checks[key]:

                        passed_checks += 1

            # --------------------------------
            # PASS / FAIL
            # --------------------------------

            if (
                valid_checks > 0
                and passed_checks == valid_checks
            ):

                passed += 1

                status = "PASS"

            else:

                failed += 1

                status = "FAIL"

            # --------------------------------
            # Save result
            # --------------------------------

            results.append({

                "test_id": test_case["test_id"],

                "test_case": test_case,

                "status": status,

                "checks": checks,

                "latency": latency,

                "generated_trip": generated_trip

            })

            # --------------------------------
            # SAVE AFTER EVERY TEST
            # --------------------------------

            save_results(results)

            print(
                f"   Result: {status}"
            )

        except KeyboardInterrupt:

            print(
                "\n\nEvaluation stopped by user."
            )

            save_results(results)

            print(
                f"Saved {len(results)} "
                f"completed results."
            )

            break

        except Exception as e:

            latency = time.time() - start_time

            total_latency += latency

            failed += 1

            results.append({

                "test_id": test_case["test_id"],

                "test_case": test_case,

                "status": "FAIL",

                "latency": latency,

                "reason": str(e)

            })

            save_results(results)

            print(
                f"   Error: {e}"
            )

    # --------------------------------
    # Final statistics
    # --------------------------------

    completed_tests = len(results)

    if completed_tests > 0:

        success_rate = (
            passed / completed_tests
        ) * 100

        average_latency = (
            total_latency / completed_tests
        )

    else:

        success_rate = 0

        average_latency = 0

    print("\n================================")
    print("       EVALUATION RESULTS")
    print("================================")

    print(
        f"Requested tests: {total_tests}"
    )

    print(
        f"Completed tests: {completed_tests}"
    )

    print(
        f"Passed: {passed}"
    )

    print(
        f"Failed: {failed}"
    )

    print(
        f"Success rate: "
        f"{success_rate:.2f}%"
    )

    print(
        f"Average latency: "
        f"{average_latency:.2f} seconds"
    )

    print(
        f"Results saved to: "
        f"{RESULTS_FILE}"
    )

    print("================================")


if __name__ == "__main__":

    run_evaluation()