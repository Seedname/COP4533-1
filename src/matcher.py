import pathlib


def matcher(hospitals: list[list[int]], students: list[list[int]], n: int):
    
    hospital_matches = [-1] * n
    student_matches = [-1] * n
    
    if n == 1:
        return [(1, 1)]
    
    # dictionaries for O(1) lookup of preferences
    student_preference_maps = []
    for i in range(n):
        student_preference_maps.append({})
        for j in range(n):
            hospital = students[i][j]-1
            student_preference_maps[-1][hospital] = j
            
    print(student_preference_maps)
    
    
    # count the number of consecutive checks to know when to stop
    count_checks = 0
    while i < n:
        if count_checks == n:
            break
        
        count_checks+=1
        
        for j in range(n):
            # break if we've reached the same optimal matching
            if hospital_matches[i] == j:
                break
            
            curr_student = hospitals[i][j]-1
            # student is unmatched
            if student_matches[curr_student] == -1:
                hospital_matches[i] = curr_student
                student_matches[curr_student] = i
                count_checks = 1
                break
            # student is matched
            else:
                old_hospital = student_matches[curr_student]
                if student_preference_maps[curr_student][old_hospital] > student_preference_maps[curr_student][i]:
                    hospital_matches[old_hospital] = -1
                    student_matches[curr_student] = i
                    hospital_matches[i] = curr_student
                    count_checks = 1
                    break

        i+=1
        if i == n:
            i = 0
    
    # return list of tuples
    matches = []
    for i in range(len(hospital_matches)):
        matches.append((i+1, hospital_matches[i]+1))
        
    return matches
    
if __name__ == "__main__":
    main()


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