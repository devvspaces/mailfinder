import logging

logging.basicConfig(
    filename = 'my_run_logs.log',
    level =  logging.INFO,
    format ="%(asctime)s:%(levelname)s:%(message)s"
)


# def add(x, y):
#     return x + y

# def substract(x, y):
#     return x - y

# def multiply(x, y):
#     return x * y

# def divide(x, y):
#     return x / y

# num_1 = 10
# num_2 = 5

# add_result = add(num_1, num_2)
# logging.debug('Add: {} + {} = {}'.format(num_1, num_2, add_result))

# sub_result = substract(num_1, num_2)
# logging.debug('Add: {} - {} = {}'.format(num_1, num_2, sub_result))

# mul_result = multiply(num_1, num_2)
# logging.debug('Add: {} * {} = {}'.format(num_1, num_2, mul_result))

# div_result = divide(num_1, num_2)
# logging.debug('Add: {} / {} = {}'.format(num_1, num_2, div_result))

class Employee:
    '''Sample employee class'''
    def __init__(self, first, last):
        self.first = first
        self.last = last

        logging.info('Created Employee class: {} - {}'.format(self.first, self.last))
    
    @property
    def email(self):
        return '{}.{}@email.com'.format(self.first, self.last)
    
    @property
    def fullname(self):
        return '{} {}'.format(self.first, self.last)


emp1=Employee('John','Smith')
emp1=Employee('Ayanwola','Ayomide')
emp1=Employee('Gary','Doe')