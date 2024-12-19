from config import config
from program.xml_parse import XML


def main():
    db_params = config(filename='database.ini', section='postgresql')

    db_name = 'companies_db'

    xml_file = 'companies.xml'

    xml_processor = XML(xml_file, db_name, db_params)
    xml_processor.dbrec()


if __name__ == "__main__":
    main()
