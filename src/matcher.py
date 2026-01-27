import pathlib


def matcher(hospitals: list[list[int]], students: list[list[int]], n: int):
    pass


def read_input(file_name: str) -> tuple[list[list[int]], list[list[int]], int]:
    parent_dir = pathlib.Path(__file__).parent
    input_directory = parent_dir.parent / "inputs"

    input_file = input_directory / f"{file_name}.in"

    if not input_file.exists():
        raise ValueError(f"Input file {file_name}.in does not exist")

    hospitals: list[list[int]] = []
    students: list[list[int]] = []

    with open(input_file) as f:
        # read the lines of the input file
        lines: list[str] = f.readlines()

        # checks that the file is empty
        if len(lines) == 0:
            raise ValueError("Empty file")

        # check that the first line in the file is a number
        if lines[0].strip().isdigit():
            n = int(lines[0].strip())
        else:
            # else, return an error
            raise ValueError("Number of hospitals/students not properly specified")

        for i in range(2 * n):
            index = i + 1

            # check that the index doesnt exceed the end of the file
            if (i + 1) >= len(lines):
                raise ValueError("Invalid number of elements")
            
            # take the priority list and remove any spaces around elemnts
            priority_list: list[str] = list(map(str.strip, lines[index].strip().split(" ")))

            # makes sure that the priority list has the correct amount of elemnts
            if len(priority_list) != n:
                raise ValueError(f"Invalid length in priority list")

            # checks that the items are all numerical
            if not all(item.isdigit() for item in priority_list):
                raise ValueError("Not all values in priority list are integers")

            if i < n:
                # append the list of priorities to the hospital list (first n elements)
                hospitals.append(list(map(int, priority_list)))
            else:
                # append the list of priorities to the students list (last n elements)
                students.append(list(map(int, priority_list)))

        return hospitals, students, n


if __name__ == "__main__":
    hospitals, students, n = read_input("example")

    print(hospitals)
    print(students)
    print(n)