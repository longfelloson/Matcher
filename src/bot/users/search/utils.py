import random


def shift_numbers(numbers: list[int], index: int = None) -> list:
    if index is None:
        index = len(numbers) // 2
    
    if index < 0 or index >= len(numbers):
        raise ValueError("Index is out of bounds.")
    
    shift_direction = random.choice(["left", "right"])
    numbers_to_shift = random.choice([1, 2])

    if shift_direction == "left":
        numbers_to_shift_list = numbers[:index + 1]
        first_number = numbers_to_shift_list[0]

        if numbers_to_shift == 2:
            extension = [first_number - 2, first_number - 1]
            return extension + numbers_to_shift_list
        else:
            extension = [first_number - 1]
            addition = [numbers_to_shift_list[-1] + 1]
            return extension + numbers_to_shift_list + addition
    elif shift_direction == "right":
        numbers_to_shift_list = numbers[index:]
        last_number = numbers_to_shift_list[-1]
        
        if numbers_to_shift == 2:
            extension = [last_number + 1, last_number + 2]
            return numbers_to_shift_list + extension
        else:
            extension = [numbers_to_shift_list[0] - 1]
            addition = [last_number + 1]
            return extension + numbers_to_shift_list + addition


def get_age_range(
    user_age: int, 
    shift: bool = False,
    extend: bool = False,
) -> list:
    age_range = list(range(user_age - 2, user_age + 3)) 

    if extend:
        age_range = list(range(user_age - 4, user_age + 5))
    elif shift:
        age_range = shift_numbers(age_range)

    return age_range
