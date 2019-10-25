def update_dic_test():
    context = {'name': 'wyg'}
    context['age'] = 19
    print(context['age'])
    print(context)


if __name__ == '__main__':
    # update_dic_test()
    import os
    file_name = 'abc.text.doc.jpg'
    print(os.path.splitext(file_name)[1])
    print(os.path.splitext(file_name)[-1])