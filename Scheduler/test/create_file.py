import os

def create_unique_file():
    index = 1
    while True:
        file_name = f"{index}.txt"
        if not os.path.exists(file_name):
            with open(file_name, 'w') as file:
                file.write(f"This is file {index}")
            print(f"File {file_name} created.")
            break
        else:
            index += 1

if __name__ == "__main__":
    create_unique_file()

