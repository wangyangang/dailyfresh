from django.test import TestCase
from fdfs_client.client import *

import django
# Create your tests here.

if __name__ == '__main__':
    client_conf_obj = get_tracker_conf('/User/mac/Documents/projects/python_self_teaching/'
                                       'dailyfresh/utils/fdfs/client.conf')
    client = Fdfs_client(client_conf_obj)
    ret = client.upload_by_filename('/User/mac/Pictures/1.jpg')
