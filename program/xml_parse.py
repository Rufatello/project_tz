from datetime import datetime
import xml.etree.ElementTree as ET
from database import DatabaseManager
from validation import XMLValidation


class XML(DatabaseManager):
    def __init__(self, xml_file, db_name, params):
        super().__init__(db_name, params)
        self.xml_file = xml_file

    def save_dict(self):
        tree = ET.parse(self.xml_file)
        root = tree.getroot()

        companies_by_ogrn = {}
        invalid_company = {}
        for i in root.findall('КОМПАНИЯ'):
            ogrn = i.find('ОГРН').text.strip()
            inn = i.find('ИНН').text.strip()
            date = i.find('ДатаОбн').text.strip()
            name = i.find('НазваниеКомпании').text.strip()
            phones = [phone.text.strip() for phone in i.findall('Телефон') if phone is not None]
            if not XMLValidation.ogrn_value(ogrn):
                continue
            if not XMLValidation.inn_value(inn):
                continue
            if not XMLValidation.date(date):
                continue
            date = datetime.strptime(date, "%Y-%m-%d")
            if ogrn in companies_by_ogrn:
                if date > companies_by_ogrn[ogrn]['date']:
                    invalid_company[companies_by_ogrn[ogrn]['ogrn']] = companies_by_ogrn[ogrn]
                    companies_by_ogrn[ogrn] = {'ogrn': ogrn, 'inn': inn, 'date': date, 'name': name, 'phones': phones}
            else:
                companies_by_ogrn[ogrn] = {'ogrn': ogrn, 'inn': inn, 'date': date, 'name': name, 'phones': phones}
        if invalid_company:
            print(f'У компании дата позднее: {invalid_company}')
        else:
            print('Нет компаний с более поздней датой.')

        return companies_by_ogrn

    def dbrec(self):
        self.create_database()
        self.create_table()
        self.connect(self.db_name)

        companies_by_ogrn = self.save_dict()

        with self.connection.cursor() as cur:
            for company in companies_by_ogrn.values():
                ogrn = company['ogrn']
                inn = company['inn']
                date = company['date'].strftime("%Y-%m-%d")
                name = company['name']
                phones = company['phones']

                cur.execute('''
                    INSERT INTO company (ogrn, inn, date, name)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                ''', (ogrn, inn, date, name))
                company_id = cur.fetchone()[0]

                for phone in phones:
                    cur.execute('''
                        INSERT INTO phone (company_id, phone)
                        VALUES (%s, %s)
                    ''', (company_id, phone))

            self.connection.commit()

        self.close_connect()

