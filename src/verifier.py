import pathlib
from matcher import read_input, matcher
from string import ascii_lowercase as alphabet


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
        for student in hospitals[hospital]:
            # adjust to 0 based indexing
            student = student - 1

            # this hospital is already matched to its best candidate
            if student == hospital_matches[hospital]:
                break

            # check all the hospitals in the students preference list
            for preferred_hospital in students[student]:
                # adjust to 0 based indexing
                preferred_hospital = preferred_hospital - 1

                # check if the preferred hospital is the one its matched to
                # if its good, continue checking the other hospitals
                if preferred_hospital == student_matches[student]:
                    break

                # check if the preferred hospital is the one that we're testing
                # this means that the hospital prefers this student more than the student its currently matched to
                # and this student prefers this hospital more than the one its matched to
                if preferred_hospital == hospital:
                    # debug with letters to make it easier
                    # if n <= 13:
                    #     print(f"Hospital {alphabet[preferred_hospital]} prefers student {alphabet[student + 26 - n]} and vice versa")

                    # if so, its an unstable match
                    return "INVALID (Unstable match)"

    return "VALID STABLE"


def pretty_print_debug(hospitals: list[list[int]], students: list[list[int]], n: int, matcher_output: list[tuple[int, int]]) -> None:
    # can use letters
    if n <= 13:
        print("Hospitals")
        print("\n".join(alphabet[i] + ": " 
                        + " ".join(alphabet[student - 1 + 26 - n] for student in hospital) 
                        for i, hospital in enumerate(hospitals)))

        print("\nStudents")
        print("\n".join(alphabet[i + 26 - n] + ": " 
                        + " ".join(alphabet[hospital - 1] for hospital in student) 
                        for i, student in enumerate(students)))
        
        print("\nMatches")
        print("\n".join(f"{alphabet[hospital - 1]} - {alphabet[student - 1 + 26 - n]}" for hospital, student in matcher_output))



def read_output(file_name: str, n: int) -> list[tuple[int, int]]:
    parent_dir = pathlib.Path(__file__).parent
    input_directory = parent_dir.parent / "outputs"

    output_file = input_directory / f"{file_name}.out"

    if not output_file.exists():
        raise ValueError(f"Input file {file_name}.in does not exist")

    pairings: list[tuple[int, int]] = []

    with open(output_file, 'r') as f:
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
    file_name = "test" # Change this variable to update file name

    hospitals, students, n = read_input(file_name)
    example_output = read_output(file_name, n)

    message = verifier(hospitals, students, n, example_output)

    pretty_print_debug(hospitals, students, n, example_output)

    print(message)
