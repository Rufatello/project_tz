from datetime import datetime


class XMLValidation:
    @staticmethod
    def ogrn_value(ogrn):
        if not ogrn:
            print('ОГРН обязательное поле')
            return False
        if len(ogrn) == 13 and ogrn.isdigit():
            return True
        print(f'ОГРН должен быть равен 13 символам и состоять из цифр, а у вас {ogrn}')
        return False

    @staticmethod
    def inn_value(inn):

        if not inn:
            print('ИНН обязательное поле')
            return False
        if len(inn) == 10 and inn.isdigit():
            return True
        print(f'ИНН должен быть равен 10 символам и состоять из цифр, а у вас {inn}')
        return False

    @staticmethod
    def date(date):
        if not date:
            print('Дата обязательное поле')
            return False

        try:
            datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            print(f'Дата должна быть в формате YYYY-MM-DD, а у вас {date}')
            return False
