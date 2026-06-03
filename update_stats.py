import requests
import re
import os

LEETCODE_USER = "Ayushology7"
CODEFORCES_USER = "AYUSHOLOGY"

def get_leetcode_stats():
    try:
        url = f"https://leetcode-stats-api.herokuapp.com/{LEETCODE_USER}"
        response = requests.get(url, timeout=10).json()
        return response.get("totalSolved", 0)
    except Exception as e:
        print(f"Error fetching LeetCode: {e}")
        return 0

def get_codeforces_stats():
    try:
        url = f"https://codeforces.com/api/user.status?handle={CODEFORCES_USER}"
        response = requests.get(url, timeout=10).json()
        if response.get("status") == "OK":
            solved = set()
            for submission in response["result"]:
                if submission["verdict"] == "OK":
                    # Unique identifier for a problem
                    problem_id = f"{submission['problem']['contestId']}-{submission['problem']['index']}"
                    solved.add(problem_id)
            return len(solved)
    except Exception as e:
        print(f"Error fetching Codeforces: {e}")
        return 0

# Adjust this number manually if you want to include CodeChef/GFG base counts
BASE_OTHER_PLATFORMS_COUNT = 0 

def main():
    lc_count = get_leetcode_stats()
    cf_count = get_codeforces_stats()
    
    total_solved = lc_count + cf_count + BASE_OTHER_PLATFORMS_COUNT
    print(f"LeetCode: {lc_count}")
    print(f"Codeforces: {cf_count}")
    print(f"Total Solved: {total_solved}")

    # Read the current README
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            readme_content = f.read()
    except FileNotFoundError:
        print("README.md not found!")
        return

    # Replace the count between the markers using Regex
    pattern = r"(<!-- stats:start -->).*?(<!-- stats:end -->)"
    replacement = rf"\1{total_solved}\2"
    updated_readme = re.sub(pattern, replacement, readme_content, flags=re.DOTALL)

    # Write the updated content back to README.md
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated_readme)
    print("README.md updated successfully!")

if __name__ == "__main__":
    main()
