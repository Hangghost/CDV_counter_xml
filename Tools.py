def print_type(object):
    print(object)
    print(type(object))


def CDV_counter(CDV_name, tag_list, other_name = None):
    CDV_count = 0
    for element in tag_list:
        CDV_count += element.count(str(CDV_name))
        if CDV_count == 0:
            CDV_count += element.count(str(other_name))
    return CDV_count


        