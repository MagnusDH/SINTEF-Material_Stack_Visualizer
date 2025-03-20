import globals
from tkinter import messagebox

import numpy as np


#This class handles all equations
class Equations:
    # def __init__(self):
        # print("CLASS EQUATIONS INIT()")
        # pass


    # def calculate_Zn(self):
    #     print("CALCULATE_Zn()")

    #     """
    #     E = modulus *1e9
    #     V = poisson
    #     t = thickness * 1e-9
    #     """

    #     #Get the total number of materials
    #     n = len(globals.materials)

    #     #Check for "zero division errors"
    #     for i in range(1, n+1):
    #         v_i = self.return_poisson(i)
    #         if(1 - (v_i**2) == 0):
    #             messagebox.showerror("Equation error", f"the equation: '1 - (v_{i}**2))' causes a zero division error")
    #             return 

    #     #Term1:
    #     """
    #         E₀          (t₀)²
    #     _________   *   _____
    #     1 - (V₀)²        2            
    #     """

    #     #Calculate term1
    #     E0 = self.return_modulus(1) * 1e9
    #     v0 = self.return_poisson(1)
    #     t0 = self.return_thickness(1) * 1e-9
    #     term1 = (E0 / (1-v0**2))  *   ((t0**2)/2)



        
    #     #Term2 a loop going from i=1 to n=tot materials. j=1
    #     """
    #         Eᵢ
    #     _________   *   tᵢ  *   (sum(tj) (from: j=1 to: i-1))     +       (tᵢ/2)) 
    #     1 - (Vᵢ)²

    #     """


    #     #Calculate term2
    #     term2 = 0

    #     for i in range(2, n+1):
    #         Ei = self.return_modulus(i) * 1e9
    #         vi = self.return_poisson(i)
    #         Ai = Ei / (1 - vi**2) 

    #         ti = self.return_thickness(i) * 1e-9

    #         tj = sum((self.return_thickness(j) * 1e-9) for j in range(2, i-1))    #!!!!!!!!!!!i-1 KAN være feil her

    #         second_sum = tj + (ti / 2)

    #         term2 += Ai * ti * second_sum


    #     #Calculate numerator
    #     numerator = term1 + term2


    #     ####GOOD SO FAR######


    #     #Denominator: a loop going from i=0 to n=tot materials
    #     """
    #         Eᵢ
    #     _________   *   tᵢ 
    #     1 - (Vᵢ)²

    #     """

    #     denominator = 0

    #     for i in range(1, n+1):
    #         Ei = self.return_modulus(i) * 1e9
    #         vi = self.return_poisson(i)
    #         ti = self.return_thickness(i) * 1e-9

    #         denominator += (Ei / 1 - (vi**2)) * ti


        



    #     #Total calculation:
    #     Zn = (numerator / denominator) * 1e9

    #     print(Zn)

    #     return Zn






    """??????????? explain how it calculates the neutral axis"""
    def calculate_Zn(self):
        #Create a list of all the necessary variables
        E = []
        t = []
        nu = []
        for material in globals.materials:
            E.append(globals.materials[material]["Modulus [GPa]"])
            t.append(globals.materials[material]["Thickness"])
            nu.append(globals.materials[material]["Poisson"])

        #Calculate term1
        term1 = (E[0] * (t[0] ** 2)) / (2 * (1 - (nu[0] ** 2)))

        #Calculate term2
        term2 = 0
        for i in range(1, len(t)):
            term2 += (E[i] * t[i] / (1 - (nu[i] ** 2))) * (sum(t[:i]) + t[i] / 2)

        numerator = term1 + term2
        
        denominator = 0
        for i in range(0, len(E)):
            denominator += E[i] / (1-nu[i]**2) * t[i] 

        Zn = numerator / denominator
        
        return Zn
    
    # Function to calculate mid-plane location for the nth layer (z_mid_n)
    def calculate_mid_piezo(self):

        piezo_thickness = globals.materials["PZT"]["Thickness"]


        n = int(globals.materials["PZT"]["Layer"])

        # print(n)

        #j = lag nummer 1 i en setting der lag starter på 0

        #populer en liste som går fra lag 1 til og med PZT laget
        #Regn ut Zp med disse verdiene

        # t = []
        # for i in range(1, n+1):
        #     t.append(globals.materials)


        # return (piezo_thickness / 2) + np.sum(t[:layer-1])
        #FASIT: ZP = 2518.5
        return None
        

    """Returns the 'Modulus [GPa]' value for a material at the given layer"""
    def return_modulus(self, layer):
        # print("RETURN_MODULUS()")

        #loop through all materials and find the material with the correct layer number
        for material in globals.materials:
            if(globals.materials[material]["Layer"] == layer):
                return globals.materials[material]["Modulus [GPa]"]
        
        return None

    """Returns the 'Thickness' value for a material at the given layer"""
    def return_thickness(self, layer):
        # print("RETURN_THICKNESS()")

        #loop through all materials and find the material with the correct layer number
        for material in globals.materials:
            if(globals.materials[material]["Layer"] == layer):
                return globals.materials[material]["Thickness"]
        
        return None

    """Returns the 'Poisson' value for a material at the given layer"""
    def return_poisson(self, layer):
        # print("RETURN_V()")

        #loop through all materials and find the material with the correct layer number
        for material in globals.materials:
            if(globals.materials[material]["Layer"] == layer):
                return globals.materials[material]["Poisson"]
        
        return None
