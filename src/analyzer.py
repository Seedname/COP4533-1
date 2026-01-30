from matcher import matcher
from verifier import verifier, pretty_print_debug

import matplotlib.pyplot as plt
from tqdm import tqdm

import time
import random
import json
from datetime import datetime
from string import ascii_lowercase as alphabet
import pathlib




def generate_random_preference_lists(n: int) -> tuple[list[list[int]], list[list[int]]]:
    # start off with default preference lists
    hospitals = [list(range(1, n+1)) for _ in range(n)]
    students = [list(range(1, n+1)) for _ in range(n)]

    # shuffle each row in each table
    for hospital in hospitals:
        random.shuffle(hospital)

    for student in students:
        random.shuffle(student)

    # return the lists of students and hospitals
    return hospitals, students


def generate_random_matchings(n: int) -> list[tuple[int, int]]:
    # we can just have one ordered list of hospitals
    # to one randomized list of students
    return list(
        zip(range(1, n+1), # list of hospitals
            random.sample(range(1, n+1), n)) # randomized list of students
        )


def analyze(sizes: list[int], iterations: int):
    data_dir = pathlib.Path(__file__).parent.parent / "data"

    matcher_times: list[int] = [0] * len(sizes)
    verifier_times: list[int] = [0] * len(sizes)

    # perform this iterations times and average the results in the end
    for _ in tqdm(range(iterations)):
        for i, n in enumerate(sizes):
            # generate random preference lists
            hospitals, students = generate_random_preference_lists(n)


            # time the matcher
            matcher_start_time = time.time_ns()
            # run the matcher
            matcher_output = matcher(hospitals, students, n)
            # find the end time
            matcher_end_time = time.time_ns()
            
            # add the difference to the matcher times
            matcher_times[i] += (matcher_end_time - matcher_start_time)

            # generate random matchings for verifier
            random_matchings = generate_random_matchings(n)

            # time the verifier
            verifier_start_time = time.time_ns()
            # run the verifier
            verifier_output = verifier(hospitals, students, n, matcher_output)
            # find the end time
            verifier_end_time = time.time_ns()
            # print(verifier_output)

            # if the matcher gave an invalid match, flag this so we can debug
            # if "INVALID" in verifier_output:
            #     pretty_print_debug(hospitals, students, n, matcher_output)
            #     print(f"\nHospitals:\n{hospitals}\nStudents:\n{students}\nn: {n}")
            #     print(f"Output:\n{matcher_output}")

            #     raise RuntimeError(f"Verifier returned '{verifier_output}', there's a problem with the matcher or verifier")

            # add the difference to the verifier times
            verifier_times[i] += (verifier_end_time - verifier_start_time)
    
    datetime_string = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    # save the times to a file, in case we need it for later
    with open(data_dir / f"output-{datetime_string}.json", 'w') as f:
        json.dump({
            "matcher_times": matcher_times,
            "verifier_times": verifier_times,
            "iterations": iterations,
            "sizes": sizes
        }, f)

    # divide by the number of iterations to get the average time and convert to milliseconds
    matcher_times = [(matcher_time / iterations) for matcher_time in matcher_times]
    verifier_times = [(verifier_time / iterations) for verifier_time in verifier_times]

    # plot the matcher times on a graph
    plt.plot(sizes, matcher_times)
    plt.xlabel("n")
    plt.ylabel("Completion Time (ns)")
    plt.title("Number of hospitals/students vs. Matcher runtime")
    # save it to a file
    plt.savefig(data_dir / f"matcher-{datetime_string}.png")
    # show the figure
    plt.show()
    # close it
    plt.close()

    # plot the verifier times on a graph
    plt.plot(sizes, verifier_times)
    plt.xlabel("n")
    plt.ylabel("Completion Time (ns)")
    plt.title("Number of hospitals/students vs. Verifier runtime")
    # save it to a file
    plt.savefig(data_dir / f"verifier-{datetime_string}.png")
    # show the figure
    plt.show()
    # close it
    plt.close()

    # plot both of them on the same graph
    plt.plot(sizes, matcher_times)
    plt.plot(sizes, verifier_times)
    plt.xlabel("n")
    plt.ylabel("Completion Time (ns)")
    plt.title("Matcher and Verifier runtime scale comparison")
    # save it to a file
    plt.savefig(data_dir / f"matcher-verifier-{datetime_string}.png")
    # show the figure
    plt.show()
    # close it
    plt.close()


if __name__ == "__main__":
    # analyze n = 1, 2, 4, 8, 16, 32, 64, 128, 256, 512 
    # 1 iteration per size
    # analyze(sizes=[1 << i for i in range(10)], iterations=10)

    # analyze n = 1, 6, 11, 16, ..., 1021
    analyze(sizes=list(range(1, 1024, 5)), iterations=10)
