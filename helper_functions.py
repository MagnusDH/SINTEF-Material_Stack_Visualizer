def convert_decimal_string_to_float(string_number):
        """
        -Converts a string to float no matter if it is written with "," or "."\n 
        -Returns the float if sucessfull, returns False if not sucessfull
        """
        # print("CINVERT_DECIMAL_STRING_TO_FLOAT()")
        try:
            new_float = float(string_number)
            return new_float
        
        except:
            if((isinstance(string_number, str)) and ("," in string_number)):
                try:
                    new_float = string_number.replace(",", ".")
                    new_float = float(new_float)
                    return new_float

                except:
                    return False
            else:
                return False