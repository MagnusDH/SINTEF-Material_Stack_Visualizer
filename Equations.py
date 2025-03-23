import globals
from tkinter import messagebox


#This class handles all equations
class Equations:
    # def __init__(self):
        # print("CLASS EQUATIONS INIT()")
        # pass


    def calculate_Zn(self):
        """
        -Calculates the neutral axis value for the materials in the stack\n
        -Returns the 'Zn' value
        """
        # print("CALCULATE_ZN()")
        #Create a list of all the necessary variables
        E = []
        t = []
        nu = []
        for material in globals.materials:
            E.append(globals.materials[material]["Modulus [GPa]"])
            t.append(globals.materials[material]["Thickness"])
            nu.append(globals.materials[material]["Poisson"])

        #Check for "zero division errors"
        for i in range(len(nu)):
            if(1 - (nu[i]**2) == 0):
                messagebox.showerror("Equation error", f"the equation: '1 - (nu{i}**2))' causes a zero division error because the 'poisson' value of a material equals 1")
                return 

        #Calculate term1
        term1 = (E[0] * (t[0] ** 2)) / (2 * (1 - (nu[0] ** 2)))

        #Calculate term2
        term2 = 0
        for i in range(1, len(t)):
            term2 += (E[i] * t[i] / (1 - (nu[i] ** 2))) * (sum(t[:i]) + t[i] / 2)

        numerator = term1 + term2

        #Calculate denominator        
        denominator = 0
        for i in range(0, len(E)):
            denominator += E[i] / (1-nu[i]**2) * t[i] 

        Zn = numerator / denominator
        
        return Zn
    

    """????????????????????????????????????????"""
    #Function to calculate mid-plane location for the nth layer (z_mid_n)
    def calculate_mid_piezo(self, Zn):
        # print("CALCULATE_MID_PIEZO()")

        #j = lag nummer 1 i en setting der lag starter på 0

        piezo_thickness = 0
        #populer en liste som går fra lag 1 til og med PZT laget
        t = []
        for material in globals.materials:
            if(material.lower() == "pzt"):
                break

            t.append(globals.materials[material]["Thickness"])
            


        piezo_thickness = globals.materials[material]["Thickness"]

        # Zp = (piezo_thickness / 2) + sum(t) - Zn
        Zp = (piezo_thickness / 2) + sum(t)

        return Zp 


    def return_modulus(self, layer:int):
        """Returns the 'Modulus [GPa]' value for a material at the given layer"""
        # print("RETURN_MODULUS()")

        #loop through all materials and find the material with the correct layer number
        for material in globals.materials:
            if(globals.materials[material]["Layer"] == layer):
                return globals.materials[material]["Modulus [GPa]"]
        
        return None


    def return_thickness(self, layer:int):
        """Returns the 'Thickness' value for a material at the given layer"""
        #print("RETURN_THICKNESS()")

        #loop through all materials and find the material with the correct layer number
        for material in globals.materials:
            if(globals.materials[material]["Layer"] == layer):
                return globals.materials[material]["Thickness"]
        
        return None


    def return_poisson(self, layer:int):
        """Returns the 'Poisson' value for a material at the given layer"""
        # print("RETURN_V()")

        #loop through all materials and find the material with the correct layer number
        for material in globals.materials:
            if(globals.materials[material]["Layer"] == layer):
                return globals.materials[material]["Poisson"]
        
        return None
