# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")

def solution(L):
    # write your code in Python 3.6



    list_local_names = []
    for email in L:
        list_local_names += [get_local_names_clean(email)]




def get_local_name(email):
    local_name = ''
    for i in email:
        if i == '@':
            break
        local_name += i
    return local_name


def get_clean_local_names(local_name):
    index_of_plus = 0
    index_of_at = 0
    setFlag = False

    for i in local_name:
        if i == '+':
            setFlag = True

    if setFlag:
        for i in range(0, len(local_name)):
            if local_name[i] == '+':
                index_of_plus = i
                break
        for i in range(0, len(local_name)):
            if local_name[i] == '@':
                index_of_at = i
                break
        a = ''
        for i in range(0, len(local_name)):
            if i not in range(index_of_plus, index_of_at):
                a += local_name[i]
        return a
    else:
        return local_name

def remove_dots(local_name):

    for i in range(0, len(local_name)):
        if local_name[i] == '@':
            index_of_at = i
            break




def get_local_names_clean(local_name):
    a = get_local_name(local_name)
    b = get_clean_local_names(a)
    return b





L = ["abcd@exam.com", "bcks.a+dfj....kld@eample.com"]


print(get_clean_local_names(L[1]))
solution(L)