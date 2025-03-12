import globals

#This class handles all equations
class Equations:
    def __init__(self):
        print("CLASS EQUATIONS INIT()")


    def calculate_Zn(self):
        print("CALCULATE_Zn()")

        #EXPLANATION OF TERMS USED IN EQUATION


        #Term1:
        """
            E₀          (t₀)²
        _________   *   _____
        1 - (V₀)²        2            
        """
        
        #Ai:
        """
            Eᵢ
        _________
        1 - (Vᵢ)²

        """

        
        #sum_Ai: sum of all 'Ai' calculations from i=1 to n=total number of materials
        """
            E₁              E₂
        _________   +  _____________
        1 - (V₁)²       1 - (V₂)² 
        """

        #Term2



    
        #TODO
            #Find E0
            #Find V0
            #Check: if( 1 - (V0**2) == 0):
                #Return divison by zero error
                #return
            
            #Calculate: E0 / 1 - (V0**2)
            
            
            
            
            #o calculate from)  
            #Set n=number of layers
            #Calculate "A(i)" for each material


        Zn = None   #Neutral line
        E0 = None   #E of substrate
        t0 = None   #Thickness of substrate
        V0 = None   #Poisson of substrate
        n = None    #number of material layers
        i = None    #Current material layer
        Ei = None   #E of current material
        Vi = None   #Poisson of current material
        ti = None   #Thickness of current material
        j = None    #Current material layer of second sum calculation
        tj = None


        return 500000
        

    """Returns the 'Modulus [GPa]' value for a material at the given layer"""
    def return_modulus(self, layer):
        # print("RETURN_MODULUS()")

        #loop through all materials and find the material with the correct layer number
        for material in globals.materials:
            if(globals.materials[material]["Layer"] == layer):
                return globals.materials[material]["Modulus [GPa]"]
        
        return None