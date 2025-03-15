import globals
from tkinter import messagebox


#This class handles all equations
class Equations:
    def __init__(self):
        print("CLASS EQUATIONS INIT()")


    def calculate_Zn(self):
        print("CALCULATE_Zn()")

        """
        E = modulus *1e9
        V = poisson
        t = thickness * 1e-9
        """

        #Get the total number of materials
        n = len(globals.materials)

        #Check for "zero division errors"
        for i in range(1, n+1):
            v_i = self.return_poisson(i)
            if(1 - (v_i**2) == 0):
                messagebox.showerror("Equation error", f"the equation: '1 - (v_{i}**2))' causes a zero division error")
                return 

        #Term1:
        """
            E₀          (t₀)²
        _________   *   _____
        1 - (V₀)²        2            
        """

        #Calculate term1
        E0 = self.return_modulus(1) * 1e9
        v0 = self.return_poisson(1)
        t0 = self.return_thickness(1) * 1e-9
        term1 = (E0 / (1-v0**2))  *   ((t0**2)/2)



        
        #Term2 a loop going from i=1 to n=tot materials. j=1
        """
            Eᵢ
        _________   *   tᵢ  *   (sum(tj) (from: j=1 to: i-1))     +       (tᵢ/2)) 
        1 - (Vᵢ)²

        """


        #Calculate term2
        term2 = 0

        for i in range(2, n+1):
            Ei = self.return_modulus(i) * 1e9
            vi = self.return_poisson(i)
            Ai = Ei / (1 - vi**2) 

            ti = self.return_thickness(i) * 1e-9

            tj = sum((self.return_thickness(j) * 1e-9) for j in range(2, i-1))    #!!!!!!!!!!!i-1 KAN være feil her

            second_sum = tj + (ti / 2)

            term2 += Ai * ti * second_sum


        #Calculate numerator
        numerator = term1 + term2


        ####GOOD SO FAR######


        #Denominator: a loop going from i=0 to n=tot materials
        """
            Eᵢ
        _________   *   tᵢ 
        1 - (Vᵢ)²

        """

        denominator = 0

        for i in range(1, n+1):
            Ei = self.return_modulus(i) * 1e9
            vi = self.return_poisson(i)
            ti = self.return_thickness(i) * 1e-9

            denominator += (Ei / 1 - (vi**2)) * ti


        #Total calculation:
        Zn = (numerator / denominator) * 1e9

        print(Zn)

        return Zn
        


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
