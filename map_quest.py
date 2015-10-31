# Darshan Parajuli 16602518
# ICS 32 Fall 2015
# Project 3


from output_generators import OutputGenerators


def get_num_locations() -> int:
    num = _get_input_as_int()
    if num == None:
        _print_error_msg('The first line must specify a positive integer number of locations.')
    elif num < 2:
        _print_error_msg('You must specify at least two locations to run this experiment.')
    else:
       return num


def get_locations(num_locations: int) -> [str]:
    locations = []
    for i in range(num_locations):
        user_input = input().strip()
        if user_input == '':
            _print_error_msg('Location cannot be an empty string.')
            return None
        
        locations.append(user_input)

    return locations


def get_num_output_generators() -> str:
    num = _get_input_as_int()
    if num == None or num < 1:
        _print_error_msg('There must be a positive integer number of generators.')
    else:
       return num

   
def get_output_generators(num_generators: int) -> [str]:
    output_generators = []
    for i in range(num_generators):
        user_input = input().strip()
        if not OutputGenerators.is_valid_output_generator(user_input):
            _print_error_msg('Invalid output type: {}'.format(user_input if user_input != '' else 'undefined'))
            return None

        output_generators.append(user_input)

    return output_generators


def get_output(locations: [str], output_generators: [str]) -> [[str]]:
    output_gen = OutputGenerators(locations)
    output = []
    for output_generator_type in output_generators:
        output_generator = output_gen.get_ouput_generator(output_generator_type)
        if output_generator != None:
            output.append(output_generator.get_output())

    return output


def print_result(output: [[str]]) -> None:
    for list_element in output:
        if list_element != None:
            for element in list_element:
                print(element)
        
    print()
    print('Directions Courtesy of MapQuest; Map Data Copyright OpenStreetMap Contributors')

def _get_input_as_int() -> int:
    try:
        return int(input().strip())
    except ValueError:
        return None

    
def _print_error_msg(error_msg: str):
    print('\n{}'.format(error_msg))

    
def main() -> None:
    num_locations = get_num_locations()
    if num_locations == None:
        return

    locations = get_locations(num_locations)
    if locations == None:
        return
    
    num_generators = get_num_output_generators()
    if num_generators == None:
        return

    output_generators = get_output_generators(num_generators)
    if output_generators == None:
        return

    output = get_output(locations, output_generators)
    print_result(output)
    
    
if __name__ == '__main__':
    main()
