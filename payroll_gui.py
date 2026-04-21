import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, timedelta
import calendar
import os

class DateEntry:
    def __init__(self, parent, label_text, callback=None):
        self.parent = parent
        self.callback = callback
        self.frame = ttk.Frame(parent)
        ttk.Label(self.frame, text=label_text, width=15).pack(side="left")

        self.date_var = tk.StringVar(value=datetime.now().strftime("%m-%d-%Y"))
        self.date_btn = ttk.Button(self.frame, textvariable=self.date_var, command=self.open_calendar)
        self.date_btn.pack(side="left", padx=5)

        self.now = datetime.now()
        self.curr_month = self.now.month
        self.curr_year = self.now.year

    def open_calendar(self):
        self.top = tk.Toplevel(self.parent)
        self.top.title("Select Date")
        self.top.geometry("280x300")
        self.top.resizable(False, False)
        self.top.grab_set()
        self.draw_calendar()

    def draw_calendar(self):
        for widget in self.top.winfo_children():
            widget.destroy()

        header = ttk.Frame(self.top)
        header.pack(fill="x", pady=10)
        
        ttk.Button(header, text="<", width=3, command=self.prev_month).pack(side="left", padx=10)
        month_name = calendar.month_name[self.curr_month]
        ttk.Label(header, text=f"{month_name} {self.curr_year}", font=("Arial", 10, "bold")).pack(side="left", expand=True)
        ttk.Button(header, text=">", width=3, command=self.next_month).pack(side="right", padx=10)

        days_frame = ttk.Frame(self.top)
        days_frame.pack(pady=5)
        week_days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        for i, day in enumerate(week_days):
            color = "red" if i >= 5 else "black"
            tk.Label(days_frame, text=day, width=4, fg=color).grid(row=0, column=i)

        month_days = calendar.monthcalendar(self.curr_year, self.curr_month)
        for r, week in enumerate(month_days):
            for c, day in enumerate(week):
                if day != 0:
                    btn_state = "normal"
                    btn_bg = "#ffffff"
                    if c >= 5:
                        btn_state = "disabled"
                        btn_bg = "#e0e0e0"

                    btn = tk.Button(days_frame, text=day, width=3, state=btn_state, bg=btn_bg,
                                    command=lambda d=day: self.select_date(d))
                    btn.grid(row=r+1, column=c, padx=1, pady=1)

    def prev_month(self):
        self.curr_month -= 1
        if self.curr_month < 1:
            self.curr_month = 12
            self.curr_year -= 1
        self.draw_calendar()

    def next_month(self):
        self.curr_month += 1
        if self.curr_month > 12:
            self.curr_month = 1
            self.curr_year += 1
        self.draw_calendar()

    def select_date(self, day):
        selected = datetime(self.curr_year, self.curr_month, day)
        self.date_var.set(selected.strftime("%m-%d-%Y"))
        self.top.destroy()
        if self.callback:
            self.callback()

    def get_date_obj(self):
        return datetime.strptime(self.date_var.get(), "%m-%d-%Y")

    def set_date(self, date_obj):
        self.date_var.set(date_obj.strftime("%m-%d-%Y"))
        self.curr_month = date_obj.month
        self.curr_year = date_obj.year

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)


class Employee:
    def __init__(self):
        self.emp_company = "MAO'S COMPANY"
        self.emp_name = ""
        self.emp_department = ""
        self.emp_designation = ""
        self.date_today = datetime.now().date()
        self.pay_date = ""
        self.working_days = 0
        self.has_sss = False
        self.has_pagibig = False
        self.has_philhealth = False


class Payslip:
    def __init__(self, employee):
        self.employee = employee
        self.salary_perhour = 0.0
        self.allowance = 0.0
        self.commission = 0.0
        self.overtime = 0.0
        self.tardy = 0.0
        self.sss_rate = 0.05
        self.pag_ibig_rate = 0.02
        self.philhealth_rate = 0.025
        self.professional_tax = 250
        self.basic_salary = 0
        self.gross_pay = 0
        self.sss_ded = 0
        self.pag_ibig_ded = 0
        self.philhealth_ded = 0
        self.income_tax = 0
        self.total_deduction = 0
        self.net_pay = 0

    def calculate_salary(self):
        self.basic_salary = self.employee.working_days * self.salary_perhour
        self.gross_pay = self.basic_salary + self.allowance + self.commission + self.overtime

        self.sss_ded = (self.gross_pay * self.sss_rate) if self.employee.has_sss else 0
        self.pag_ibig_ded = min(self.gross_pay * self.pag_ibig_rate, 200) if self.employee.has_pagibig else 0
        self.philhealth_ded = (self.gross_pay * self.philhealth_rate) if self.employee.has_philhealth else 0

        taxable_income = self.gross_pay - (self.sss_ded + self.pag_ibig_ded + self.philhealth_ded)

        if taxable_income <= 20833:
            self.income_tax = 0
        elif taxable_income <= 33333:
            self.income_tax = (taxable_income - 20833) * 0.15
        elif taxable_income <= 66667:
            self.income_tax = 1875 + (taxable_income - 33333) * 0.20
        else:
            self.income_tax = 8541.80 + (taxable_income - 66667) * 0.25

        self.total_deduction = (self.sss_ded + self.pag_ibig_ded + self.philhealth_ded +
                                self.income_tax + self.professional_tax + self.tardy)
        self.net_pay = self.gross_pay - self.total_deduction

    def get_payslip_text(self):
        text = "=" * 45 + "\n"
        text += "                PAYSLIP\n"
        text += "=" * 45 + "\n"
        text += f"Company Name     : {self.employee.emp_company}\n"
        text += f"Employee Name    : {self.employee.emp_name}\n"
        text += f"Department       : {self.employee.emp_department}\n"
        text += f"Designation      : {self.employee.emp_designation}\n"
        
        contribs = []
        if self.employee.has_sss: contribs.append("SSS")
        if self.employee.has_pagibig: contribs.append("Pag-IBIG")
        if self.employee.has_philhealth: contribs.append("PhilHealth")
        contrib_str = ", ".join(contribs) if contribs else "None"
        
        text += f"Contributions    : {contrib_str}\n"
        text += f"Date             : {self.employee.date_today}\n"
        text += f"Period           : {self.employee.pay_date}\n"
        text += "-" * 45 + "\n"
        text += f"{'EARNINGS':<20} {'AMOUNT':>15}\n"
        text += "-" * 45 + "\n"
        text += f"{'Basic Salary':<20} ₱{self.basic_salary:>10,.2f}\n"
        text += f"{'Allowance':<20} ₱{self.allowance:>10,.2f}\n"
        text += f"{'Commission':<20} ₱{self.commission:>10,.2f}\n"
        text += f"{'Overtime':<20} ₱{self.overtime:>10,.2f}\n"
        text += f"{'Gross Pay':<20} ₱{self.gross_pay:>10,.2f}\n"
        text += "-" * 45 + "\n"
        text += f"{'DEDUCTIONS':<20} {'AMOUNT':>15}\n"
        text += "-" * 45 + "\n"
        text += f"{'SSS':<20} ₱{self.sss_ded:>10,.2f}\n"
        text += f"{'Pag-IBIG':<20} ₱{self.pag_ibig_ded:>10,.2f}\n"
        text += f"{'PhilHealth':<20} ₱{self.philhealth_ded:>10,.2f}\n"
        text += f"{'Income Tax':<20} ₱{self.income_tax:>10,.2f}\n"
        text += f"{'Professional Tax':<20} ₱{self.professional_tax:>10,.2f}\n"
        text += f"{'Tardy':<20} ₱{self.tardy:>10,.2f}\n"
        text += f"{'Total Deduction':<20} ₱{self.total_deduction:>10,.2f}\n"
        text += "-" * 45 + "\n"
        text += f"{'NET PAY':<20} ₱{self.net_pay:>10,.2f}\n"
        text += "=" * 45 + "\n"
        return text


class PayslipGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Payslip Generator")
        self.root.geometry("950x750")
        self.root.configure(bg="#E8F4F8")

        self.dept_mapping = {
            "IT Department": ["Web Developer", "Software Developer", "Database Management"],
            "Human Resources": ["Recruitment Officer"],
            "Accounting": ["Payroll Staff"],
            "Sales": ["Sales Agent"],
            "Engineering": ["Mechanical Engineer", "Materials Engineer"]
        }

        self.employee = Employee()
        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#2B5CBE")
        self.style.configure("TLabel", background="#E8E8F8")
        self.style.configure("TRadiobutton", background="#FFFFFF")
        self.style.configure("TCheckbutton", background="#E8F4F8")
        self.style.configure("TLabelframe", background="#E8F4F8")
        self.style.configure("TNotebook", background="#E8F4F8")
        self.style.configure("TNotebook.Tab", background="#D0E8F0", padding=[10, 5])

    def setup_ui(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.employee_frame = ttk.Frame(notebook)
        notebook.add(self.employee_frame, text="1. Employee Details")
        self.setup_employee_tab()

        self.salary_frame = ttk.Frame(notebook)
        notebook.add(self.salary_frame, text="2. Salary Details")
        self.setup_salary_tab()

        self.results_frame = ttk.Frame(notebook)
        notebook.add(self.results_frame, text="3. Payslip")
        self.setup_results_tab()

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(btn_frame, text="Calculate Payslip", command=self.calculate_payslip).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Print Payslip", command=self.print_payslip).pack(side="left", padx=5) # NEW PRINT BUTTON
        ttk.Button(btn_frame, text="Clear All", command=self.clear_all).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="New Employee", command=self.new_employee).pack(side="right", padx=5)

    def setup_employee_tab(self):
        ttk.Label(self.employee_frame, text="MAO'S COMPANY", font=("Arial", 20, "bold")).pack(pady=5)
        ttk.Separator(self.employee_frame, orient="horizontal").pack(fill="x", pady=10)
        
        ttk.Label(self.employee_frame, text="Employee Name:").pack(anchor="w")
        self.name_var = tk.StringVar()
        ttk.Entry(self.employee_frame, textvariable=self.name_var, width=50).pack(fill="x", padx=10, pady=2)

        ttk.Label(self.employee_frame, text="Department:").pack(anchor="w")
        self.dept_var = tk.StringVar()
        self.dept_combo = ttk.Combobox(self.employee_frame, textvariable=self.dept_var, width=47, state="readonly")
        self.dept_combo['values'] = list(self.dept_mapping.keys())
        self.dept_combo.pack(fill="x", padx=10, pady=2)
        self.dept_combo.bind("<<ComboboxSelected>>", self.update_designation_options)

        ttk.Label(self.employee_frame, text="Designation:").pack(anchor="w")
        self.designation_var = tk.StringVar()
        self.designation_combo = ttk.Combobox(self.employee_frame, textvariable=self.designation_var, width=47, state="readonly")
        self.designation_combo.pack(fill="x", padx=10, pady=2)

        ttk.Separator(self.employee_frame, orient="horizontal").pack(fill="x", pady=10)
        
        self.start_date_picker = DateEntry(self.employee_frame, "Start Date:", callback=self.update_working_days)
        self.start_date_picker.pack(fill="x", padx=10, pady=2)
        self.end_date_picker = DateEntry(self.employee_frame, "End Date:", callback=self.update_working_days)
        self.end_date_picker.pack(fill="x", padx=10, pady=2)

        ttk.Label(self.employee_frame, text="Total Working Days (Calculated):").pack(anchor="w")
        self.working_days_var = tk.StringVar(value="0")
        ttk.Entry(self.employee_frame, textvariable=self.working_days_var, width=10, state="readonly").pack(anchor="w", padx=10)

        statutory_frame = ttk.Frame(self.employee_frame)
        statutory_frame.pack(anchor="w", padx=10, pady=10)
        self.sss_var = tk.BooleanVar()
        self.pagibig_var = tk.BooleanVar()
        self.philhealth_var = tk.BooleanVar()
        ttk.Checkbutton(statutory_frame, text="SSS", variable=self.sss_var).pack(side="left")
        ttk.Checkbutton(statutory_frame, text="Pag-IBIG", variable=self.pagibig_var).pack(side="left", padx=10)
        ttk.Checkbutton(statutory_frame, text="PhilHealth", variable=self.philhealth_var).pack(side="left")

    def update_designation_options(self, event=None):
        dept = self.dept_var.get()
        designations = self.dept_mapping.get(dept, [])
        self.designation_combo['values'] = designations
        if designations:
            self.designation_combo.current(0)
        else:
            self.designation_var.set("")

    def update_working_days(self):
        start = self.start_date_picker.get_date_obj()
        end = self.end_date_picker.get_date_obj()
        if start > end:
            self.working_days_var.set("0")
            return
        count = 0
        current = start
        while current <= end:
            if current.weekday() < 5: count += 1
            current += timedelta(days=1)
        self.working_days_var.set(str(count))

    def setup_salary_tab(self):
        ttk.Label(self.salary_frame, text="Salary & Earnings", font=("Arial", 12, "bold")).pack(pady=10)
        
        ttk.Label(self.salary_frame, text="Salary per Hour :").pack(anchor="w")
        self.hourly_var = tk.StringVar()
        ttk.Entry(self.salary_frame, textvariable=self.hourly_var, width=20).pack(anchor="w", padx=10)

        ttk.Label(self.salary_frame, text="Allowance :").pack(anchor="w")
        self.allowance_var = tk.StringVar()
        ttk.Entry(self.salary_frame, textvariable=self.allowance_var, width=20).pack(anchor="w", padx=10)

        commission_frame = ttk.LabelFrame(self.salary_frame, text="Commission")
        commission_frame.pack(fill="x", padx=10, pady=10)
        self.comm_type = tk.StringVar(value="none")
        ttk.Radiobutton(commission_frame, text="None", variable=self.comm_type, value="none").pack(side="left")
        ttk.Radiobutton(commission_frame, text="Fixed", variable=self.comm_type, value="fixed").pack(side="left")
        ttk.Radiobutton(commission_frame, text="Sales %", variable=self.comm_type, value="percent").pack(side="left")
        
        self.comm_amount_var = tk.StringVar()
        ttk.Entry(commission_frame, textvariable=self.comm_amount_var, width=10).pack(side="left", padx=5)
        self.comm_rate_var = tk.StringVar()
        ttk.Entry(commission_frame, textvariable=self.comm_rate_var, width=5).pack(side="left")
        ttk.Label(commission_frame, text="%").pack(side="left")

        ttk.Label(self.salary_frame, text="Overtime Pay:").pack(anchor="w")
        self.ot_var = tk.StringVar()
        ttk.Entry(self.salary_frame, textvariable=self.ot_var, width=20).pack(anchor="w", padx=10)

        ttk.Label(self.salary_frame, text="Tardy Deduction:").pack(anchor="w")
        self.tardy_var = tk.StringVar()
        ttk.Entry(self.salary_frame, textvariable=self.tardy_var, width=20).pack(anchor="w", padx=10)

    def setup_results_tab(self):
        self.results_text = scrolledtext.ScrolledText(self.results_frame, height=25, width=100, font=("Courier", 10))
        self.results_text.pack(fill="both", expand=True, padx=10, pady=10)

    def calculate_payslip(self):
        if not self.name_var.get().strip():
            messagebox.showerror("Error", "Enter Name")
            return

        self.employee.emp_name = self.name_var.get()
        self.employee.emp_department = self.dept_var.get()
        self.employee.emp_designation = self.designation_var.get()
        self.employee.pay_date = f"{self.start_date_picker.date_var.get()} to {self.end_date_picker.date_var.get()}"
        self.employee.working_days = int(self.working_days_var.get())
        self.employee.has_sss = self.sss_var.get()
        self.employee.has_pagibig = self.pagibig_var.get()
        self.employee.has_philhealth = self.philhealth_var.get()

        self.payslip = Payslip(self.employee)
        try:
            self.payslip.salary_perhour = float(self.hourly_var.get() or 0)
            self.payslip.allowance = float(self.allowance_var.get() or 0)
            self.payslip.overtime = float(self.ot_var.get() or 0)
            self.payslip.tardy = float(self.tardy_var.get() or 0)

            if self.comm_type.get() == "fixed":
                self.payslip.commission = float(self.comm_amount_var.get() or 0)
            elif self.comm_type.get() == "percent":
                self.payslip.commission = float(self.comm_amount_var.get() or 0) * (float(self.comm_rate_var.get() or 0) / 100)

            self.payslip.calculate_salary()
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, self.payslip.get_payslip_text())
        except ValueError:
            messagebox.showerror("Error", "Invalid numbers entered")

    def print_payslip(self):
        content = self.results_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "calculate the payslip first before printing.")
            return

        filename = "temp_payslip.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            
            # 'print' verb opens the system print dialog for .txt files
            os.startfile(filename, "print")
        except Exception as e:
            messagebox.showerror("Error", f"Could not print: {str(e)}")

    def clear_all(self):
        self.name_var.set("")
        self.dept_var.set("")
        self.designation_var.set("")
        self.hourly_var.set("")
        self.results_text.delete(1.0, tk.END)

    def new_employee(self):
        self.clear_all()
        for child in self.root.winfo_children():
            if isinstance(child, ttk.Notebook):
                child.select(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = PayslipGUI(root)
    root.mainloop()
