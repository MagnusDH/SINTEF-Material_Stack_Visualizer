import globals
from tkinter import messagebox
import helper_functions
from scipy.optimize import fsolve


#This class handles all equations
class Equations:
    # def __init__(self):
        # print("CLASS EQUATIONS INIT()")


    def calculate_Zn(self):#E:list, t:list, nu:list):
        """
        -Calculates the neutral axis value for the given materials\n
        -Returns the 'Zn' value in nanometers\n

        PARAMETERS:        
        E = list of "Modulus [GPa]" values\n
        t = list of "Thickness" values in nanometers\n
        nu = list of "Poisson" values\n

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
    

    #NOT DONE
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


    #NOT DONE
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

        #Convert W value to micrometers
        W = 160
        W = W / 1e6

        #Calculate Zn value
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


        #Convert W value to micrometers
        W = 160
        W = W / 1e6

        #Calculate Zn value
        Zn = self.calculate_Zn() / 1e9

        #Calculate M_tot
        term1 = W * t[0] * sigma_i[0] * (t[0] / 2 - Zn)
        term2 = sum(W * t[i] * sigma_i[i] * (sum(t[:i]) + t[i] / 2 - Zn) for i in range(1, len(t)))
        M_is = term1 + term2

        return M_is


    #NOT DONE
    def calculate_M_tot_cantilever(self):
        
        M_tot = self.calculate_M_is_cantilever() + self.calculate_M_p_cantilever()

        return M_tot
    

    #NOT DONE
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

        #Convert L to micrometers
        L = L / 1e6

        z_tip_tot = 0.5 * curv_is * L**2

        return z_tip_tot * 1e6


    #NOT DONE
    def calculate_M_p_cantilever(self):#, Zp:float, W:float, V_p:float, e_31_f:float):
        """
        -Function to calculate cantilever piezoelectric moment (M_p)
        
        -Parameters:\n
        Zp unit ???
        W unit ???
        V_p unit ???
        e_31_f unit ???
        """
        # print("CALCULATE_M_P_CANTILEVER()")

        #Calculate Zp value
        Zp = self.calculate_mid_piezo() / 1e9

        #Convert W value to micrometers
        W = 160
        W = W / 1e6

        #Fetch the 'volt' value from new_panel
        V_p = helper_functions.convert_decimal_string_to_float(globals.new_panel.volt_entry.get())

        #Fetch the 'e_31_f' value from new_panel
        e_31_f = helper_functions.convert_decimal_string_to_float(globals.new_panel.e_31_f_entry.get())

        #Calculate M_p value
        M_p = e_31_f * V_p * Zp * W

        return M_p


    #NOT DONE
    def neutralize_global_stress(self, t_guess):
        """
        Objective function for fsolve: sets the second-layer thickness to t_guess[0],
        computes the resulting tip displacement, then restores the original thickness.
        Returns the tip displacement in the same units that calculate_tip_placement uses.
        """
        # Identify the second layer key (assumes ordering in globals.materials)
        layer_keys = list(globals.materials.keys())
        second_key = layer_keys[1]

        # Backup original thickness and set the trial value
        original_thickness = globals.materials[second_key]["Thickness"]
        globals.materials[second_key]["Thickness"] = t_guess[0]

        #Fetch L and compute tip displacement
        L_val = helper_functions.convert_decimal_string_to_float(globals.new_panel.L_entry.get())

        #calculate_tip_placement expects L in μm and returns z_tip in μm
        z_tip = self.calculate_tip_placement(L_val)

        # Restore original thickness
        globals.materials[second_key]["Thickness"] = original_thickness
        
        return z_tip
    

    #NOT DONE
    def find_t_solution(self):
        """
        Solve for and return the thickness of the second layer that makes the
        stress-induced tip displacement zero.
        """
        # print("FIND_T_SOLUTION()")

        # Identify second layer current thickness
        t_guess = float(globals.materials["SiO2"]["Thickness"])  #Extract scalar from array

        # Use fsolve to find the root of neutralize_global_stress
        t_sol = fsolve(self.neutralize_global_stress, [t_guess])[0]
        # print(f'Neutralizing thickness is: {t_sol} nm')
        
        return t_sol


