import globals
import tkinter
from tkinter import messagebox
import helper_functions
from scipy.optimize import fsolve


#This class handles all equations
class Equations:
    # def __init__(self):
        # print("CLASS EQUATIONS INIT()")
            

    def calculate_Zn(self, E:list, t:list, nu:list):
        """
        Calculates the neutral axis value for the given materials\n

        PARAMETERS:\n     
            E: list of "Modulus" values in unit: Pascal
            t: list of "Thickness" values in unit: meters
            nu: list of "Poisson" values in unit: "no special unit"

        Returns "Zn" in unit: meters
        """
        #print("CALCULATE_ZN()")

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
    

    def calculate_mid_piezo(self, t:list, Zn:float, piezo_thickness:float):
        """
        Calculates mid-plane location for the nth layer (z_mid_n)\n

        PARAMETERS:\n
            t: list of "thickness" values in "meters" for materials from layer1 up til chosen piezo material.
            Zn: value in "meters"
            piezo_thickness: "thickness" of chosen piezo material in "meters"

        Returns "Zp" in unit: meters
        """
        # print("CALCULATE_MID_PIEZO()")

        #Calculate Zp
        Zp = (piezo_thickness / 2) + sum(t) - Zn

        return Zp 


    def calculate_EI(self, E:list, t:list, nu:list, W:float, Zn:float):
        """
        Function to calculate flexural rigidity (EI) scaled to SI-units\n

        PARAMETERS:\n
            E: list of "Modulus" values in unit: pascal
            t: list of "Thickness" values in unit: meters
            nu: list of "Poisson" values in unit: "no special unit"
            W: value in unit: meters
            Zn: value in unit: meters

        Returns "EI" in unit: newton meter**2
        """
        # print("CALCULATE_EI()")

        EI = W * ((E[0] / (1 - nu[0]**2)) * (t[0]**3 / 12 + t[0] * (t[0]/2 - Zn)**2))
        
        EI += W * sum([
        
        E[i] / (1 - nu[i]**2) * (t[i]**3 / 12 + t[i] * (sum(t[:i]) + t[i]/2 - Zn)**2)
        for i in range(1, len(t))
        ])

        return EI


    def calculate_M_is_cantilever(self, Zn:float, sigma_i:list, t:list, W:float):
        """
        Function to calculate cantilever stress bending moment (M_tot)\n

        PARAMETERS:\n
            sigma_i: list of "Stress_x" values in unit: pascal
            W: value in unit: meters
            Zn: value in unit: meters

        Returns M_is value in unit: newton meters
        """

        #Calculate M_tot
        term1 = W * t[0] * sigma_i[0] * (t[0] / 2 - Zn)
        term2 = sum(W * t[i] * sigma_i[i] * (sum(t[:i]) + t[i] / 2 - Zn) for i in range(1, len(t)))
        M_is = term1 + term2

        return M_is


    def calculate_M_tot_cantilever(self, M_is:float, M_p:float):
        """
        PARAMETERS:\n
            M_is: value in unit: newton meters
            M_p: value in unit: newton meters

        Returns M_tot value in unit: newton meters
        """
        
        M_tot = M_is + M_p

        return M_tot
    

    def calculate_curvature(self, M_tot:float, EI:float):
        """
        Function to calculate Curvature\n

        PARAMETERS:\n
            M_tot: value in unit: newton meters
            EI: value in unit: newton meter**2

        Return curv_is in unit: 1/meters
        """

        curv_is = M_tot / EI

        return curv_is


    def calculate_tip_placement(self, curv_is:float, L:float):
        """
        Calculates tip displacement for a given "length/L" value\n

        PARAMETERS:
            curv_is: value in unit: 1/meters
            L: value in unit: micrometers

        Return z_tip_tot in unit: micrometers
        """

        z_tip_tot = 0.5 * curv_is * L**2

        #Convert to micrometers
        z_tip_tot = z_tip_tot * 1e6

        return z_tip_tot


    def calculate_M_p_cantilever(self, Zp:float, W:float, V_p:float, e_31_f:float):
        """
        Calculates cantilever piezoelectric moment (M_p)

        PARAMETERS:\n
            Zp: value in unit: meters
            W: value in unit: meters
            V_p: value in unit: volt
            e_31_f: value in unit: c/m2

        Returns "M_p" in unit: newton meters
        """
        # print("CALCULATE_M_P_CANTILEVER()")

        #Calculate M_p value
        M_p = e_31_f * V_p * Zp * W

        return M_p


    #HVA ER RETUR VERDI???
    def neutralize_global_stress(self, t:list, L:float, curv_is:float):
        """
        Objective function for fsolve: sets the second-layer thickness to t_guess[0],
        computes the resulting tip displacement, then restores the original thickness.
        Returns the tip displacement in the same units that calculate_tip_placement uses\n

        PARAMETERS:\n
            t: list of thickness values in unit: meters
            L: value in unit: meters

        Returns z_tip in unit: meters??
        """
        # Identify the second layer key (assumes ordering in globals.materials)
        layer_keys = list(globals.materials.keys())
        second_key = layer_keys[1]

        # Backup original thickness and set the trial value
        original_thickness = globals.materials[second_key]["Thickness [nm]"]
        globals.materials[second_key]["Thickness [nm]"] = t

        #calculate_tip_placement expects L in μm and returns z_tip in μm
        z_tip = self.calculate_tip_placement(curv_is, L)

        # Restore original thickness
        globals.materials[second_key]["Thickness [nm]"] = original_thickness

        print("t_guess:", t)
        print("L:", L)

        return z_tip
    

    def find_t_solution(self, L:float, curv_is:float):
        """
        Solve for and return the thickness of the second layer that makes the
        stress-induced tip displacement zero.\n

        Returns the neutralizing thickness in unit: nanometer
        """
        # print("FIND_T_SOLUTION()")

        # print(L, curv_is)

        # Identify second layer current thickness
        t_guess = float(globals.materials["SiO2"]["Thickness [nm]"]) / 1e9  #Extract scalar from array

        t = []
        for material in globals.materials:
            t.append(float(globals.materials[material]["Thickness [nm]"]) / 1e9)

        # Use fsolve to find the root of neutralize_global_stress
        t_sol = fsolve(self.neutralize_global_stress(t, L, curv_is), [t_guess])[0]

        return t_sol


    #ADD EXPLANATION OF FUNCTION
    def calculate_blocking_force(self, E:list, t:list, V:float, e_31_f:float, h_PZT:float, h_Si:float, w:float, L:float):
        '''
        Blocking force calculations
        '''
        #Piezo & substrate compliances
        S11_PZT = 13.8e-12      # [m²/N]  from Jaffe/Tyholdt
        S12_PZT = -4.07e-12     # [m²/N]
        S11_Si  = 1.0 / E[0]    # [m²/N], isotropic Si approximation

        # 9) Effective d31 for thin film (m/V)
        
        d31 = e_31_f * (S11_PZT + S12_PZT)

        # 10) Layer thicknesses for blocking force formula
        h_PZT = t[3]            # PZT layer thickness [m]
        h_Si  = t[0]            # substrate layer thickness [m]
        num = -3 * d31 * h_Si * (h_PZT + h_Si) * w
        den =  4 * (S11_PZT * h_Si + S11_Si * h_PZT) * L

        blocking_force = (num/den) * V

        return blocking_force












    # def neutralize_global_stress(t1):
    #     t_temp = t.copy()
    #     t_temp[1] = t1[0]  # Extract scalar from array
    #     zn = calculate_zn(E, t_temp, nu)
    #     EI = calculate_EI(E, t_temp, nu, w, zn)
    #     M_is = calculate_M_is_cantilever(w, t_temp, sigma, zn)
    #     curv_is = M_is / EI
    #     z_tip_is = 0.5 * curv_is * l**2
    #     return z_tip_is
    

    # def find_t1_solution():
    #     """
    #     Solve for and return the thickness t[1] that makes the 
    #     stress‐induced tip displacement zero.
    #     """
    #     # use the current global t[1] as the initial guess
    #     t_initial_guess = t[1]
    #     # fsolve expects an array‐like initial guess
    #     t1_sol = fsolve(neutralize_global_stress, [t_initial_guess])[0]
    #     return t1_sol


