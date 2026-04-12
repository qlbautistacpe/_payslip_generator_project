import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import tkinter.font as tkfont



class DateEntry: # Custom Date Entry Widget
    def __init__(self, parent, label_text):
        self.frame = ttk.Frame(parent)
        ttk.Label(self.frame, text=label_text).pack(side="left")

        # Month
        ttk.Label(self.frame, text="MM").pack(side="left", padx=(5, 2))
        self.month_var = tk.StringVar(value="01")
        month_combo = ttk.Combobox(self.frame, textvariable=self.month_var, width=3, state="readonly")
        month_combo['values'] = [f"{i:02d}" for i in range(1, 13)]
        month_combo.pack(side="left", padx=2)

        # Day
        ttk.Label(self.frame, text="DD").pack(side="left", padx=(5, 2))
        self.day_var = tk.StringVar(value="01")
        day_combo = ttk.Combobox(self.frame, textvariable=self.day_var, width=3, state="readonly")
        day_combo['values'] = [f"{i:02d}" for i in range(1, 32)]
        day_combo.pack(side="left", padx=2)

        # Year
        ttk.Label(self.frame, text="YYYY").pack(side="left", padx=(5, 2))
        self.year_var = tk.StringVar(value=datetime.now().strftime("%Y"))
        year_combo = ttk.Combobox(self.frame, textvariable=self.year_var, width=6, state="readonly")
        years = [str(y) for y in range(2020, 2031)]
        year_combo['values'] = years
        year_combo.pack(side="left", padx=2)

        # Today button
        ttk.Button(self.frame, text="Today", command=self.set_today).pack(side="left", padx=5)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def get_date(self):
        try:
            dt = datetime(int(self.year_var.get()), int(self.month_var.get()), int(self.day_var.get()))
            return dt.strftime("%m-%Y")
        except:
            return ""

    def set_today(self):
        today = datetime.now()
        self.month_var.set(today.strftime("%m"))
        self.day_var.set(today.strftime("%d"))
        self.year_var.set(today.strftime("%Y"))


class Employee:
    # Handles employee data collection - stores data instead of console input

    def __init__(self):
        self.emp_company = ""
        self.company_address = ""
        self.emp_name = ""
        self.emp_department = ""
        self.emp_designation = ""
        self.date_today = datetime.now().date()
        self.pay_date = ""
        self.working_days = 0
        self.emp_statutory = "Without Contributions"


class Payslip:
    def __init__(self, employee):
        self.employee = employee
        # Salary inputs
        self.salary_perhour = 0.0
        self.allowance = 0.0
        self.commission = 0.0
        self.overtime = 0.0
        self.tardy = 0.0

        # Fixed rates
        self.sss_rate = 0.05
        self.pag_ibig_rate = 0.02
        self.philhealth_rate = 0.025
        self.professional_tax = 300

        # Calculated fields
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

        if self.employee.emp_statutory == "With Contributions":
            self.sss_ded = self.gross_pay * self.sss_rate
            self.pag_ibig_ded = min(self.gross_pay * self.pag_ibig_rate, 200)
            self.philhealth_ded = self.gross_pay * self.philhealth_rate
        else:
            self.sss_ded = self.pag_ibig_ded = self.philhealth_ded = 0

        taxable_income = self.gross_pay - (self.sss_ded + self.pag_ibig_ded + self.philhealth_ded)

        if taxable_income <= 20833:
            self.income_tax = 0
        elif taxable_income <= 33333:
            self.income_tax = (taxable_income - 20833) * 0.15
        elif taxable_income <= 66667:
            self.income_tax = 1875 + (taxable_income - 33333) * 0.20
        else:
            self.income_tax = 8541.80 + (taxable_income - 66667) * 0.25

        self.total_deduction = (
                self.sss_ded + self.pag_ibig_ded + self.philhealth_ded +
                self.income_tax + self.professional_tax + self.tardy
        )
        self.net_pay = self.gross_pay - self.total_deduction

    def get_payslip_text(self):
        # displays generated payslip
        text = "=" * 45 + "\n"
        text += "                 PAYSLIP\n"
        text += "=" * 45 + "\n"
        text += f"Company Name     : {self.employee.emp_company}\n"
        text += f"Employee Name    : {self.employee.emp_name}\n"
        text += f"Department       : {self.employee.emp_department}\n"
        text += f"Designation      : {self.employee.emp_designation}\n"
        text += f"Contribution     : {self.employee.emp_statutory}\n"
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
        self.root.resizable(False, False)

        self.employee = Employee()
        self.payslip = None

        self.pay_date_picker = None  # Store date picker reference

        self.setup_ui()

    def setup_ui(self):
        # Main notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both",
                      expand=True,
                      padx=10,
                      pady=10)

        # Employee Details Tab
        self.employee_frame = ttk.Frame(notebook)
        notebook.add(self.employee_frame,
                     text="1. Employee Details")
        self.setup_employee_tab()

        # Salary Details Tab
        self.salary_frame = ttk.Frame(notebook)
        notebook.add(self.salary_frame,
                     text="2. Salary Details")
        self.setup_salary_tab()

        # Results Tab
        self.results_frame = ttk.Frame(notebook)
        notebook.add(self.results_frame,
                     text="3. Payslip")
        self.setup_results_tab()

        # Buttons frame
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x",
                       padx=10,
                       pady=5)

        ttk.Button(btn_frame,
                   text="Calculate Payslip",
                   command=self.calculate_payslip).pack(side="left",
                                                        padx=5)
        ttk.Button(btn_frame,
                   text="Clear All",
                   command=self.clear_all).pack(side="left",
                                                padx=5)
        ttk.Button(btn_frame,
                   text="New Employee",
                   command=self.new_employee).pack(side="right",
                                                   padx=5)

    def setup_employee_tab(self):
        # Company Details
        ttk.Label(self.employee_frame,
                  text="Company Details",
                  font=("Arial", 12, "bold")).pack(pady=5)
        ttk.Label(self.employee_frame,
                  text="Company Name:").pack(anchor="w")
        self.company_var = tk.StringVar()
        ttk.Entry(self.employee_frame,
                  textvariable=self.company_var,
                  width=50).pack(fill="x",
                                 padx=10, pady=2)

        ttk.Label(self.employee_frame, text="Company Address:").pack(anchor="w")
        self.address_var = tk.StringVar()
        ttk.Entry(self.employee_frame, textvariable=self.address_var, width=50).pack(fill="x", padx=10, pady=2)

        # Employee Details
        ttk.Separator(self.employee_frame, orient="horizontal").pack(fill="x", pady=10)
        ttk.Label(self.employee_frame, text="Employee Details", font=("Arial", 12, "bold")).pack(pady=5)

        ttk.Label(self.employee_frame, text="Employee Name:").pack(anchor="w")
        self.name_var = tk.StringVar()
        ttk.Entry(self.employee_frame, textvariable=self.name_var, width=50).pack(fill="x", padx=10, pady=2)

        ttk.Label(self.employee_frame, text="Department:").pack(anchor="w")
        self.dept_var = tk.StringVar()
        ttk.Entry(self.employee_frame, textvariable=self.dept_var, width=50).pack(fill="x", padx=10, pady=2)

        ttk.Label(self.employee_frame, text="Designation:").pack(anchor="w")
        self.designation_var = tk.StringVar()
        ttk.Entry(self.employee_frame, textvariable=self.designation_var, width=50).pack(fill="x", padx=10, pady=2)

        # Pay Period - DATE PICKER
        ttk.Separator(self.employee_frame, orient="horizontal").pack(fill="x", pady=10)
        ttk.Label(self.employee_frame, text="Pay Period Details", font=("Arial", 12, "bold")).pack(pady=5)

        self.pay_date_picker = DateEntry(self.employee_frame, "Date of Payment:")
        self.pay_date_picker.pack(fill="x", padx=10, pady=5)

        ttk.Label(self.employee_frame, text="Working Days (1-31):").pack(anchor="w", pady=(10, 0))
        self.working_days_var = tk.StringVar()
        self.working_days_entry = ttk.Entry(self.employee_frame, textvariable=self.working_days_var, width=10)
        self.working_days_entry.pack(anchor="w", padx=10, pady=2)

        # Statutory Contributions
        ttk.Label(self.employee_frame, text="Government Contributions:").pack(anchor="w", pady=(10, 0))
        self.statutory_var = tk.StringVar(value="No")
        statutory_frame = ttk.Frame(self.employee_frame)
        statutory_frame.pack(anchor="w", padx=10, pady=2)
        ttk.Radiobutton(statutory_frame, text="Yes (SSS, Pag-IBIG, PhilHealth)",
                        variable=self.statutory_var, value="Yes").pack(side="left")
        ttk.Radiobutton(statutory_frame, text="No",
                        variable=self.statutory_var, value="No").pack(side="left", padx=(20, 0))

    def setup_salary_tab(self):
        ttk.Label(self.salary_frame, text="Salary & Earnings", font=("Arial", 12, "bold")).pack(pady=10)

        # Basic salary
        ttk.Label(self.salary_frame, text="Salary per Hour (₱):").pack(anchor="w")
        self.hourly_var = tk.StringVar()
        ttk.Entry(self.salary_frame, textvariable=self.hourly_var, width=20).pack(anchor="w", padx=10, pady=2)

        # Allowance
        ttk.Label(self.salary_frame, text="Allowance (₱):").pack(anchor="w")
        self.allowance_var = tk.StringVar()
        ttk.Entry(self.salary_frame, textvariable=self.allowance_var, width=20).pack(anchor="w", padx=10, pady=2)

        # Commission frame
        ttk.Label(self.salary_frame, text="Commission:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(20, 0))
        commission_frame = ttk.LabelFrame(self.salary_frame, text="Commission Type")
        commission_frame.pack(fill="x", padx=10, pady=5)

        self.comm_type = tk.StringVar()
        ttk.Radiobutton(commission_frame, text="None", variable=self.comm_type,
                        value="none").pack(side="left", padx=5)
        ttk.Radiobutton(commission_frame, text="Fixed Amount (₱)", variable=self.comm_type,
                        value="fixed").pack(side="left", padx=5)
        ttk.Radiobutton(commission_frame, text="Sales %", variable=self.comm_type,
                        value="percent").pack(side="left", padx=5)

        ttk.Label(commission_frame, text="Amount/Sales:").pack(side="left", padx=(20, 0))
        self.comm_amount_var = tk.StringVar()
        ttk.Entry(commission_frame, textvariable=self.comm_amount_var, width=15).pack(side="left", padx=5)
        ttk.Label(commission_frame, text=" %").pack(side="left")
        self.comm_rate_var = tk.StringVar()
        ttk.Entry(commission_frame, textvariable=self.comm_rate_var, width=10).pack(side="left", padx=(5, 10))

        # Other earnings/deductions
        ttk.Label(self.salary_frame, text="Other Earnings & Deductions",
                  font=("Arial", 10, "bold")).pack(anchor="w", pady=(20, 0))

        ttk.Label(self.salary_frame, text="Overtime Pay (₱):").pack(anchor="w")
        self.ot_var = tk.StringVar()
        ttk.Entry(self.salary_frame, textvariable=self.ot_var, width=20).pack(anchor="w", padx=10, pady=2)

        ttk.Label(self.salary_frame, text="Tardy/Absent Deduction (₱):").pack(anchor="w")
        self.tardy_var = tk.StringVar()
        ttk.Entry(self.salary_frame, textvariable=self.tardy_var, width=20).pack(anchor="w", padx=10, pady=2)

    def setup_results_tab(self):
        self.results_text = scrolledtext.ScrolledText(self.results_frame, height=25, width=100, wrap=tk.WORD)
        self.results_text.pack(fill="both", expand=True, padx=10, pady=10)

    def validate_employee_data(self): # validates whole data before receiving
        if not self.company_var.get().strip():
            messagebox.showerror("Error", "Please enter Company Name")
            return False
        if not self.name_var.get().strip():
            messagebox.showerror("Error", "Please enter Employee Name")
            return False

        try:
            days = int(self.working_days_var.get() or 0)
            if not 1 <= days <= 31:
                messagebox.showerror("Error", "Working days must be between 1-31")
                return False
        except ValueError:
            messagebox.showerror("Error", "Please enter valid Working Days (1-31)")
            return False

        if not self.pay_date_picker.get_date():
            messagebox.showerror("Error", "Please select a valid payment date")
            return False
        return True

    def calculate_payslip(self):
        if not self.validate_employee_data():
            return

        # Update employee data
        self.employee.emp_company = self.company_var.get()
        self.employee.company_address = self.address_var.get()
        self.employee.emp_name = self.name_var.get()
        self.employee.emp_department = self.dept_var.get()
        self.employee.emp_designation = self.designation_var.get()
        self.employee.pay_date = self.pay_date_picker.get_date()  # Uses date picker
        self.employee.working_days = int(self.working_days_var.get())
        self.employee.emp_statutory = "With Contributions" if self.statutory_var.get() == "Yes" else "Without Contributions"

        # Create payslip and populate salary data
        self.payslip = Payslip(self.employee)

        try:
            self.payslip.salary_perhour = float(self.hourly_var.get() or 0)
            self.payslip.allowance = float(self.allowance_var.get() or 0)
            self.payslip.overtime = float(self.ot_var.get() or 0)
            self.payslip.tardy = float(self.tardy_var.get() or 0)

            # Commission calculation
            if self.comm_type.get() == "fixed":
                self.payslip.commission = float(self.comm_amount_var.get() or 0)
            elif self.comm_type.get() == "percent":
                sales = float(self.comm_amount_var.get() or 0)
                rate = float(self.comm_rate_var.get() or 0)
                self.payslip.commission = sales * (rate / 100)
            else:
                self.payslip.commission = 0

            # Calculate and display
            self.payslip.calculate_salary()
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, self.payslip.get_payslip_text())

            # Switch to results tab
            self.root.nametowidget(".!notebook").select(2)

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for salary fields")

    def clear_all(self):
        self.company_var.set("")
        self.address_var.set("")
        self.name_var.set("")
        self.dept_var.set("")
        self.designation_var.set("")
        self.pay_date_picker.month_var.set("01")
        self.pay_date_picker.day_var.set("01")
        self.pay_date_picker.year_var.set(datetime.now().strftime("%Y"))
        self.working_days_var.set("")
        self.statutory_var.set("No")
        self.hourly_var.set("")
        self.allowance_var.set("")
        self.comm_type.set("none")
        self.comm_amount_var.set("")
        self.comm_rate_var.set("")
        self.ot_var.set("")
        self.tardy_var.set("")
        self.results_text.delete(1.0, tk.END)

    def new_employee(self): # starts a new employee instance
        self.company_var.set("")
        self.address_var.set("")
        self.name_var.set("")
        self.dept_var.set("")
        self.designation_var.set("")
        self.pay_date_picker.month_var.set("01")
        self.pay_date_picker.day_var.set("01")
        self.pay_date_picker.year_var.set(datetime.now().strftime("%Y"))
        self.working_days_var.set("")
        self.statutory_var.set("No")
        self.root.nametowidget(".!notebook").select(0)


if __name__ == "__main__":
    root = tk.Tk()
    app = PayslipGUI(root)
    root.mainloop()