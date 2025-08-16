# import globals
# import tkinter
# from tkinter import messagebox
# import helper_functions
import numpy as np
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
            term1 = (E[0] * (t[0] * 2)) / (2 * (1 - (nu[0] * 2)))

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
            Zn: value in unit "meters"
            sigma_i: list of Stress_x values in unit "pascal"
            t: list of Thickness values in unit "meters"
            W: value in unit "meters"

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


    #HERE IS A NEW FUNCTION with an error!!!
    def calculate_is_curvature(self, M_tot:float, EI:float):
        """
        Function to calculate Curvature\n

        PARAMETERS:\n
            M_tot: value in unit "newton meters"
            EI: value in unit "newton meter**2"

        Returns "curv_is"    if succesfull.
        If not successfull the error is returned.
        """

        try:
            curv_is = M_is / EI

            return curv_is
    
        except Exception as error:
            return error


    def calculate_curvature(self, M_tot:float, EI:float):
        """
        Function to calculate Curvature\n

        PARAMETERS:\n
            M_tot: value in unit "newton meters"
            EI: value in unit "newton meter**2"

        Returns "curv_is"    if succesfull.
        If not successfull the error is returned.
        """

        try:
            curv_tot = M_tot / EI

            return curv_tot
    
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

    def neutralize_global_stress(self, t1, E:list, t:list, nu:list, W:float, L:float, sigma_i:list):
        """
        Given a trial thickness t1 for layer 2 (SiO2), compute the stress-only
        tip displacement (meters). fsolve will drive this to ~0.

        PARAMETERS:
        t1: ?????
        E: ?????
        t: list of thickness values in unit "meters"
        nu: ?????
        W: ?????
        L: value in unit "meters"
        sigma_i: ?????   

        Returns "z_tip_is" in unit "meters??" if succesfull.
        If not successfull the error is returned.
        """
        try:
            # make a working copy and set layer-2 thickness
            t_work = list(t)            # copy so we don't mutate the caller's list
            t_work[1] = float(t1)       # set SiO2 thickness
    
            # recompute with this trial stack
            Zn = self.calculate_Zn(E, t_work, nu)
            EI = self.calculate_EI(E, t_work, nu, W, Zn)
            M_is = self.calculate_M_is_cantilever(Zn, sigma_i, t_work, W)
    
            # curvature and tip deflection (meters)
            curv_is = M_is / EI
            z_tip_is = 0.5 * curv_is * (L ** 2)
    
            return z_tip_is
        
        except Exception as error:
            return error

    def find_t_solution(self, E:list, t:list, nu:list, sigma_i:list, W:float, L:float):
        """
        Solve for the layer-2 (SiO2) thickness that makes the stress-only
        tip displacement zero. Returns thickness in meters.

        PARAMETERS:\n
            E: ????
            t: list of thickness values in unit "meters"
            nu: ????
            sigma_i: ????
            W: ????
            L: value in unit "meters"

        Returns the neutralizing thickness in unit: "meter" if succesfull.
        If not successfull the error is returned.
        """
        try:
            # t1_guess = float(t[1]) #Tykkelse på SiO2 - "neutralizing filament"
            # t1_guess = globals.materials[globals.neutralizing_material_name.get()]["Thickness [nm]"].get() 
            t1_guess = 1e-6

            # print(globals.neutralizing_material_name.get())
    
            # root function: only t1 varies; everything else is captured
            def root_fn(t1):
                return self.neutralize_global_stress(t1, E, t, nu, W, L, sigma_i)
    
            t1_sol = fsolve(root_fn, x0=t1_guess)[0]
            print(t1_sol)
            return float(t1_sol)
        
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
            h_Si: thickness of materials from substrate up to (but not including) chosen piezo material in unit "meters"
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

    def solve_sigma_for_target_curvature(self, curv_is: float,
                                         E: list, t: list, nu: list, W: float,
                                         sigma_i: list, layer_index: int = 3):
        """
        Solve for sigma_i[layer_index] (Pa) that yields the given stress-only curvature (1/m).
    
        PARAMETERS:
            curv_is: target stress-induced curvature (1/m)
            E, t, nu: lists (SI units) for modulus (Pa), thickness (m), Poisson (-)
            W: beam width (m)
            sigma_i: list of current layer stresses (Pa); sigma_i[layer_index] will be solved
            layer_index: which layer's stress to solve for (default 3 => 4th layer)
    
        RETURNS:
            sigma_required (Pa) or raises ValueError on singular geometry.
        """
        # Make safe copies
        E = list(E); t = list(t); nu = list(nu); sigma = list(sigma_i)
    
        # Geometry / stiffness
        Zn = self.calculate_Zn(E, t, nu)
        EI = self.calculate_EI(E, t, nu, W, Zn)
    
        # Target bending moment from desired curvature
        M_target = curv_is * EI
    
        # Helper: centroid lever arm of layer i relative to Zn
        def lever_arm(i):
            return (sum(t[:i]) + t[i]/2.0) - Zn
    
        # Moment from all other layers (exclude the solved layer)
        M_others = 0.0
        for i in range(len(t)):
            if i == layer_index:
                continue
            M_others += W * t[i] * sigma[i] * lever_arm(i)
    
        # Denominator term for the unknown layer
        denom = W * t[layer_index] * lever_arm(layer_index)
        if abs(denom) < 1e-30:
            raise ValueError(
                f"Layer {layer_index} centroid is at the neutral axis (lever arm ~ 0); "
                "cannot achieve the target curvature by changing this layer's stress."
            )
    
        # Solve for the required stress in the chosen layer (Pa)
        sigma_required = (M_target - M_others) / denom
        return sigma_required