import streamlit as st
from experta import Fact, KnowledgeEngine, Field, Rule, P, AS, MATCH, TEST

# Define LoanApplicant Facts
class LoanApplicant(Fact):
    """Fact representation of a loan applicant"""
    name = Field(str, mandatory=True)
    age = Field(int, mandatory=True)
    marital_status = Field(str, mandatory=True)
    employment_status = Field(str, mandatory=True)
    annual_income = Field(int, mandatory=True)
    family_size = Field(int, mandatory=True)
    loan_amount = Field(int, mandatory=True)
    existing_debt = Field(int, mandatory=True)
    loan_purpose = Field(str, mandatory=True)
    loan_term = Field(int, mandatory=True)
    monthly_expenses = Field(int, mandatory=True)
    has_collateral = Field(bool, mandatory=True)
    bankruptcy_history = Field(bool, mandatory=True)

# Define LoanApprovalRules
class LoanApprovalRules(KnowledgeEngine):
    
    def __init__(self):
        super().__init__()
        self.decision = "Loan Denied"
        self.approved_amount = 0
    
    @Rule(
        AS.applicant << LoanApplicant(
            age=MATCH.age, 
            employment_status=MATCH.es, 
            marital_status=MATCH.ms,
            family_size=MATCH.fs, 
            loan_purpose=MATCH.lp,
            existing_debt=P(lambda x: x < 300000), # Existing Debt should not be more than 50% of Annual income
            loan_term=P(lambda x: x <= 60), # Longer periods increase risk
            bankruptcy_history=False, # Bankruptcy history shows inability to repay debts
            has_collateral = MATCH.collateral, 
            monthly_expenses = MATCH.m_exp,
            annual_income = MATCH.income),
        TEST(lambda collateral, income:
            (collateral and income > 0)), # Collateral reduces lender's risk
        TEST(lambda income, m_exp: # income -> annual_income | m_exp -> monthly_expenses 
            (m_exp / (income/12)) * 100 < 70),# Monthly expenses should not exceed 70% of Monthly Income
        TEST(lambda ms, fs: # ms -> marital_status | fs -> family_size
            # More dependants higher expenses
            (ms == "Single" and fs <= 2) or 
            (ms == "Married" and fs <= 4)), 
        TEST(lambda age, lp, es, income: # lp -> loan_purpose | es -> employment_status
            (age <= 25 and lp == "Education" and es == "Student" and income >= 72000) or # loan to students accepted
            (age >= 25 and # Applicant to be of reasonable age
             lp in ["Business", "Education", "Medical"] and # Reasonable loan request
             es == "Employed" and # Preference for stable employment
             income >= 600000)) # Annual income should be at least 600000
        )
        
    def approve_loan(self, applicant):
        self.decision = "Loan Approved"
        # Loan request amount should align with income level
        self.approved_amount = min(applicant.get("loan_amount"), applicant.get("annual_income") * 0.4)
    
    @Rule(AS.applicant << LoanApplicant())
    def deny_loan(self, applicant):
        self.decision = "Loan Denied"
        self.approved_amount = 0
    
# Streamlit UI
def main():
    st.set_page_config(page_title="Loan Application")
    st.title("Loan Application")
    
    name = st.text_input("What's your name:")
    if name:
        st.info(f"Hello {name}, Enter your loan details below.")
    
    col1, col2, col3 = st.columns(3, vertical_alignment="top", border=True, gap="small")
    with col1:
        age = st.number_input("Age", min_value=18, max_value=100, step=1)
        marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced", "Other"])
        family_size = st.number_input("Family Size", min_value=0, step=1)
        employment_status = st.selectbox("Employment Status", ["Employed", "Self-Employed", "Unemployed", "Retired", "Student"])
        loan_purpose = st.selectbox("Purpose of Loan", ["Business", "Home", "Car", "Education", "Medical", "Other"]) 
        
    
    with col2:
        annual_income = st.number_input("Annual Income(Kshs)", min_value=0, step=10000)
        existing_debt = st.number_input("Existing Debt(Kshs)", min_value=0, step=1000)
        loan_term = st.number_input("Loan Term (Months)", min_value=0, max_value=720, step=3)
        monthly_expenses = st.number_input("Monthly Expenses(Kshs)", min_value=0, step=1000)
        loan_amount = st.number_input("Loan Request(Kshs):", min_value=0, step=1000)
    
    with col3:
        has_collateral = st.checkbox("Do you have collateral?")
        bankruptcy_history = st.checkbox("Have you declared bankruptcy before?")
    
        if st.button("Submit Application"):
            engine = LoanApprovalRules()
            engine.reset()
            engine.declare(
                LoanApplicant(
                    name=name, 
                    age=age, 
                    marital_status=marital_status,
                    employment_status=employment_status, 
                    annual_income=annual_income, 
                    family_size=family_size, 
                    loan_amount=loan_amount, 
                    existing_debt=existing_debt, 
                    loan_purpose=loan_purpose, 
                    loan_term=loan_term, 
                    monthly_expenses=monthly_expenses, 
                    has_collateral=has_collateral, 
                    bankruptcy_history=bankruptcy_history)
            )
            engine.run()
            if engine.decision == 'Loan Approved':
                st.success('Loan Approved')
                st.write(f'Amount : Kshs {engine.approved_amount:.2f}')
            else:
                st.error('Loan Denied')
    
if __name__ == "__main__":
    main()
