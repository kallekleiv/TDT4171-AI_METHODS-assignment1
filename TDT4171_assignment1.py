import random
import statistics
import matplotlib.pyplot as plt
import seaborn as sns


# Spins the slot machine, returning a three tuple of symbols
def spin_slot_machine():
    combination = []
    symbols = ["BAR", "BELL", "LEMON", "CHERRY"]
    for _ in range(3):
        combination.append(random.choice(symbols))
    return tuple(combination)


# Pattern matches the combination, returning the appropriate payout
def check_payout(result):
    match result:
        case ("BAR", "BAR", "BAR"):
            return 20
        case ("BELL", "BELL", "BELL"):
            return 15
        case ("LEMON", "LEMON", "LEMON"):
            return 5
        case ("CHERRY", "CHERRY", "CHERRY"):
            return 3
        case ("CHERRY", "CHERRY", _):
            return 2
        case ("CHERRY", _, _): 
            return 1
    return 0


# Runs a simulation with balance of 10, checking how many rounds it can go before tapping out
# Returns a tuple of containing (1) number of rounds until broke and (2) the win/loss ratio
def play(balance):
    num_rounds = won_rounds = 0

    while balance > 0:
        num_rounds = num_rounds + 1
        combination = spin_slot_machine()
        payout = check_payout(combination)
        payout_bool = payout > 0 
        balance = balance + payout - 1

        if payout_bool:
            won_rounds = won_rounds + 1

    win_ratio = won_rounds/num_rounds
    return (num_rounds, win_ratio)


# Calculate the chance that two people in a group of n people share birthdays
def calculate_birthday_probability(n):
    chance = 1
    for x in range(0, n):
        chance = chance * (365-x)/365
    return (1 - chance)


# Adds a person with a random birthday to the group. When each birthday in list_of_people is True, the function returns
# the number of additions that had to be made in the group
def add_person_to_group():
    num_persons = 0
    list_of_people = [False] * 365
    group_filled = False

    while not group_filled:
        new_birthday = random.randint(0, 364)
        list_of_people[new_birthday] = True
        num_persons = num_persons + 1
        if num_persons > 366:
            group_filled = all(x == True for x in list_of_people)

    return num_persons


# Constants
N_SIMULATIONS = 1000
BALANCE = 10


def exercise_1():
    num_rounds_data = []
    win_ratio_data = []
    for _ in range(N_SIMULATIONS):
        temp = play(BALANCE)
        num_rounds_data.append(temp[0])
        win_ratio_data.append(temp[1])

    # Visualization
    sns.set_style("whitegrid")
    plt.title("Slot Machine Results 1a")
    plt.ylabel("Rounds played before loss")
    y_median = round(statistics.median(num_rounds_data), 1)
    y_mean = round(statistics.mean(num_rounds_data), 1)
    plt.axhline(y_median, c='red', linestyle="--", label="Median: " + str(y_median))
    plt.axhline(y_mean, c='green', linestyle="-", label="Mean: " + str(y_mean))
    sns.scatterplot(num_rounds_data)
    plt.show()

    # We'll plot it with y between 0 and a 1000, so the median and mean are visible. The mean is more sensitive to
    # skewed data, which is why it is 10 times higher than the median.
    plt.title("Slot Machine Results 1b")
    plt.ylabel("Rounds played before loss")
    y_median = round(statistics.median(num_rounds_data), 1)
    y_mean = round(statistics.mean(num_rounds_data), 1)
    plt.axhline(y_median, c='red', linestyle="--", label="Median: " + str(y_median))
    plt.axhline(y_mean, c='green', linestyle="-", label="Mean: " + str(y_mean))
    sns.scatterplot(num_rounds_data)
    plt.ylim(0, 1000)
    plt.show()

    # Let's look at the win ratio, just for fun
    plt.title("Slot Machine Results 2")
    plt.ylabel("Win ratio")
    win_ratio_median = round(statistics.median(win_ratio_data), 3)
    win_ratio_mean = round(statistics.mean(win_ratio_data), 3)
    plt.axhline(win_ratio_median, c='red', linestyle="--", label="Median: " + str(win_ratio_median))
    plt.axhline(win_ratio_mean, c='green', linestyle="-", label="Mean: " + str(win_ratio_mean))
    sns.scatterplot(win_ratio_data)
    plt.show()

    print("Results after " + str(N_SIMULATIONS) + " simulations:\n")
    print("Median number of rounds played before going broke: " + str(y_median))
    print("Mean number of rounds played before going broke: " + str(y_mean))
    print("Mean win_ratio: " + str(win_ratio_mean))


def exercise_2():
    # Calculate probability in the interval 0 (0% chance of birthday sharing) to 366 people (100% chance of birthday
    # sharing)
    data = []
    for n in range(0, 366):
        probability = calculate_birthday_probability(n)
        data.append(probability)

    # Now we'll calculate the proportion of N where the event happens with at least 50% chance, and the the smallest N
    # where the probability of the event is at least 50%
    smallest_n = next(x for x, probability in enumerate(data) if probability > 0.5)
    left_bound = 10
    right_bound = 50
    proportion = (right_bound - smallest_n)/(right_bound - left_bound)

    print("Proportion of N where the event happens with at least 50% chance: " + str(proportion))
    print("Smallest N where the probability is at least 50%: " + str(smallest_n))

    # Let's visualize the probability. At 1 it is 0, and at 366 it is 100%
    plt.ylabel("Probability")
    plt.xlabel("n")
    plt.title("Probability that two people share birthdays")
    sns.lineplot(data)
    plt.ylim(0, 1)
    plt.xlim(0, 100)
    plt.axhline(y=0.5, c='green', linestyle="--", label="50%")
    plt.axvline(x=smallest_n, c='red', linestyle="-", label="Smallest n: " + str(smallest_n))
    plt.legend()
    plt.show()

    # Runs simulation n times
    birthday_data = []
    for _ in range(N_SIMULATIONS):
        birthday_data.append(add_person_to_group())

    # Let's plot each attempt, and find the median and mean number of additions that had to be made!
    plt.title("Every Date a Birthday")
    plt.ylabel("Additions before every date covered")
    y_median = round(statistics.median(birthday_data), 0)
    y_mean = round(statistics.mean(birthday_data), 0)
    plt.axhline(y_median, c='red', linestyle="-", label="Median: " + str(int(y_median)) + " additions")
    plt.axhline(y_mean, c='green', linestyle="-", label="Mean: " + str(int(y_mean)) + " additions")
    sns.scatterplot(birthday_data)
    plt.show()


def main():
    exercise_1()
    exercise_2()


if __name__ == "__main__":
    main()