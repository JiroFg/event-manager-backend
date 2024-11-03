from schemas.company_schema import Company, CompanyDisplay
from config.db_connection import PostgresConnection
from fastapi.encoders import jsonable_encoder

class CompanyController():
    def __init__(self):
        self.conn = PostgresConnection.get_instance()
        self.cursor = self.conn.cursor()
    
    def create(self, new_company: Company):
        # Validate if a company with the inputted rfc already exist
        query = "SELECT * FROM companies WHERE rfc = %s"
        self.cursor.execute(query, (new_company.rfc,))
        row = self.cursor.fetchone()
        if row:
            return {
                "error": True,
                "details": "Company with that RFC already exists"
            }
        # Create the new company
        query = "INSERT INTO companies (name, commercial_name, logo_url, phone, rfc, email, website_url, employee_count, address, state_id, zip_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(query, (
            new_company.name,
            new_company.commercial_name,
            new_company.logo_url,
            new_company.phone,
            new_company.rfc,
            new_company.email,
            new_company.website_url,
            new_company.employee_count,
            new_company.address,
            new_company.state_id,
            new_company.zip_code
        ))
        self.conn.commit()
        rows_affected = self.cursor.rowcount
        self.cursor.close()
        if rows_affected > 0:
            return {
                "error": False,
                "details": "Company created successfully"
            }
        else:
            return {
                "error": True,
                "details": "Company couldn't be created"
            }
    
    def get_company(self, company_id: int):
        query = "SELECT * FROM companies WHERE company_id = %s"
        self.cursor.execute(query, (company_id,))
        row = self.cursor.fetchone()
        if not row:
            return {
                "error": True,
                "details": "Company not found"
            }
        found_company = CompanyDisplay(
            company_id=row[0],
            name=row[1],
            commercial_name=row[2],
            logo_url=row[3],
            phone=row[4],
            rfc=row[5],
            email=row[6],
            website_url=row[7],
            employee_count=row[8],
            address=row[9],
            state_id=row[10],
            zip_code=row[11]
        )
        return jsonable_encoder(found_company)