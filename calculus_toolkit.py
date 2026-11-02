import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sympy as sp
import numpy as np

class CalculusApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Calculus Toolkit")
        self.geometry("900x700")
        self.minsize(800, 600)
        
        # Configure layout / styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Main Layout split into Navigation (Left) and Workspace (Right)
        self.paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True)
        
        # Left Navigation Panel
        self.nav_frame = ttk.Frame(self.paned, width=220, padding=10)
        self.paned.add(self.nav_frame, weight=1)
        
        # Right Workspace Panel
        self.work_frame = ttk.Frame(self.paned, padding=15)
        self.paned.add(self.work_frame, weight=4)
        
        self.build_navigation()
        self.show_welcome_screen()

    def build_navigation(self):
        lbl_menu = ttk.Label(self.nav_frame, text="MODULE MENU", font=("Arial", 12, "bold"))
        lbl_menu.pack(anchor=tk.W, pady=(0, 15))
        
        # Differentiation Section
        lbl_diff = ttk.Label(self.nav_frame, text="1. Differentiation", font=("Arial", 10, "bold"), foreground="#2b579a")
        lbl_diff.pack(anchor=tk.W, pady=(10, 2))
        ttk.Button(self.nav_frame, text="Single Variable Symbolic", command=lambda: self.load_module("diff_single_sym")).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(self.nav_frame, text="Single Variable Numerical", command=lambda: self.load_module("diff_single_num")).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(self.nav_frame, text="Multi Variable Symbolic", command=lambda: self.load_module("diff_multi_sym")).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(self.nav_frame, text="Multi Variable Numerical", command=lambda: self.load_module("diff_multi_num")).pack(fill=tk.X, padx=5, pady=2)
        
        # Integration Section
        lbl_int = ttk.Label(self.nav_frame, text="2. Integration", font=("Arial", 10, "bold"), foreground="#00a300")
        lbl_int.pack(anchor=tk.W, pady=(15, 2))
        ttk.Button(self.nav_frame, text="Single Variable Symbolic", command=lambda: self.load_module("int_single_sym")).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(self.nav_frame, text="Single Variable Numerical", command=lambda: self.load_module("int_single_num")).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(self.nav_frame, text="Multi Variable Symbolic", command=lambda: self.load_module("int_multi_sym")).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(self.nav_frame, text="Multi Variable Numerical", command=lambda: self.load_module("int_multi_num")).pack(fill=tk.X, padx=5, pady=2)
        
        # Differential Equations Section
        lbl_de = ttk.Label(self.nav_frame, text="3. Differential Equations", font=("Arial", 10, "bold"), foreground="#b91d47")
        lbl_de.pack(anchor=tk.W, pady=(15, 2))
        ttk.Button(self.nav_frame, text="ODE General Solution", command=lambda: self.load_module("ode_gen")).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(self.nav_frame, text="ODE Particular Solution", command=lambda: self.load_module("ode_part")).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(self.nav_frame, text="PDE General Solution", command=lambda: self.load_module("pde_gen")).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(self.nav_frame, text="PDE Particular Solution", command=lambda: self.load_module("pde_part")).pack(fill=tk.X, padx=5, pady=2)
        
        # Exit App
        ttk.Separator(self.nav_frame, orient='horizontal').pack(fill=tk.X, pady=20)
        ttk.Button(self.nav_frame, text="Exit Toolkit", command=self.quit).pack(fill=tk.X, padx=5)

    def clear_workspace(self):
        for widget in self.work_frame.winfo_children():
            widget.destroy()

    def show_welcome_screen(self):
        self.clear_workspace()
        welcome_lbl = ttk.Label(self.work_frame, text="Welcome to the SymPy/NumPy Calculus Toolkit", font=("Arial", 16, "bold"))
        welcome_lbl.pack(pady=40)
        
        desc_text = ("Select an operation from the sidebar navigation menu to get started.\n\n"
                     "This application supports highly complex algebraic symbolic calculations, "
                     "exact multi-variable numeric solutions, and Differential Equation solvers.")
        desc_lbl = ttk.Label(self.work_frame, text=desc_text, font=("Arial", 11), justify=tk.CENTER, wraplength=500)
        desc_lbl.pack(pady=10)

    def load_module(self, target):
        self.clear_workspace()
        
        titles = {
            "diff_single_sym": "Single-Variable Symbolic Differentiation",
            "diff_single_num": "Single-Variable Numerical Differentiation",
            "diff_multi_sym": "Multi-Variable Symbolic Mixed Partial Differentiation",
            "diff_multi_num": "Multi-Variable Numerical Mixed Partial Differentiation",
            "int_single_sym": "Single-Variable Symbolic Integration",
            "int_single_num": "Single-Variable Numerical Integration",
            "int_multi_sym": "Multi-Variable Symbolic Integration",
            "int_multi_num": "Multi-Variable Numerical Integration",
            "ode_gen": "Ordinary Differential Equation (ODE) General Solution",
            "ode_part": "Ordinary Differential Equation (ODE) Particular Solution",
            "pde_gen": "Partial Differential Equation (PDE) General Solution",
            "pde_part": "Partial Differential Equation (PDE) Particular Solution"
        }
        
        header = ttk.Label(self.work_frame, text=titles.get(target, "Toolkit Module"), font=("Arial", 14, "bold"))
        header.pack(anchor=tk.W, pady=(0, 15))
        
        # Dynamic container for inputs
        input_box = ttk.LabelFrame(self.work_frame, text="Input Configurations", padding=15)
        input_box.pack(fill=tk.X, pady=5)
        
        entries = {}
        
        def add_field(label_text, key):
            row_frame = ttk.Frame(input_box)
            row_frame.pack(fill=tk.X, pady=4)
            lbl = ttk.Label(row_frame, text=label_text, width=45, anchor=tk.W)
            lbl.pack(side=tk.LEFT)
            ent = ttk.Entry(row_frame)
            ent.pack(side=tk.LEFT, fill=tk.X, expand=True)
            entries[key] = ent

        # Configure fields dynamically based on modules with integrated examples
        if target == "diff_single_sym" or target == "diff_single_num":
            add_field("Enter the variable (e.g., x):", "var")
            add_field("Enter the function (e.g., sin(x)*exp(x)):", "func")
            add_field("Enter the order of differentiation (e.g., 1):", "order")
            if target == "diff_single_num":
                add_field("Enter the evaluation point (e.g., 2.0):", "point")
                
        elif target == "diff_multi_sym" or target == "diff_multi_num":
            add_field("Enter all variables (e.g., x y):", "vars")
            add_field("Enter the function (e.g., x**2*y + sin(y)):", "func")
            add_field("Enter differentiation sequence (e.g., x y):", "seq")
            add_field("Enter orders for sequence (e.g., 1 1):", "orders")
            if target == "diff_multi_num":
                add_field("Enter values for ALL vars in order (e.g., 2.0 1.5):", "points")
                
        elif target == "int_single_sym" or target == "int_single_num":
            add_field("Enter the variable of integration (e.g., x):", "var")
            add_field("Enter the function (e.g., sin(x)):", "func")
            if target == "int_single_num":
                add_field("Enter the lower bound (e.g., 0):", "lower")
                add_field("Enter the upper bound (e.g., 3.14159):", "upper")
                
        elif target == "int_multi_sym" or target == "int_multi_num":
            add_field("Enter all variables (e.g., x y):", "vars")
            add_field("Enter the function (e.g., x*y):", "func")
            add_field("Enter integration sequence (e.g., x y):", "seq")
            if target == "int_multi_num":
                add_field("Enter lower bounds for sequence (e.g., 0 0):", "lowers")
                add_field("Enter upper bounds for sequence (e.g., 1 2):", "uppers")
                
        elif target in ["ode_gen", "ode_part"]:
            add_field("Enter the independent variable (e.g., x):", "var")
            add_field("Enter dependent function name (e.g., y):", "func")
            add_field("Enter maximum order of ODE (e.g., 2):", "order")
            add_field("Enter equation expression (= 0 implicitly) (e.g., y(x).diff(x,2) + y(x)):", "eq")
            if target == "ode_part":
                add_field("Enter conditions (e.g., y(0)=1, y(x).diff(x).subs(x,0)=0):", "ics")
                
        elif target in ["pde_gen", "pde_part"]:
            add_field("Enter independent variables (e.g., x t):", "vars")
            add_field("Enter dependent function name (e.g., u):", "func")
            add_field("Enter maximum order of PDE (e.g., 2):", "order")
            add_field("Enter equation expression (= 0 implicitly) (e.g., u(x,t).diff(t) - u(x,t).diff(x,2)):", "eq")
            if target == "pde_part":
                add_field("Enter boundary conditions separated by commas (e.g., u(x,0)=sin(x)):", "ics")

        # Result display window
        result_box = ttk.LabelFrame(self.work_frame, text="Calculation Results Output", padding=10)
        result_box.pack(fill=tk.BOTH, expand=True, pady=10)
        
        output_area = scrolledtext.ScrolledText(result_box, wrap=tk.WORD, height=10, font=("Consolas", 11))
        output_area.pack(fill=tk.BOTH, expand=True)
        
        # Action execution button
        btn_calc = ttk.Button(self.work_frame, text="Execute System Calculation", 
                              command=lambda: self.run_calculation(target, entries, output_area))
        btn_calc.pack(anchor=tk.E, pady=5)

    def run_calculation(self, target, entries, output_area):
        output_area.delete('1.0', tk.END)
        try:
            if target == "diff_single_sym":
                v = entries["var"].get().strip()
                f = entries["func"].get().strip()
                o = int(entries["order"].get().strip())
                
                s_dict = {v: sp.Symbol(v)}
                local_env = {**sp.__dict__, **s_dict}
                parsed = sp.parse_expr(f, local_dict=local_env)
                res = sp.diff(parsed, s_dict[v], o)
                output_area.insert(tk.END, f"Function: {parsed}\n\nDerivative (Order {o}):\n{res}")
                
            elif target == "diff_single_num":
                v = entries["var"].get().strip()
                f = entries["func"].get().strip()
                o = int(entries["order"].get().strip())
                pt = float(entries["point"].get().strip())
                
                s_dict = {v: sp.Symbol(v)}
                local_env = {**sp.__dict__, **s_dict}
                parsed = sp.parse_expr(f, local_dict=local_env)
                formula = sp.diff(parsed, s_dict[v], o)
                res = float(formula.subs(s_dict[v], pt).evalf())
                output_area.insert(tk.END, f"Evaluated at {v} = {pt}\n\nNumerical Result:\n{res}")
                
            elif target == "diff_multi_sym":
                v_list = entries["vars"].get().strip().split()
                f = entries["func"].get().strip()
                seq = entries["seq"].get().strip().split()
                orders = entries["orders"].get().strip().split()
                
                s_dict = {var: sp.Symbol(var) for var in v_list}
                local_env = {**sp.__dict__, **s_dict}
                parsed = sp.parse_expr(f, local_dict=local_env)
                
                res = parsed
                for i in range(len(seq)):
                    res = sp.diff(res, s_dict[seq[i]], int(orders[i]))
                output_area.insert(tk.END, f"Function: {parsed}\n\nPartial Derivative with respect to {seq}:\n{res}")
                
            elif target == "diff_multi_num":
                v_list = entries["vars"].get().strip().split()
                f = entries["func"].get().strip()
                seq = entries["seq"].get().strip().split()
                orders = entries["orders"].get().strip().split()
                pts = entries["points"].get().strip().split()
                
                s_dict = {var: sp.Symbol(var) for var in v_list}
                local_env = {**sp.__dict__, **s_dict}
                parsed = sp.parse_expr(f, local_dict=local_env)
                
                formula = parsed
                for i in range(len(seq)):
                    formula = sp.diff(formula, s_dict[seq[i]], int(orders[i]))
                
                pt_map = {s_dict[v_list[i]]: float(pts[i]) for i in range(len(v_list))}
                res = float(formula.subs(pt_map).evalf())
                output_area.insert(tk.END, f"Evaluation Coordinates: {pt_map}\n\nNumerical Partial Result:\n{res}")

            elif target == "int_single_sym":
                v = entries["var"].get().strip()
                f = entries["func"].get().strip()
                
                s_dict = {v: sp.Symbol(v)}
                local_env = {**sp.__dict__, **s_dict}
                parsed = sp.parse_expr(f, local_dict=local_env)
                res = sp.integrate(parsed, s_dict[v])
                output_area.insert(tk.END, f"Indefinite Integral Formula:\n{res} + C")
                
            elif target == "int_single_num":
                v = entries["var"].get().strip()
                f = entries["func"].get().strip()
                low = float(entries["lower"].get().strip())
                upp = float(entries["upper"].get().strip())
                
                s_dict = {v: sp.Symbol(v)}
                local_env = {**sp.__dict__, **s_dict}
                parsed = sp.parse_expr(f, local_dict=local_env)
                expr = sp.integrate(parsed, (s_dict[v], low, upp))
                res = float(expr.evalf())
                output_area.insert(tk.END, f"Definite Integral Bounds: [{low}, {upp}]\n\nNumerical Evaluation Result:\n{res}")
                
            elif target == "int_multi_sym":
                v_list = entries["vars"].get().strip().split()
                f = entries["func"].get().strip()
                seq = entries["seq"].get().strip().split()
                
                s_dict = {var: sp.Symbol(var) for var in v_list}
                local_env = {**sp.__dict__, **s_dict}
                parsed = sp.parse_expr(f, local_dict=local_env)
                
                res = parsed
                for var in seq:
                    res = sp.integrate(res, s_dict[var])
                output_area.insert(tk.END, f"Multiple Indefinite Integration Matrix:\n{res}")
                
            elif target == "int_multi_num":
                v_list = entries["vars"].get().strip().split()
                f = entries["func"].get().strip()
                seq = entries["seq"].get().strip().split()
                lowers = entries["lowers"].get().strip().split()
                uppers = entries["uppers"].get().strip().split()
                
                s_dict = {var: sp.Symbol(var) for var in v_list}
                local_env = {**sp.__dict__, **s_dict}
                parsed = sp.parse_expr(f, local_dict=local_env)
                
                expr = parsed
                for i in range(len(seq)):
                    expr = sp.integrate(expr, (s_dict[seq[i]], float(lowers[i]), float(uppers[i])))
                res = float(expr.evalf())
                output_area.insert(tk.END, f"Evaluated Definite Multiple Numerical Bound Value:\n{res}")

            elif target == "ode_gen":
                v = entries["var"].get().strip()
                f = entries["func"].get().strip()
                eq_str = entries["eq"].get().strip()
                
                ind_symbol = sp.Symbol(v)
                dep_func = sp.Function(f)
                dep_symbol = dep_func(ind_symbol)
                
                local_env = {**sp.__dict__, v: ind_symbol, f: dep_func}
                parsed = sp.parse_expr(eq_str, local_dict=local_env)
                res = sp.dsolve(parsed, dep_symbol)
                output_area.insert(tk.END, f"ODE General Analytical Equation Solution:\n\n{res}")
                
            elif target == "ode_part":
                v = entries["var"].get().strip()
                f = entries["func"].get().strip()
                eq_str = entries["eq"].get().strip()
                ics_str = entries["ics"].get().strip()
                
                ind_symbol = sp.Symbol(v)
                dep_func = sp.Function(f)
                dep_symbol = dep_func(ind_symbol)
                
                local_env = {**sp.__dict__, v: ind_symbol, f: dep_func}
                parsed = sp.parse_expr(eq_str, local_dict=local_env)
                
                ics_dict = {}
                for cond in ics_str.split(','):
                    if '=' in cond:
                        l_str, r_str = cond.split('=', 1)
                        l_parsed = sp.parse_expr(l_str.strip(), local_dict=local_env)
                        r_parsed = sp.parse_expr(r_str.strip(), local_dict=local_env)
                        ics_dict[l_parsed] = r_parsed
                        
                res = sp.dsolve(parsed, dep_symbol, ics=ics_dict)
                output_area.insert(tk.END, f"Particular Initial/Boundary Condition Solution:\n\n{res}")
                
            elif target == "pde_gen":
                v_list = entries["vars"].get().strip().split()
                f = entries["func"].get().strip()
                eq_str = entries["eq"].get().strip()
                
                s_dict = {var: sp.Symbol(var) for var in v_list}
                v_tuple = tuple(s_dict[var] for var in v_list)
                dep_func = sp.Function(f)
                dep_symbol = dep_func(*v_tuple)
                
                local_env = {**sp.__dict__, **s_dict, f: dep_func}
                parsed = sp.parse_expr(eq_str, local_dict=local_env)
                
                try:
                    res = sp.pdsolve(parsed, dep_symbol)
                    output_area.insert(tk.END, f"[Exact PDE Symbolic Formula Solution]:\n\n{res}")
                except Exception:
                    if len(v_list) == 2:
                        var1, var2 = v_list[0], v_list[1]
                        X = sp.Function(f'X_{var1}')(s_dict[var1])
                        T = sp.Function(f'X_{var2}')(s_dict[var2])
                        subbed = parsed.subs(dep_symbol, X * T).doit()
                        divided = sp.simplify(subbed / (X * T))
                        t_side, x_side = divided.as_independent(X)
                        lam = sp.Symbol('lambda')
                        sol_x = sp.dsolve(sp.simplify((x_side + lam) * X), X)
                        sol_t = sp.dsolve(sp.simplify((t_side - lam) * T), T)
                        output_area.insert(tk.END, f"[Separated Analytical Variable Solution Formula]:\n\n"
                                                      f"{f}({var1}, {var2}) = ({sol_x.rhs}) * ({sol_t.rhs})")
                    else:
                        output_area.insert(tk.END, "SymPy pdsolve could not determine exact form. Variable separation matches 2D vectors.")

            elif target == "pde_part":
                v_list = entries["vars"].get().strip().split()
                f = entries["func"].get().strip()
                eq_str = entries["eq"].get().strip()
                ics_str = entries["ics"].get().strip()
                
                s_dict = {var: sp.Symbol(var) for var in v_list}
                v_tuple = tuple(s_dict[var] for var in v_list)
                dep_func = sp.Function(f)
                dep_symbol = dep_func(*v_tuple)
                
                local_env = {**sp.__dict__, **s_dict, f: dep_func}
                parsed = sp.parse_expr(eq_str, local_dict=local_env)
                
                bcs = {}
                for cond in ics_str.split(';'):
                    if '=' in cond:
                        l_str, r_str = cond.split('=', 1)
                        bcs[sp.parse_expr(l_str.strip(), local_dict=local_env)] = sp.parse_expr(r_str.strip(), local_dict=local_env)
                
                try:
                    res = sp.pdsolve(parsed, dep_symbol, ics=bcs)
                    output_area.insert(tk.END, f"[Exact Particular Boundary Solution]:\n\n{res}")
                except Exception:
                    output_area.insert(tk.END, f"[Symbolic Boundary Solver Limited] Displaying system configurations:\n\nPDE Expression: {parsed} = 0\nBoundary Sets: {bcs}")

        except Exception as err:
            messagebox.showerror("Execution Error", f"Failed parsing calculation inputs.\n\nDetails: {err}")
            output_area.insert(tk.END, f"SYSTEM FAULT LOG:\n{err}")

if __name__ == "__main__":
    app = CalculusApp()
    app.mainloop()
