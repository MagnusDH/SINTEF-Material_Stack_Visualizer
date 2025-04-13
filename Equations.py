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

        #Populate a list with thickness values from layer1 up until "PZT" material
        t = []
        for material in globals.materials:
            if(material.lower() == "pzt"):
                break

            t.append(globals.materials[material]["Thickness"])
            
        #Fetch thickness value for Piezo material
        piezo_thickness = globals.materials[material]["Thickness"]

        #Calculate Zn
        Zn = self.calculate_Zn()

        #Calculate Zp
        Zp = (piezo_thickness / 2) + sum(t) - Zn

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

        #Fetch the 'W_entry' value from new_panel
        W = helper_functions.convert_decimal_string_to_float(globals.new_panel.W_value.get())
        if(W == 0 or W == False):
            messagebox.showerror("ERROR", "'W [μm]' entry can not be zero or empty")
            return None

        #Convert W value to micrometers
        W = W / 1e6

        #Calculate Zn value
        Zn = self.calculate_Zn() / 1e9 #divided by 1 billion to get correct value


        EI = W * ((E[0] / (1 - nu[0]**2)) * (t[0]**3 / 12 + t[0] * (t[0]/2 - Zn)**2))
        
        EI += W * sum([
        
        E[i] / (1 - nu[i]**2) * (t[i]**3 / 12 + t[i] * (sum(t[:i]) + t[i]/2 - Zn)**2)
        for i in range(1, len(t))
        ])

        return EI


    def calculate_M_tot_cantilever(self):
        """
        -Function to calculate cantilever stress bending moment (M_tot)\n
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


        #Fetch the 'W_entry' value from new_panel
        W = helper_functions.convert_decimal_string_to_float(globals.new_panel.W_value.get())
        if(W == 0 or W == False):
            messagebox.showerror("ERROR", "'W [μm]' entry can not be zero or empty")
            return None

        #Convert W_value to micrometers
        W = W / 1e6

        if(W == 0 or W == False):
            messagebox.showerror("ERROR", "'W [μm]' entry can not be zero or empty")
            return None

        #Calculate Zn value
        Zn = self.calculate_Zn() / 1e9

        #Calculate M_tot
        term1 = W * t[0] * sigma_i[0] * (t[0] / 2 - Zn)
        term2 = sum(W * t[i] * sigma_i[i] * (sum(t[:i]) + t[i] / 2 - Zn) for i in range(1, len(t)))
        M_tot = term1 + term2 + self.calculate_M_p_cantilever()

        return M_tot


    def calculate_curvature(self):
        """
        -Curvature calculation\n
        -return value is in 1/meters
        """

        M_tot = self.calculate_M_tot_cantilever()
        #If W_entry value is zero and M_tot function returns None, return
        if(M_tot == None):
            return

        EI = self.calculate_EI()
        #If W_entry value is zero and calculate_EI function returns None, return
        if(EI == None):
            return

        curv_is = M_tot / EI

        return curv_is

    #NOT DONE
    def calculate_tip_placement(self, L):
        """
        -Tip displacement calculation for a given "length/L" value\n
        -return value is in meters
        """
        curv_is = self.calculate_curvature()

        # #Fetch the 'L' value from new_panel
        # L = helper_functions.convert_decimal_string_to_float(globals.new_panel.L_value.get())
        # # L = 1000e-6  #length in meters
        
        # if(L == 0 or L == False):
        #     messagebox.showerror("ERROR", "'L [μm]' entry can not be zero or empty")
        #     return None

        #Convert L to micrometers
        L = L / 1e6

        z_tip_tot = 0.5 * curv_is * L**2

        return z_tip_tot * 1e6


    #NOT DONE AND NOT IN USE 
    def tip_displacement_zero(self):
        """???????????????"""
        print("TIP_DISPLACEMENT_ZERO()")

        t = []
        for material in globals.materials:
            t.append(globals.materials[material]["Thickness"])

        #CONVERT this to lower case!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        t1 = float(globals.materials["SiO2"]["Thickness"])

        # t_temp = t.copy()
        # t_temp[1] = t1[0]  #Extract scalar from array

        #Fetch the 'L' value from new_panel
        L = helper_functions.convert_decimal_string_to_float(globals.new_panel.L_entry.get())
        
        #Convert to micrometers
        L = L / 1e6


        zn = self.calculate_Zn()
        EI = self.calculate_EI()
        M_tot = self.calculate_M_tot_cantilever()
        curv_is = M_tot / EI
        
        z_tip_tot = 0.5 * curv_is * L**2

        return z_tip_tot


    def calculate_M_p_cantilever(self):
        """
        -Function to calculate cantilever piezoelectric moment (M_p)
        """
        # print("CALCULATE_M_P_CANTILEVER()")

        #Calculate Zp value
        Zp = self.calculate_mid_piezo() / 1e9

        #Fetch the 'W_entry' value from new_panel
        W = helper_functions.convert_decimal_string_to_float(globals.new_panel.W_value.get())
        if(W == 0 or W == False):
            messagebox.showerror("ERROR", "'W [μm]' entry can not be zero or empty")
            return None
        #Convert to micrometers
        W = W / 1e6

        #Fetch the 'volt' value from new_panel
        V_p = helper_functions.convert_decimal_string_to_float(globals.new_panel.volt_entry.get())

        #Fetch the 'e_31_f' value from new_panel
        e_31_f = helper_functions.convert_decimal_string_to_float(globals.new_panel.e_31_f_entry.get())

        #Calculate M_p value
        M_p = e_31_f * V_p * Zp * W

        return M_p
