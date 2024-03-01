import re
import os

class Hooks:
    def __init__(self, input_file, output_folder):
        self.input_file = input_file
        self.output_folder = output_folder

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        _allLines   = []
        _allClasses = []

        for className, line in self.slice(self.filter()).items():
            self.write(className, line)
            _allClasses.append(className)
            for hook in line:
                _allLines.append(hook)
        pass

        _allLines.sort()
        _allClasses.sort()

        if not os.path.exists(output_folder + "/all"):
            os.makedirs(output_folder + "/all")

        self.write("all/PalAllHooks", _allLines)
        self.write("all/PalAllClasses", _allClasses)

    def filter(self):
        functions = set()
        pattern = re.compile(r'\[.+?\]\s+Function\s+(.+?):(\w+)\s')
        with open(self.input_file, 'r') as file:
            for line in file:
                match = pattern.search(line)
                if match:
                    function_name = match.group(1) + ":" + match.group(2)
                    functions.add(function_name)
        return functions

    def slice(self, filteredFunctions):
        
        functions_per_class = {}
        for line in filteredFunctions:
            className = line.split(':')[0].split('.')[-1]
            if className in functions_per_class:
                functions_per_class[className].append(line)
            else:
                functions_per_class[className] = [line]

        return functions_per_class


    def write(self, output_file, slicedFunctions):
        output_path = os.path.join(self.output_folder, f'{output_file}.lua')
        with open(output_path, 'w') as file:
            file.write("local self = {\n")
            for index, function in enumerate(slicedFunctions):
                if index < len(slicedFunctions) - 1:
                    file.write(f'   "{function}",\n')
                else:
                    file.write(f'   "{function}"\n')
            file.write("}\nreturn self")


main_file_path = os.path.abspath(__file__)
parent_directory = os.path.abspath(os.path.join(main_file_path, os.pardir))
grandparent_directory = os.path.abspath(os.path.join(parent_directory, os.pardir))
input_file = os.path.join(parent_directory, "Ue4ssSearchResult.txt")
output_folder = os.path.join(grandparent_directory, "Hooks")
hook_filter = Hooks(input_file, output_folder)