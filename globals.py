import tkinter

#The main dictionary where ALL materials and info about each material is stored
materials = {}

#Reference to all classes
app = None
material_adjustment_panel = None
material_control_panel = None
parameters_panel = None
layer_stack_canvas = None
canvas_control_panel = None
graph_canvas = None
graph_control_panel = None
equations = None

#Reference to current sizes of program window
current_program_window_height = None
current_program_window_width = None


#TEMPORARY DICTIONARY FOR RUNAR TO USE (key is material name, value is Zp value)
zp = {}

def initialize_globals(root_window):
    """
    Creates variables that are used globaly in the program
    """
    # print("INITIALIZE_GLOBALS()")

    global current_view
    current_view = tkinter.StringVar(value="Multi")
    current_view.trace_add("write", lambda *args, identifier="current_view_updated": app.update_widgets(identifier))

    global piezo_material_name
    piezo_material_name = tkinter.StringVar(value="")
    piezo_material_name.trace_add("write", lambda *args, identifier="piezo_material_updated": app.update_widgets(identifier))

    global L_value
    L_value = tkinter.DoubleVar(value=1000)
    L_value.trace_add("write", lambda *args, identifier="L_value_updated": app.update_widgets(identifier))
    
    global e_31_f_value
    e_31_f_value = tkinter.DoubleVar(value=18)
    e_31_f_value.trace_add("write", lambda *args, identifier="e_31_f_value_updated": app.update_widgets(identifier))

    global volt_value
    volt_value = tkinter.DoubleVar(value=0)
    volt_value.trace_add("write", lambda *args, identifier="volt_value_updated": app.update_widgets(identifier))

    global neutralizing_material_name
    neutralizing_material_name = tkinter.StringVar(value="")
    neutralizing_material_name.trace_add("write", lambda *args, identifier="neutralizing_material_updated": app.update_widgets(identifier))

    # global stress_neutral_SiO2_thickness_value
    # stress_neutral_SiO2_thickness_value = tkinter.DoubleVar(value=0)
    # stress_neutral_SiO2_thickness_value.trace_add("write", lambda *args, identifier="stress_neutral_SiO2_thickness_value": app.update_widgets(identifier))

    # global piezoelectric_bending_moment_value
    # piezoelectric_bending_moment_value = tkinter.DoubleVar(value=0)
    # piezoelectric_bending_moment_value.trace_add("write", lambda *args, identifier="piezoelectric_bending_moment_value": app.update_widgets(identifier))
    
    global blocking_force_cantilever
    blocking_force_cantilever = tkinter.DoubleVar(value=0)
    blocking_force_cantilever.trace_add("write", lambda *args, identifier="blocking_force_cantilever_updated": app.update_widgets(identifier))
    
    # global initial_curvature_value
    # initial_curvature_value = tkinter.DoubleVar(value=0)
    # initial_curvature_value.trace_add("write", lambda *args, identifier="initial_curvature_value": app.update_widgets(identifier))
    
    # global final_curvature_value
    # final_curvature_value = tkinter.DoubleVar(value=0)
    # final_curvature_value.trace_add("write", lambda *args, identifier="final_curvature_value": app.update_widgets(identifier))

    # global Zn
    # Zn = tkinter.DoubleVar(value=0)
    # Zn.trace_add("write", lambda *args, identifier="Zn": app.update_widgets(identifier))
    
    # global Zp
    # Zp = tkinter.DoubleVar(value=0)
    # Zp.trace_add("write", lambda *args, identifier="Zp": app.update_widgets(identifier))
    
    # global EI
    # EI = tkinter.DoubleVar(value=0)
    # EI.trace_add("write", lambda *args, identifier="EI": app.update_widgets(identifier))
    
    # global M_is
    # M_is = tkinter.DoubleVar(value=0)
    # M_is.trace_add("write", lambda *args, identifier="M_is": app.update_widgets(identifier))
    
    # global M_tot
    # M_tot = tkinter.DoubleVar(value=0)
    # M_tot.trace_add("write", lambda *args, identifier="M_tot": app.update_widgets(identifier))
    
    # global curv_is
    # curv_is = tkinter.DoubleVar(value=0)
    # curv_is.trace_add("write", lambda *args, identifier="curv_is": app.update_widgets(identifier))
    
    # global z_tip_tot
    # z_tip_tot = tkinter.DoubleVar(value=0)
    # z_tip_tot.trace_add("write", lambda *args, identifier="z_tip_tot": app.update_widgets(identifier))
    
    global M_p
    M_p = tkinter.DoubleVar(value=0)
    M_p.trace_add("write", lambda *args, identifier="M_p": app.update_widgets(identifier))
    
    # global z_tip
    # z_tip = tkinter.DoubleVar(value=0)
    # z_tip.trace_add("write", lambda *args, identifier="z_tip": app.update_widgets(identifier))
    
    global t_sol
    t_sol = tkinter.DoubleVar(value=0)
    t_sol.trace_add("write", lambda *args, identifier="t_sol": app.update_widgets(identifier))

    global stoney_filament
    stoney_filament = tkinter.StringVar(value="")
    stoney_filament.trace_add("write", lambda *args, identifier="stoney_filament_updated": app.update_widgets(identifier))
