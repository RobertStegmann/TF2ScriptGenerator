import argparse, sys

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-input', help='Input File')
    parser.add_argument('-key', help='Bind Key')
    parser.add_argument('-alias', help='Bind Alias')
    parser.add_argument('-cycle', help='Cycle Alias')
    parser.add_argument('-output', help='Output File')
    parser.add_argument('-wait', help='Time in frames between messages')
    
    args = parser.parse_args()
    
    if args.input is None:
        print("Please provide all required arguments:")
        parser.print_help()
        exit(1)
    else:
        input = args.input
    
    if args.key is None:
        key = "RIGHTARROW"
    else:
        key = args.key
        
    if args.alias is None:
        alias = "BINDNAME"
    else:
        alias = args.alias
        
    if args.cycle is None:
        cycle = "CYCLE"
    else:
        cycle = args.cycle
        
    if args.output is None:
        output = "output.txt"
    else:
        output = args.output
        
    if args.wait is None:
        wait = 500
    else:
        wait = int(args.wait) 
        
    generateCycleBind(input,key,alias,cycle,output,wait)
        
        
def generateCycleBind(input,key,alias,cycle,output,wait):
    inputFile = open(input, "r")
    outputFile = open(output, "w")
    outputFile.write("// Place this in your autoexec.cfg file or any .cfg file you'd like\n")
    outputFile.write("// Every time that .cfg is ran (For example, every time the game is launched for autoexec.cfg), the cycle starts from the beginning\n")
    outputFile.write("// The binds will go in order, there is no randomization\n")
    outputFile.write(f"// If you would like to jump to somewhere in the list, type 'alias {alias} \"{cycle}[whatever number here]\"' in the developer console\n")
    outputFile.write("\n")
    outputFile.write(f"bind {key} \"{alias}\"\n")
    outputFile.write("\n")
    i = 0
    outputFile.write(f"alias {alias} \"{cycle}0\"\n")
    for input_line in inputFile:
        line = input_line.strip().replace("\"","\'")
        if len(line) > 0:
            if i > 0:
                outputFile.write(f"alias {alias} {cycle}{i}\"\n") 
            if len(line) > 0:
                if len(line) <= 127:
                    outputFile.write(f"alias {cycle}{i} \"say {line};")   
                else:
                    lines = splitLines(line)
                    length = len(lines)
                    if length > 0:
                        for j in range(1,length):
                            if j > 1:
                                outputFile.write(f";{alias}{i}{j+1};\"\n")
                            outputFile.write(f"alias {alias}{i}{j} \"wait {wait}; say {lines[j]}")
                        outputFile.write(f"\"\nalias {cycle}{i} \"say {lines[0]}; {alias}{i}1;") 
                
        i += 1
    
    inputFile.close()
        
    outputFile.write(f"alias {alias} {cycle}0\"\n")
    
    outputFile.close()
    
def splitLines(line):
    correct_split = False
    seperators = [". ","! ","? ",", ",": "]
    for seperator in seperators:
        if seperator in line:
            split_lines = line.split(seperator,1)
            correct_split = True
            for i in range(0,len(split_lines)):
                if i < len(split_lines) - 1:
                    split_lines[i] = split_lines[i] + seperator.strip()
                if len(split_lines[i]) > 127:
                    correct_split = False
            
            if correct_split:
                return split_lines
            j = 1
            if len(split_lines[0]) <= 127:
                while (not correct_split) and seperator in split_lines[j]:
                    newSplit = split_lines[j].split(seperator,1)
                    split_lines[j] = newSplit[0] + seperator.strip()
                    split_lines.append(newSplit[1])
                    if len(split_lines[j]) > 127:
                        break
                    if len(newSplit[1]) <= 127:
                        correct_split = True
                if correct_split:
                    return split_lines
                                   
    words = line.split(" ")
    correct_line = ""
    splits = []
    for word in words:
        if len(word) > 127:
            return []
        if (len(correct_line) + len(word) + 1) > 127:
            splits.append(correct_line)
            correct_line = word
        else:
            if len(correct_line) > 0:
                correct_line = f"{correct_line} {word}"
            else:
                correct_line = word
    if len(correct_line) > 0:
        splits.append(correct_line)
    return splits                

if __name__ == "__main__":
    main()