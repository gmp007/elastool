import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from view_file import InputFileViewer
import sys
import os
from write_default_input import display_help,write_default_input

class FileHandler:
    def __init__(self, tmp_path):
        self.tmp_path = tmp_path

    def save_path(self, pp_path_entry):
        base_path = self.tmp_path
        try:
            with open(os.path.join(base_path, "pp_path.txt"), "w") as file:
                file.write(pp_path_entry.get() + "\n")
        except FileNotFoundError:
            pass

    def load_config(self, pp_path_entry):
        base_path = self.tmp_path
        try:
            with open(os.path.join(base_path, "pp_path.txt"), "r") as file:
                lines = file.readlines()
                if len(lines) >= 1:
                    pp_path_entry.insert(0, lines[0].strip())
        except FileNotFoundError:
            pass
            
            
class UFCFileGenerator:
    def __init__(self, tab, file_handler):
        self.file_handler = file_handler
        self.run_mode_options = ["0-generating key", "1-Automatic", "2-Pre-processing", "3-Post-processing"]
        self.system_mode_options = ["1D", "2D", "3D"]
        self.cell_mode_options = ["primitive cell", "conventional cell"]
        self.stress_method_options = ["static", "dynamic"]
        self.strains_matrix_options = ["ohess", "asess", "ulics"]
        self.plot_options = ["no", "yes"]
        self.eplot_options = ["None", "print", "POISSON", "SHEAR", "LC", "YOUNG", "PUGH_RATIO", "BULK", "RATIO_COMPRESSIONAL_SHEAR", "DEBYE_SPEED", "all"]

        self.create_canvas(tab)
        self.create_form()
        self.load_config()
        self.add_strains()
        self.lock_unlock_entries()

    def load_config(self):
        self.file_handler.load_config(self.pp_path_entry)

    def create_canvas(self, tab):
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas = tk.Canvas(tab)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor=tk.NW)

        v_scrollbar = tk.Scrollbar(tab, orient=tk.VERTICAL, command=canvas.yview, bg='black')
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.config(yscrollcommand=v_scrollbar.set)

        h_scrollbar = tk.Scrollbar(tab, orient=tk.HORIZONTAL, command=canvas.xview, bg='black')
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        canvas.config(xscrollcommand=h_scrollbar.set)

        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * int(event.delta / 120), "units"))
        canvas.bind_all("<Shift-MouseWheel>", lambda event: canvas.xview_scroll(-1 * int(event.delta / 120), "units"))

        frame.bind("<Configure>", configure_scroll_region)
        self.frame = frame

    def create_form(self):
        self.create_button_frame()
        self.create_form_fields()
        self.create_additional_fields()

    def create_button_frameold(self):
        button_frame = tk.Frame(self.frame)
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        tk.Button(button_frame, bg='cyan', text="Generate elastool.in", command=self.generate_elastoolin_file).grid(row=0, column=0, padx=5, pady=1, sticky="w")
        tk.Button(button_frame, bg='#ffff99', text="View/Edit elastool.in", command=self.open_sample_file).grid(row=0, column=3, padx=5, pady=1, sticky="w")
        tk.Button(button_frame, text="Generate KPOINTS and INCARs", command=self.generate_kpoints_incar).grid(row=0, column=6, padx=5, pady=1, sticky="w")
        tk.Button(button_frame, text="help", command=lambda kw="ufc_file": display_help(keyword=kw,use_tk=True)).grid(row=0, column=5, padx=5, pady=25, sticky="w")
        
    def create_button_frame(self):
        button_frame = tk.Frame(self.frame)
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        tk.Button(button_frame, bg='cyan', text="Generate elastool.in", command=self.generate_elastoolin_file).grid(row=0, column=0, padx=5, pady=1, sticky="w")
        tk.Button(button_frame, bg='#ffff99', text="View/Edit elastool.in", command=self.open_sample_file).grid(row=0, column=1, padx=5, pady=1, sticky="w")
        tk.Button(button_frame, text="Generate KPOINTS and INCARs", command=self.generate_kpoints_incar).grid(row=0, column=2, padx=5, pady=1, sticky="w")
        tk.Button(button_frame, text="RUN ELasTool", command=self.run_calculation).grid(row=0, column=3, padx=5, pady=1, sticky="w")
        tk.Button(button_frame, text="help", command=lambda kw="ufc_file": display_help(keyword=kw,use_tk=True)).grid(row=0, column=4, padx=5, pady=1, sticky="w")
        tk.Button(button_frame, text="Exit", command=self.exit_application).grid(row=0, column=5, padx=5, pady=1, sticky="w")
        

    def run_calculation(self):
        #self.generate_elastoolin_file()
        #self.generate_kpoints_incar()
        os.system("elastool")
        messagebox.showinfo("Success", "Calculation started.")
        sys.exit(0)



    def exit_application(self):
        print("======================================================")
        print("= ElasTool input files successfully written to file  =")
        print("=  Modify if necessary and proceed with runs Exiting =")
        print("=          Happy simulations Exiting ...             =")
        print("======================================================")
        self.frame.quit()
        self.frame.update()
        self.frame.destroy()



    def create_form_fields(self):
        self.mode = tk.LabelFrame(self.frame, text="ELASTOOL COMPUTATIONAL TOOLKIT: ", font=("Helvetica", 14, "bold"))
        self.mode.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=(3, 3))

        self.create_dropdown("run_mode", "Please choose run mode:", self.run_mode_options, 0)
        self.create_dropdown("system_mode", "Define the dimensional of the system:", self.system_mode_options, 1)
        self.create_file_entry("crystal_filename", "Enter the crystal structure file:", 2, "Browse", self.browse_crystal_file)
        #self.create_dropdown("cell_mode", "Used cell:", self.cell_mode_options, 3)
        self.create_dropdown("cell_mode", "Used cell:", self.cell_mode_options, 3, self.update_cell_mode)
        self.create_dropdown("stress_method", "Method_stress_statistics:", self.stress_method_options, 4)
        self.create_dropdown("strains_matrix", "Strain matrix method:", self.strains_matrix_options, 5)

    def create_additional_fields(self):
        row = 6
        self.strains_num_label = tk.Label(self.mode, text="Number of strains").grid(row=row, column=0, sticky='w', pady=1)
        self.strains_num_entry = tk.Entry(self.mode, width=10, bg='white')
        self.strains_num_entry.grid(row=row, column=1, sticky='w', pady=1)
        self.strains_num_entry.insert(0, 5)
        self.add_strains_button = tk.Button(self.mode, text="Add strains", command=self.add_strains)
        self.add_strains_button.grid(row=row, column=2, sticky='w', pady=1)

        row += 1
        self.strains_list_frame = tk.Frame(self.mode)
        self.strains_list_frame.grid(row=row, column=1, columnspan=9, sticky='w', pady=1)

        row += 1
        self.create_repeat_numbers(row)

        row += 2
        self.create_pp_path_field(row)

        row += 2
        self.create_plot_parameters(row)

        row += 2
        self.create_parallel_command_field(row)

        # Add initialization for last_number_entry
        row += 1
        last_step_label = tk.Label(self.mode, text="MD steps for averaging stresses in dynamic method").grid(row=row, column=0, sticky='w', pady=1)
        #row += 1
        self.last_number_entry = tk.Entry(self.mode, width=10, bg='white')
        self.last_number_entry.grid(row=row, column=1, sticky='w', pady=1)
        self.last_number_entry.insert(0, "500")

        # Add this part to ensure eplot_var is initialized
        row += 2
        eplot_label = tk.Label(self.mode, text="Parameters to plot (expensive). Choices are: none, print ...").grid(row=row, column=0, sticky='w', pady=1)
        self.eplot_var = tk.StringVar()
        self.eplot_var.set(self.eplot_options[0])
        self.eplot_menu = tk.OptionMenu(self.mode, self.eplot_var, *self.eplot_options, command=self.lock_unlock_entries)
        self.eplot_menu.config(width=25)
        self.eplot_menu.grid(row=row, column=1, columnspan=9, sticky='w', pady=1)

        
    def create_dropdown(self, var_name, label_text, options, row, command=None):
        label = tk.Label(self.mode, text=label_text).grid(row=row, column=0, sticky='w', pady=1)
        var = tk.StringVar()
        var.set(options[0])
        menu = tk.OptionMenu(self.mode, var, *options, command=command)
        menu.config(width=15)
        menu.grid(row=row, column=1, columnspan=9, sticky='w', pady=1)
        setattr(self, var_name + "_var", var)
        setattr(self, var_name + "_menu", menu)


    def create_file_entry(self, var_name, label_text, row, button_text, button_command):
        label = tk.Label(self.mode, text=label_text).grid(row=row, column=0, sticky='w', pady=1)
        entry = tk.Entry(self.mode, width=55, bg='white')
        entry.grid(row=row, column=1, columnspan=9, sticky='w', pady=1)
        button = tk.Button(self.mode, text=button_text, command=button_command)
        button.grid(row=row, column=10, padx=5, pady=10, sticky="e")
        setattr(self, var_name + "_entry", entry)
        setattr(self, var_name + "_button", button)

    def create_repeat_numbers(self, row):
        self.vector_entries = []
        lbl = tk.Label(self.mode, text="Supercell size (only for dynamic (MD) method): ")
        lbl.grid(row=row, column=0, sticky='w', pady=1)
        for i in range(3):
            entry = tk.Entry(self.mode, width=10, bg='white')
            entry.grid(row=row, column=i + 1, sticky='w', padx=5, pady=1)
            entry.insert(0, "1")
            self.vector_entries.append(entry)

    def create_pp_path_field(self, row):
        path_pp_label = tk.Label(self.mode, text="Pseudopotential path for vasp:").grid(row=row, column=0, sticky='w', pady=1)
        self.pp_path_entry = tk.Entry(self.mode, width=55, bg='white')
        self.pp_path_entry.grid(row=row, column=1, columnspan=9, sticky='w', pady=1)
        self.browse_pp_button = tk.Button(self.mode, text="Browse", command=self.browse_pp_path)
        self.browse_pp_button.grid(row=row, column=10, padx=5, pady=10, sticky="e")

    def create_plot_parameters(self, row):
        plot_label = tk.Label(self.mode, text="Plot choice (local/web):").grid(row=row, column=0, sticky='w', pady=1)
        self.plot1_var = tk.StringVar()
        self.plot1_var.set(self.plot_options[0])
        self.plot1_menu = tk.OptionMenu(self.mode, self.plot1_var, *self.plot_options, command=self.lock_unlock_entries)
        self.plot1_menu.config(width=5)
        self.plot1_menu.grid(row=row, column=1, sticky='w', pady=1)

        self.plot2_var = tk.StringVar()
        self.plot2_var.set(self.plot_options[0])
        self.plot2_menu = tk.OptionMenu(self.mode, self.plot2_var, *self.plot_options, command=self.lock_unlock_entries)
        self.plot2_menu.config(width=5)
        self.plot2_menu.grid(row=row, column=2, sticky='e', pady=1)

    def create_parallel_command_field(self, row):
        self.command_label = tk.Label(self.mode, text="Job submission command:").grid(row=row, column=0, sticky='w', pady=1)
        self.command_entry = tk.Entry(self.mode, width=30, bg='white')
        self.command_entry.grid(row=row, column=1, columnspan=9, sticky='we', pady=1, padx=5)
        self.command_entry.insert(0, "mpirun -n 4 vasp_std > vasp.log")

    def browse_crystal_file(self):
        filepath = filedialog.askopenfilename(title="Select crystal structure, vasp or cif format")
        if filepath:
            self.crystal_filename_entry.delete(0, tk.END)
            self.crystal_filename_entry.insert(0, filepath)

    def browse_pp_path(self):
        filepath = filedialog.askdirectory(title="Pseudopotential directory - location of POTCAR files for VASP")
        if filepath:
            self.pp_path_entry.delete(0, tk.END)
            self.pp_path_entry.insert(0, filepath)

    def open_sample_file(self):
        InputFileViewer("elastool.in")

    def lock_unlock_entries(self, *args):
        pass

    def add_strains(self):
        for widget in self.strains_list_frame.winfo_children():
            widget.destroy()

        try:
            num_stress = int(self.strains_num_entry.get())
            if num_stress % 2 == 0:
                num_stress += 1
            elif num_stress == 1:
                num_stress += 1
            self.num_stressed = num_stress
        except ValueError:
            messagebox.showerror("Error", "Please enter integer number.")
            return

        self.strains_list_entries = []
        strnmax = 0.06
        strnmin = -0.06
        step = (strnmax - strnmin) / (num_stress - 1)
        stress = strnmin - step
        col = 0
        row = 0
        for i in range(num_stress):
            col += 1
            stress = round(stress + step, 3)
            strn = 0.0 if stress == 0.0 else stress
            entry = tk.Entry(self.strains_list_frame, width=10, bg='white')
            entry.grid(row=row, column=col, sticky='w', padx=3, pady=1)
            entry.insert(0, strn)
            self.strains_list_entries.append(entry)
            if col == 5:
                row += 1
                col = 0

    def generate_elastoolin_file(self):
        filename = "elastool.in"
        self.list_keys = self.collect_form_data()
        with open(filename, 'w') as f:
            self.write_elastoolin_file(f)
        messagebox.showinfo("Success", f"{filename} has been generated.")
        self.file_handler.save_path(self.pp_path_entry)

    def collect_form_data(self):
        list_keys = {
            "run_mode": self.run_mode_options.index(self.run_mode_var.get()),
            "dimensional": self.system_mode_var.get(),
            "structure_file": self.crystal_filename_entry.get(),
            "if_conventional_cell": self.cell_mode_var.get(),
            "method_stress_statistics": self.stress_method_var.get(),
            "strains_matrix": self.strains_matrix_var.get(),
            "strains_list": ' '.join(map(str, [entry.get() for entry in self.strains_list_entries])),
            "repeat_num": ' '.join(map(str, [entry.get() for entry in self.vector_entries])),
            "num_last_samples": self.last_number_entry.get(),
            "potential_dir": self.pp_path_entry.get(),
            "plotparameters": f"{self.plot1_var.get()},{self.plot2_var.get()}",
            "elateparameters": self.eplot_var.get(),
            "parallel_submit_command": self.command_entry.get()
        }
        return list_keys

    def write_elastoolin_file(self, file):
        print("###############################################################################", file=file)
        print("### The input file to control the calculation details of elastic constants  ###", file=file)
        print("###############################################################################\n", file=file)
        
        print("# run mode: 0 for generating key default input files, 1 for automatic run, 2 for pre-processing, 3 for post-processing", file=file)
        print("# if 2, plz ensure the structure opt. is performed at fixed pressure or volume", file=file)
        print("# i.e. CONTCAR and OUTCAR files both exist in ./OPT directory.", file=file)
        print("# Additionally, you can visualize elastic parameters directly using Elate by running \"elastool -elate\" after strain-stress calculations", file=file)
        print(f"run_mode = {self.list_keys['run_mode']}\n", file=file)
        
        print("# Define the dimensional of the system: 1D/2D/3D.", file=file)
        print(f"dimensional = {self.list_keys['dimensional']}\n", file=file)
        
        print("# the crystal structure file in vasp POSCAR (.vasp) or cif (.cif) format", file=file)
        print(f"structure_file = {self.list_keys['structure_file']}\n", file=file)
        
        print("# if use conventional cell, no for primitive cell, yes for conventional cell", file=file)
        print(f"if_conventional_cell = {self.list_keys['if_conventional_cell']}\n", file=file)
        
        print("# static or dynamic, static for 0 K, dynamic for finite-temperature", file=file)
        print(f"method_stress_statistics = {self.list_keys['method_stress_statistics']}\n", file=file)
        
        print("# strains matrix for solve all elastic constants, asess or ohess or ulics", file=file)
        print(f"strains_matrix = {self.list_keys['strains_matrix']}\n", file=file)
        
        print("# strains list for deforming lattice cell, 0 will be neglected because of", file=file)
        print("# the initial optimization, if method_statistics = dynamic, the first one is used", file=file)
        print(f"strains_list = {self.list_keys['strains_list']}\n", file=file)
        
        print("# repeat numbers of three lattice vectors in conventional lattice for making", file=file)
        print("# supercell of molecular dynamics simulations (method_statistics = dynamic)", file=file)
        print(f"repeat_num = {self.list_keys['repeat_num']}\n", file=file)
        
        print("# last number of steps for sampling stresses used in the dynamic method", file=file)
        print(f"num_last_samples = {self.list_keys['num_last_samples']}\n", file=file)
        
        print("# Potential directory - specify the location of your POTCAR files", file=file)
        print(f"potential_dir = {self.list_keys['potential_dir']}\n", file=file)
        
        print("# Plot parameters EVGB for 2D. Second argument turns on interactive plotly. Do not turn on for high-throughput calculations", file=file)
        print(f"plotparameters = {self.list_keys['plotparameters']}\n", file=file)
        
        print("# Choose Elate parameters to plot. Alternatively, after obtaining your elastic tensor, run \"elastool -elate to view on the web browser", file=file)
        print("# None, print (just data), POISSON, SHEAR, LC, YOUNG, PUGH_RATIO, BULK,RATIO_COMPRESSIONAL_SHEAR,DEBYE_SPEED. You can use \"all\" for 2D only", file=file)
        print(f"elateparameters = {self.list_keys['elateparameters']}\n", file=file)
        
        print("# The parallel submitting commmd", file=file)
        print(f"parallel_submit_command = {self.list_keys['parallel_submit_command']}\n", file=file)

    def generate_kpoints_incar(self):
        cwd = os.getcwd()
        method_stress_statistics = self.stress_method_var.get()
        write_default_input(method_stress_statistics, cwd)
        messagebox.showinfo("Success", "KPOINTS and INCAR files have been generated.")
        
    def update_cell_mode(self, *args):
        if self.cell_mode_var.get() == "primitive cell":
            self.cell_mode_var.set("no")
        else:
            self.cell_mode_var.set("yes")
  
def elastoolguicall():
    root = tk.Tk()
    root.title("ElasTool Computational Toolkit Input Generator")
    
    root.geometry("900x700")

    tabControl = ttk.Notebook(root)
    tab1 = ttk.Frame(tabControl)
    tabControl.add(tab1, text='Generate ElasTool Input')
    tabControl.pack(expand=1, fill="both")

    home_dir = os.path.expanduser("~")
    elastools_dir = os.path.join(home_dir, "elastools_dir" if sys.platform == "win32" else ".elastools_dir")
    if not os.path.exists(elastools_dir):
        os.makedirs(elastools_dir)

    file_handler = FileHandler(elastools_dir)
    UFCFileGenerator(tab1, file_handler)

    root.mainloop()


if __name__ == "__main__":
    elastoolguicall()

