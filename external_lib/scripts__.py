import members


def p1(global_dict):
    global_dict['attr2'] = 12345
    print(members.primitive_dict['memberID-0'])


def p2(global_dict):
    global_dict['attr4'] = 954.49


def p3(global_dict):
    members.primitive_dict['memberID-1']['个人自信水平'] = 1.0

