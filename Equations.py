# import globals
# import tkinter
# from tkinter import messagebox
# import helper_functions
from scipy.optimize import fsolve


class Equations:
    # def __init__(self):
        # print("CLASS EQUATIONS INIT()")
            

    def calculate_Zn(self, E:list, t:list, nu:list):
        """
        Calculates the neutral axis value for the given materials\n

        PARAMETERS:\n     
            E: list of Modulus values in unit "Pascal"
            t: list of Thickness values in unit "meters"
            nu: list of Poisson values in unit: "no special unit"

        The function returns "Zn" in unit "meters" if successfull.
        If not successfull the error is returned.
        """
        #print("CALCULATE_ZN()")

        try:
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
        
        except Exception as error:
            return error

    
    def calculate_mid_piezo(self, t:list, Zn:float, piezo_thickness:float):
        """
        Calculates mid-plane location for the nth layer (z_mid_n)\n

        PARAMETERS:\n
            t: list of thickness values in unit "meters" for materials from layer1 up til chosen piezo material.
            Zn: value in unit "meters"
            piezo_thickness: thickness of chosen piezo material in unit "meters"

        Returns "Zp" in unit "meters" if succesfull.
        If not successfull the error is returned.
        """
        # print("CALCULATE_MID_PIEZO()")

        try:
            #Calculate Zp
            Zp = (piezo_thickness / 2) + sum(t) - Zn

            return Zp 

        except Exception as error:
            return error


    def calculate_EI(self, E:list, t:list, nu:list, W:float, Zn:float):
        """
        Function to calculate flexural rigidity (EI) scaled to SI-units\n

        PARAMETERS:\n
            E: list of Modulus values in unit "pascal"
            t: list of Thickness values in unit "meters"
            nu: list of Poisson values in unit: "no special unit"
            W: value in unit "meters"
            Zn: value in unit "meters"

        Returns "EI" in unit "newton meter**2" if succesfull.
        If not successfull the error is returned.
        """
        # print("CALCULATE_EI()")

        try:
            EI = W * ((E[0] / (1 - nu[0]**2)) * (t[0]**3 / 12 + t[0] * (t[0]/2 - Zn)**2))
            
            EI += W * sum([        
            E[i] / (1 - nu[i]**2) * (t[i]**3 / 12 + t[i] * (sum(t[:i]) + t[i]/2 - Zn)**2)
            for i in range(1, len(t))
            ])

            return EI
        
        except Exception as error:
            return error


    def calculate_M_is_cantilever(self, Zn:float, sigma_i:list, t:list, W:float):
        """
        Function to calculate cantilever stress bending moment (M_tot)\n

        PARAMETERS:\n
            sigma_i: list of Stress_x values in unit "pascal"
            W: value in unit "meters"
            Zn: value in unit "meters"

        Returns "M_is" in unit "newton meters" if succesfull.
        If not successfull the error is returned.
        """

        # print("CALCULATE_M_IS_CANTILEVER")

        try:
            #Calculate M_tot
            term1 = W * t[0] * sigma_i[0] * (t[0] / 2 - Zn)
            term2 = sum(W * t[i] * sigma_i[i] * (sum(t[:i]) + t[i] / 2 - Zn) for i in range(1, len(t)))
            M_is = term1 + term2

            return M_is
        
        except Exception as error:
            return error


    def calculate_M_tot_cantilever(self, M_is:float, cumulative_M_p:float):
        """
        PARAMETERS:\n
            M_is: value in unit "newton meters"
            cumulative_M_p: value in unit "newton meters"

        Returns "M_tot" in unit "newton meters" if succesfull.
        If not successfull the error is returned.
        """
        try:
            M_tot = M_is + cumulative_M_p

            return M_tot

        except Exception as error:
            return error


    def calculate_curvature(self, M_tot:float, EI:float):
        """
        Function to calculate Curvature\n

        PARAMETERS:\n
            M_tot: value in unit "newton meters"
            EI: value in unit "newton meter**2"

        Returns "curv_is" in unit "1/meters" if succesfull.
        If not successfull the error is returned.
        """

        try:
            curv_is = M_tot / EI

            return curv_is
    
        except Exception as error:
            return error


    def calculate_tip_placement(self, curv_is:float, L:float):
        """
        Calculates tip displacement for a given "length/L" value\n

        PARAMETERS:
            curv_is: value in unit "1/meters"
            L: value in unit "micrometers"

        Returns "z_tip_tot" in unit "micrometers" if succesfull.
        If not successfull the error is returned.
        """
        try:
            z_tip_tot = 0.5 * curv_is * L**2

            #Convert to micrometers
            z_tip_tot = z_tip_tot * 1e6

            return z_tip_tot
        
        except Exception as error:
            return error


    def calculate_Mp_cantilever(self, Zp:float, W:float, V_p:float, e_31_f:float):
        """
        Calculates cantilever piezoelectric moment (M_p)

        PARAMETERS:\n
            Zp: value in unit "meters"
            W: value in unit "meters"
            V_p: value in unit "volt"
            e_31_f: value in unit "c/m2"

        Returns "Mp" in unit "newton meters" if succesfull.
        If not successfull the error is returned.
        """
        # print("CALCULATE_M_P_CANTILEVER()")

        try:
            #Calculate Mp value
            Mp = e_31_f * V_p * Zp * W

            return Mp

        except Exception as error:
            return error


    def calculate_cumulative_Mp_cantilever(self, Zp:list, W:float, V_p:float, e_31_f:float):
        """
        Calculates the cumulative cantilever piezoelectric moment (cumulative_Mp)

        PARAMETERS:\n
            Zp: list of zp values in unit "meters"
            W: value in unit "meters"
            V_p: value in unit "volt"
            e_31_f: value in unit "c/m2"

        Returns "cumulative_M_p" in unit "newton meters" if succesfull.
        If not successfull the error is returned.
        """
        # print("CALCULATE_M_P_CANTILEVER()")

        try:
            #Calculate M_p value
            cumulative_Mp = e_31_f * V_p * sum(Zp) * W

            return cumulative_Mp

        except Exception as error:
            return error

    #HVA ER RETUR VERDI???
    #hva er second_thickness?
    def neutralize_global_stress(self, second_thickness, t:list, L:float, curv_is:float):
        """
        Objective function for fsolve: sets the second-layer thickness to t_guess[0],
        computes the resulting tip displacement, then restores the original thickness.
        Returns the tip displacement in the same units that calculate_tip_placement uses\n

        PARAMETERS:\n
            second_thickness: ????????????????????????????
            t: list of thickness values in unit "meters"
            L: value in unit "meters"
            SiO2_thickness in unit "meters"

        Returns "z_tip" in unit "meters??" if succesfull.
        If not successfull the error is returned.
        """

        try:
            #Identify the second layer key (assumes ordering in globals.materials)
            # layer_keys = list(globals.materials.keys())
            # second_key = layer_keys[1]

            # # Backup original thickness and set the trial value
            # original_thickness =  globals.materials[second_key]["Thickness [nm]"]
            # globals.materials[second_key]["Thickness [nm]"] = t

            #calculate_tip_placement expects L in μm and returns z_tip in μm
            z_tip = self.calculate_tip_placement(curv_is, L)

            # Restore original thickness
            # globals.materials[second_key]["Thickness [nm]"] = original_thickness

            return z_tip
        
        except Exception as error:
            return error


    def find_t_solution(self, t:list, L:float, curv_is:float, neutralizing_material_thickness:float):
        """
        Solve for and return the thickness of the second layer that makes the
        stress-induced tip displacement zero.\n

        PARAMETERS:\n
            t: list of thickness values in unit "meters"
            L: value in unit "meters"
            curv_is: value in unit "1/meters"
            neutralizing_material_thickness: thickness of neutralizing material in unit "meters"

        Returns the neutralizing thickness in unit: "meter" if succesfull.
        If not successfull the error is returned.
        """
        # print("FIND_T_SOLUTION()")

        try:
            #Convert neutralizing_material_thickness into a list object so it can be used in "fsolve"
            neutralizing_material_thickness = [neutralizing_material_thickness]

            #Use fsolve to find the root of neutralize_global_stress
            t_sol = fsolve(self.neutralize_global_stress(t, L, curv_is), neutralizing_material_thickness)[0]

            return t_sol
        
        except Exception as error:
            return error


    def calculate_blocking_force(self, E:list, t:list, V_p:float, e_31_f:float, piezo_thickness:float, h_Si:float, w:float, L:float):
        """
        Blocking force calculation.

        PARAMETERS:\n
            E: list of Modulus values in unit "pascal"
            t: list of thickness values in unit "meters"
            V: value in "volt"
            e_31_f: value in unit "c/m2"
            piezo_thickness: thickness of chosen piezo material in unit "meters" 
            h_Si: thickness of materials from substrate up to (but not including) chosen piezo material
            W: value in unit "meters"
            L: value in unit "meters"

        Returns the "blocking force" if succesfull.
        If not successfull the error is returned.
        """        

        try:
            #Piezo & substrate compliances
            S11_PZT = 13.8e-12      # [m²/N]  from Jaffe/Tyholdt
            S12_PZT = -4.07e-12     # [m²/N]
            S11_Si  = 1.0 / E[0]    # [m²/N], isotropic Si approximation

            # 9) Effective d31 for thin film (m/V)
            
            d31 = e_31_f * (S11_PZT + S12_PZT)

            # 10) Layer thicknesses for blocking force formula
            h_Si  = t[0]            # substrate layer thickness [m]
            num = -3 * d31 * h_Si * (piezo_thickness + h_Si) * w
            den =  4 * (S11_PZT * h_Si + S11_Si * piezo_thickness) * L

            blocking_force = (num/den) * V_p

            return blocking_force
        
        except Exception as error:
            return error
        