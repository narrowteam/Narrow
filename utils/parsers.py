from UserManagement.models import User
from django.db.models import Q

def list_of_dicts_to_dict_of_list(list_of_dicts, necessary_keys=None):
    data ={}
    for key in necessary_keys:
        data[key]=[]

    for dict in list_of_dicts:
        for key, value in dict.items():
            if not key in data: data[key] = []
            data[key].append(value)
    return data

'''
    Abstraction to convert list of user unique parameters dicts, to user list
    [{id:2}, {id,:5},{email:test@test.com)] => 3 users queryset
'''
class EmailOrIdUserList():
    def __init__(self, list_of_dicts):
        self.list_of_dicts = list_of_dicts
        self.dict_of_list = self.list_of_dicts_to_dict_of_list(list_of_dicts, ['email', 'id'])

    def get_user_models(self):
        users = User.objects.filter(Q(email__in=self.dict_of_list['email']) | Q(id__in=self.dict_of_list['id']))
        return users

    def list_of_dicts_to_dict_of_list(self, list_of_dicts, necessary_keys=None):
        data = {}
        for key in necessary_keys:
            data[key] = []

        for dict in list_of_dicts:
            for key, value in dict.items():
                if not key in data: data[key] = []
                data[key].append(value)
        return data
