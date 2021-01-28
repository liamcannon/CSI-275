#File sort.py
#Lab_1 Sorting with Python
#Author Liam Cannon


def build_list():
    unsortedArray = []
    coll_data = True
    while(coll_data):
        userInput = input("Enter Number for Array: ")
        try:
            check = int(userInput)
            unsortedArray.append(check)
        except Exception:
            try:
                check = float(userInput)
                unsortedArray.append(userInput)
            except Exception: 
                if(userInput == "done"):
                    coll_data = False
                else:
                    print("Not a Num")
    return unsortedArray

def sort_list(unsortedList):
    print("unsorted:", unsortedList)
    unsortedList.sort()
    return unsortedList

def main():
    print("sort:", sort_list(build_list()))

main()
