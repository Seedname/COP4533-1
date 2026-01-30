import pathlib
from matcher import read_input, matcher


def verifier(hospitals: list[list[int]], students: list[list[int]], n: int, matcher_output: list[tuple[int, int]]) -> str:
    hospital_matches = [0] * n
    student_matches = [0] * n

    # ungroup matchings into easily accessible lists
    for hospital, student in matcher_output:
        hospital_matches[hospital - 1] = student - 1
        student_matches[student - 1] = hospital - 1

    # make sure there's a correct number of matches
    if len(matcher_output) != n:
        return "INVALID (Incorrect number of matches)"

    # check that there are no duplicate matches
    if len(set(hospital_matches)) != n or len(set(student_matches)) != n:
        return "INVALID (Duplicate matches detected)"

    # loop through all the hospitals
    for hospital in range(n):
        # check all the students that the hospital prefers more
        for student_index in range(n):
            # this hospital is already matched to its best candidate
            if student_index == hospital_matches[hospital]:
                break
            
            # get the student from the hospitals preference list
            student = hospitals[hospital][student_index] - 1

            # check all the hospitals in the students preference list
            for preferred_hospital in students[student]:
                # adjust to 0 based indexing
                preferred_hospital = preferred_hospital - 1

                # check if the preferred hospital is the one its matched to
                # if its good, continue checking
                if preferred_hospital == student_matches[student]:
                    break

                # check if the preferred hospital is the one that we're testing
                if preferred_hospital == hospital:
                    # if so, its an unstable match
                    return "INVALID (Unstable match)" 

    return "VALID STABLE"


def read_output(file_name: str, n: int) -> list[tuple[int, int]]:
    parent_dir = pathlib.Path(__file__).parent
    input_directory = parent_dir.parent / "outputs"

    output_file = input_directory / f"{file_name}.out"

    if not output_file.exists():
        raise ValueError(f"Input file {file_name}.in does not exist")

    pairings: list[tuple[int, int]] = []

    with open(output_file) as f:
        lines = f.readlines()

        # make sure theres the correct number of pairs
        if len(lines) != n:
            raise ValueError("Invalid number of matches")

        # split the lines by spaces
        pairs = [line.strip().split(" ") for line in lines]

        # check if there are two items per pair
        if not all(len(pair) == 2 for pair in pairs):
            raise ValueError("Not all lines have a pair")

        # check if all items are digits
        if not all((value.isdigit() for value in pair) for pair in pairs):
            raise ValueError("Not all values in priority list are integers")

        # convert the pairs to integers
        pairings = [tuple(int(num) for num in pair) for pair in pairs]

    return pairings


if __name__ == "__main__":
    hospitals, students, n = read_input("example")
    example_output = read_output("example", n)

    message = verifier(hospitals, students, n, example_output)
    print(message)
