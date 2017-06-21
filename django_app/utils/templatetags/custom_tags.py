from django import template

register = template.Library()


@register.filter
def query_string(q):
    # value에는 QueryDict가 온다.
    # ret = '?'
    # for k, v_list in q.lists():
    #     for v in v_list:
    #         ret += '&{}={}'.format(k, v)
    # return ret
    # 위 내용을 한줄로 줄임
    return '?' + '&'.join(['{}={}'.format(k, v) for k, v_list in q.lists() for v in v_list])
