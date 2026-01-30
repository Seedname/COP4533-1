from matcher import read_input
from matcher import matcher

def main() -> None:
    pass

if __name__ == "__main__":
    hospitals, students, n = read_input("example")

    print(hospitals)
    print(students)
    print(n)
    
    print(matcher(hospitals, students, n))