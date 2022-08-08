from flask import Flask, render_template, request

app = Flask(__name__)

class calculate_taxes:

    def __init__(self, salary, pf_status, tax_exemption = 0, saving = 0):
        self.salary = salary
        self.pf_status = pf_status
        self.tax_exemption = tax_exemption
        self.saving = saving

    def income_tax(self):
        if self.pf_status == 'yes':
            income_tax = round(((self.salary * 0.98) - self.tax_exemption) * 0.2,2)
        else:
            income_tax = round((self.salary - self.tax_exemption) * 0.2,2)
        return income_tax

    def pensions_contribution(self):
        if self.pf_status == 'yes':
            employee_contribution = self.salary * 0.02
            employer_contribution = self.salary * 0.02
            if self.salary * 12 <= 24000:
                pf_agency_contribution = self.salary * 0.02
            elif (self.salary * 12 > 24000) and (self.salary * 12 <= 60000):
                pf_agency_contribution = (2000 * 0.02) + ((self.salary - 2000)*0.01)
            else:
                pf_agency_contribution = (2000 * 0.02) + (3000 * 0.01)
            total_pf_contribution = employee_contribution + employer_contribution + pf_agency_contribution
        else:
            employee_contribution = 0
            employer_contribution = 0
            pf_agency_contribution = 0
            total_pf_contribution = 0
        return (total_pf_contribution, employee_contribution, employer_contribution, pf_agency_contribution)

    def vat_expenditures(self):
        if self.pf_status == 'yes':
            vat_expenses = (((self.salary * 0.98 - self.tax_exemption) * 0.8) + self.tax_exemption - self.saving) * 0.18
        else:
            vat_expenses = (((self.salary - self.tax_exemption) * 0.8) + self.tax_exemption - self.saving) * 0.18
        return vat_expenses

    def net_salary(self):
        if self.pf_status == 'yes':
            net_salary = (((self.salary * 0.98 - self.tax_exemption) * 0.8) + self.tax_exemption)
        else:
            net_salary = (((self.salary - self.tax_exemption) * 0.8) + self.tax_exemption)
        return net_salary

# 1. პროგრამა მომხმარებელს ეკითხება რა არის მისი გროს ანაზღაურება
# 2. პროგრამა ეკითხება მომხმარებელს სარგებლობს თუ არა ის რაიმე საგადასახდო შეღავათით
#    თუ სარგებლობს მომხმარებელმა უნდა მიუთითოს შეღავათის ოდენობა;
# 3. მომხმარებელს შეუძლია მიუთითოს გაკეთებული დანაზოგის რაოდენობა ლარებში;

# 4. პროგრამა ახალ გვერდზე გამოიტანს სრულ ინფორმაციას მომხმარებლის შესახებ:
#    რამდენია საშემოსავლო გადასახადი
#    რამდენის საპენსიო შენატანი (ჩაშლილად)
#    დააცლოებით დღგ-ში რამდენი მიდის
#    საბოლოო დასკვნა სახელმწიფოში გადასახადების სახით რა თანხა შედის
#    და საპენსიო სააგენტოში რამდენი



@app.route('/')
@app.route('/calc_amounts')
def entry_page():
    return render_template('index.html')

@app.route('/about')
def info_page():
    return render_template('about.html')

# Providing user info to backend side to assigne class parameters correctly.
@app.route('/calc_amounts', methods = ['POST'])
def calculations_page():
    salary = int(request.form['salary'])
    pf_status = request.form['PF_status']

    if request.form['tax_exemption'] != '':
        tax_exemption = int(request.form['tax_exemption'])
    else:
        tax_exemption = 0

    if request.form['saving'] != '':
        saving = int(request.form['saving'])
    else:
        saving = 0

    amount = calculate_taxes(salary, pf_status, tax_exemption, saving)
    income_tax = amount.income_tax()

    total_pf_contribution = round(amount.pensions_contribution()[0],2)
    employee_contribution = round(amount.pensions_contribution()[1],2)
    employer_contribution = round(amount.pensions_contribution()[2],2)
    pf_agency_contribution = round(amount.pensions_contribution()[3],2)

    vat_expenses = round(amount.vat_expenditures(),2)
    net_salary = round(amount.net_salary(),2)

    return render_template('calc_amounts.html',
                            income_tax = income_tax,
                            total_pf_contribution = total_pf_contribution,
                            employee_contribution = employee_contribution,
                            employer_contribution = employer_contribution,
                            pf_agency_contribution = pf_agency_contribution,
                            vat_expenses = vat_expenses,
                            net_salary = net_salary)





if __name__ == '__main__':
  app.run(debug = True)
