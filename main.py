# Press the green button in the gutter to run the script.
from convert import convert

if __name__ == '__main__':
    while (input_file := input("Which file do you want to convert? ")) != "":
        convert(input_file)
    print("Done!")
