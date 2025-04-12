import globals
from tkinter import messagebox
import helper_functions

#This class handles all equations
class Equations:
    # def __init__(self):
        # print("CLASS EQUATIONS INIT()")


    def calculate_Zn(self):
        """
        -Calculates the neutral axis value for the materials in the stack\n
        -Returns the 'Zn' value
        -Return value is nanometer
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
    

    def calculate_mid_piezo(self):
        """
        -Calculates mid-plane location for the nth layer (z_mid_n)\n 
        -Return value is Zp in nanometers
        """
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

        Zn = self.calculate_Zn()

        Zp = (piezo_thickness / 2) + sum(t) - Zn
        # Zp = (piezo_thickness / 2) + sum(t)

        return Zp 


    def calculate_EI(self):
        """
        -Function to calculate flexural rigidity (EI)
        -Scaled to SI-units 
        -Return value is 'newton meter**2'
        """
        # print("CALCULATE_EI()")

        #Create lists of all the necessary variables
        E = []
        t = []
        nu = []
        for material in globals.materials:
            E.append(globals.materials[material]["Modulus [GPa]"] * 1e9)    #multiplied with 1 billion
            t.append(globals.materials[material]["Thickness"] / 1e9)       #divided by 1 billion
            nu.append(globals.materials[material]["Poisson"])

        #Fetch the 'w' value from new_panel
        W = helper_functions.convert_decimal_string_to_float(globals.new_panel.W_value.get())
        if(W == 0 or W == False):
            messagebox.showerror("ERROR", "'W [μm]' entry can not be zero or empty")
            return None

        #Convert to micrometers
        W = W / 1e6

        # w = 160e-6  # width in meters

        #Find Zn value
        Zn = self.calculate_Zn() / 1e9 #divided by 1 billion to get correct value


        EI = W * ((E[0] / (1 - nu[0]**2)) * (t[0]**3 / 12 + t[0] * (t[0]/2 - Zn)**2))
        EI += W * sum([
        E[i] / (1 - nu[i]**2) * (t[i]**3 / 12 + t[i] * (sum(t[:i]) + t[i]/2 - Zn)**2)
        for i in range(1, len(t))
        ])

        return EI


    #NOT DONE
    def calculate_M_is_cantilever(self):
        """
        -Function to calculate cantilever stress bending moment (M_is)\n
        -Return value is 'newton meter'
        """

        #Create lists of all the necessary variables
        E = []
        t = []
        nu = []
        sigma_i = []
        for material in globals.materials:
            E.append(globals.materials[material]["Modulus [GPa]"] * 1e9)
            t.append(globals.materials[material]["Thickness"] / 1e9)
            nu.append(globals.materials[material]["Poisson"])
            sigma_i.append(globals.materials[material]["Stress_x [MPa]"] * 1e6)


        #Fetch the 'w' value from new_panel
        W = helper_functions.convert_decimal_string_to_float(globals.new_panel.W_value.get())
        if(W == 0 or W == False):
            messagebox.showerror("ERROR", "'W [μm]' entry can not be zero or empty")
            return None

        #Convert to micrometers
        W = W / 1e6

        # w = 160e-6  # width in meters

        if(W == 0 or W == False):
            messagebox.showerror("ERROR", "'W [μm]' entry can not be zero or empty")
            return None

        #Calculate Zn value
        Zn = self.calculate_Zn() / 1e9

        term1 = W * t[0] * sigma_i[0] * (t[0] / 2 - Zn)
        term2 = sum(W * t[i] * sigma_i[i] * (sum(t[:i]) + t[i] / 2 - Zn) for i in range(1, len(t)))

        M_is = term1 + term2

        return M_is


    def calculate_curvature(self):
        """
        -Curvature calculation\n
        -return value is in 1/meters
        """

        M_is = self.calculate_M_is_cantilever()
        if(M_is == None):
            return

        EI = self.calculate_EI()
        if(EI == None):
            return

        curv_is = M_is / EI

        return curv_is

    #NOT DONE
    def calculate_tip_placement(self):
        """
        -Tip displacement calculation\n
        -return value is in meters
        """
        curv_is = self.calculate_curvature()

        #Fetch the 'L' value from new_panel
        L = helper_functions.convert_decimal_string_to_float(globals.new_panel.L_value.get())
        # L = 1000e-6  #length in meters
        
        if(L == 0 or L == False):
            messagebox.showerror("ERROR", "'L [μm]' entry can not be zero or empty")
            return None

        #Convert to micrometers
        L = L / 1e6

        z_tip_is = 0.5 * curv_is * L**2

        return z_tip_is


    def tip_displacement_zero():
        """???????????????"""
        print("TIP_DISPLACEMENT_ZERO()")

        t1 = float(globals.materials["SIO2"]["Thickness"])
        
        t_temp = t.copy()
        t_temp[1] = t1[0]  # Extract scalar from array

        zn = calculate_zn(E, t_temp, nu)
        EI = calculate_EI(E, t_temp, nu, w, zn)
        M_is = calculate_M_is_cantilever(w, t_temp, sigma, zn)
        curv_is = M_is / EI
        z_tip_is = 0.5 * curv_is * l**2

        return z_tip_is
