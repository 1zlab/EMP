from distutils.core import setup

setup(
    name = 'emp-1zlab',      
    version = '0.2.2',
    py_modules = ['emp_wifi','emp_boot','emp_ide','emp_utils','emp_webrepl'],
    author = 'fuermohao@1zlab.com',        
    author_email = 'fuermohao@outlook.com',
    url = 'http://emp.1zlab.com',
    description = 'EMP(Easy MicroPython) is a upy module to make things Easy on MicroPython.'   
    )