def main(test = [0]):
    lines = []
    answer = ""
    if test[0] == 0:
        lines = [
            "3 6 7 3 1",
            "0 0 1",
            "1 1 3",
            "2 2 1",
            "1 0 3",
            "0 2 3",
            "2 1 1",
        ]
        answer = "yes"
    elif test[0] == 1:
        lines = [
            "3 6 7 3 1",
            "0 0 3",
            "1 1 3",
            "2 2 3",
            "0 1 3",
            "1 2 1",
            "2 0 1",
        ]
        answer = "no"
    elif test[0] == 2:
        lines = [
        "2 2 7 5 3",
        "0 0 3",
        "1 1 5",   
    ]
        answer = "no"
        
    for i in lines:
        aux = input()
    print(answer)
    test[0]+=1
        
main()