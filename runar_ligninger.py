# Function to calculate flexural rigidity (EI)

def calculate_EI(E, t, nu, w, zn):

    EI = w * ((E[0] / (1 - nu[0]**2)) * (t[0]**3 / 12 + t[0] * (t[0]/2 - zn)**2))

    EI += w * np.sum([

        E[i] / (1 - nu[i]**2) * (t[i]**3 / 12 + t[i] * (np.sum(t[:i]) + t[i]/2 - zn)**2)

        for i in range(1, len(t))

    ])

    return EI

 

# Function to calculate cantilever stress bending moment (M_is)

def calculate_M_is_cantilever(w, t, sigma_i, zn):

    term1 = w * t[0] * sigma_i[0] * (t[0] / 2 - zn)

    term2 = sum(w * t[i] * sigma_i[i] * (np.sum(t[:i]) + t[i] / 2 - zn) for i in range(1, len(t)))

    return term1 + term2

 

'''

Calculation for cantilevers

 

'''

 

w = 160e-6  # width in meters

l = 1000e-6  # length in meters

 

# Calculate zn, EI, and M_is

zn = calculate_zn(E, t, nu)

zp = calculate_z_mid_n(t, 4, zn)

EI = calculate_EI(E, t, nu, w, zn)

M_is = calculate_M_is_cantilever(w, t, sigma, zn)

 

# Curvature calculation

curv_is = M_is / EI

 

# Tip displacement calculation

z_tip_is = 0.5 * curv_is * l**2

 

print('Cantilever: length ' + str(l*10**6) + ' µm, width ' + str(w*10**6) + ' µm')

print(f'Zn = {zn*1e9:.2f} nm \n'

      f'EI = {EI:.4e} Nm² \n'

      f'M = {M_is:.4e} Nm\n'

      f'Z_tip = {z_tip_is*1e9:.2f} nm\n'

      f'Curve = {curv_is:.4e} 1/m')





#FASIT
Cantilever: length 1000.0 µm, width 160.0 µm

Zn = 2475.92 nm

EI = 3.3816e-10 Nm²

M = 3.4344e-08 Nm

Z_tip = 50780.50 nm

Curve = 1.0156e+02 m^-1

 

 