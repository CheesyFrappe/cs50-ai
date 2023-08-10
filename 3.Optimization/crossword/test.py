def main():
    temp = dict()
    temp["a"] = {1, 2, 3}
    temp["f"] = {1, 2}
    temp["x"] = {1, 2, 3, 6}

    temp_sorted = sorted(temp.items(), key=lambda x:x[1])
    
    min = len(temp_sorted[0][1])
    
    for val in temp_sorted:
        print(val)
        if len(val[1]) == min:
            temp_sorted.remove(val)
    
    

if __name__ == "__main__":
    main()