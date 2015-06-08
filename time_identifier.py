# _*_ coding: utf-8 _*_

__author__ = 'acepor'

import gc
import itertools
from my_tools import now_str
from operator import itemgetter
from datetime import datetime
import re


########################################################################


TIME_MORPHEMES = ['年#NT', '年#NN', '年#M', '年#AD', '年#JJ', '年内#NT',
                  '月#NT', '月#NN', '月#M', '月#CD', '月份#NN', '月份#NT', '月#AD',
                  '周#NN', '周#NT', '周#M', '周#VV', '周#JJ', '礼拜#NN', '礼拜#NT', '礼拜#M', '星期#NN', '星期#NT',
                  '日#NN', '日#NT', '日#AD','日#M', '天#NN', '天#NT', '天#AD', '天#M', '夜#AD', '夜#NT',
                  '节#NN', '节#NT', '底#NN', '底#NT', '初#NN', '初#NT',
                  '季度#NN', '季度#NT', '季#NN', '季#NT',
                  '分#M', '分钟#M', '小时#M', '片刻#AD']

PAST_PREFIX = ['前#DT', '前#LC', '前#JJ', '前面#LC', '上#DT', '上#LC', '上个#DT', '过去#NT', '过去#NN', '过去#NT 的#DEG']

PAST_SUFFIX = ['前#DT', '前#LC', '前#JJ', '前#AD',
               '底#NN', '底#NT', '初#NN', '初#NT', '初#LC', '以来#LC', '以来#AD']

PAST_AD = ['曾经#AD', '曾#AD', '最初#AD', '此前#AD', '之前#AD', '先前#AD', '往前#AD', '日前#AD', '早前#AD',
           '早日#AD', '上次#AD', '不久前#AD', '已经#AD', '已#AD', '早已#AD', '早就#AD', '以前#AD', '事先#AD4'
           '年来#AD', '前不久#AD', '不久以后#AD', '不久#AD', '前一天#AD', '去年同期#AD',
           '当初#AD', '起初#AD', '本来#AD', '刚才#AD', '早就#AD']

PAST_CD = ['去年底#CD']

PAST_NN = ['此前#NN', '之前#NN', '从前#NN', '先前#NN', '以往#NN', '往前#NN', '不久前#NN', '刚才#NN',
           '上年#NN', '去年#NN', '前年#NN', '上一年#NN', '年初#NN', '近些年#NN', '早年间#NN', '近三年#NN', '去年同期#NN',
           '去年初#NN', '去年底#NN', '近半年#NN', '早年#NN', '前些年#NN', '往年#NN', '年前#NN', '年来#NN',
           '上个月#NN', '上月#NN', '上月底#NN', '月前#NN', '月来#NN', '月末#NN',
           '上周#NN', '上个星期#NN', '上星期#NN', '上礼拜#NN', '上个礼拜#NN',
           '前日#NN', '前夜#NN', '天前#NN', '日前#NN', '昨夜#NN', '昨天#NN', '昨日#NN',
           '前一天#NN', '前三天#NN', '次日#NN', '昨天上午#NN', '昨天中午#NN', '昨天夜里#NN', '近些天#NN', '往日#NN', '近日#NN',
           '上次#NN', '最初#NN', '早前#NN', '生前#NN', '近期#NN', '近期内#NN', '早些时候#NN', '初期#NN', '早期#NN', '老早#NN',
           '前半生#NN', '公元前#NN',
           '早已#NN', '早就#NN', '起先#NN']

PAST_M = ['年来#M']

PAST_NT = ['之前#NT', '从前#NT', '以往#NT', '最初#NT', '当初#NT', '不久#NT', '先前#NT', '此前#NT', '以前#NT', '最近#NT', '当初#AD',
           '年初#NT', '前年#NT', '上年#NT', '去年#NT', '幼年#NT', '往年#NT', '早年#NT', '近些年#NT', '前些年#NT', '近两年#NT',
           '近半年#NT', '近年#NT', '年内#NT', '早年间#NT', '年来#NT', '年前#NT', '年末#NT', '当年#NT', '历年#NT', '前几年#NT',
           '近些年#NT', '早些年#NT', '前半年#NT', '早年#NT', '前些天#NT',
           '月初#NT', '上月#NT', '上个月#NT', '上月底#NT', '月前#NT', '月来#NT', '月末#NT', '本月初#NT', '前月#NT',
           '上周#NT', '上个星期#NT', '上星期#NT', '上礼拜#NT', '上个礼拜#NT', '上周末#NT',
           '前夜#NT', '前天#NT', '前日#NT', '往日#NT', '昨夜#NT', '昨天#NT', '昨日#NT', '近日#NT', '前一天#NT', '前晚#NT',
           '前三天#NT', '近些天#NT', '天前#NT', '日前#NT', '前些天#NT',
           '前半生#NT', '近期#NT', '近期内#NT', '近来#NT', '上世纪#NT', '节前#NT', '上季#NT', '前段时间#NT', '前不久#NT', '近几年#NT',
           '前一阵子#NT', '过季#NT']

PAST_NR = ['刚过去#NR']

PAST_VV = ['昨天晚上#VV', '昨天上午#VV', '过去#VV 的#DEC', '去年同期#VV', '去年底#VV']

PAST_PHRASES = PAST_AD + PAST_CD + PAST_M + PAST_NN + PAST_NR + PAST_NT + PAST_VV


########################################################################


FUTURE_NT = ['今后#NT', '未来#NT', '将来#NT', '后来#NT', '此后#NT', '之后#NT', '日后#NT', '其后#NT', '稍后#NT', '晚些时候#NT',
             '次年#NT', '明年#NT', '来年#NT', '翌年#NT', '下年#NT',
             '下月初#NT', '月后#NT',
             '下周#NT',
             '明天#NT', '次日#NT', '后天#NT', '明后天#NT', '翌日#NT', '明晚#NT', '明早#NT']

FUTURE_PREFIX = ['后#DT', '后#JJ', '下#DT']

FUTURE_SUFFIX = ['后#LC']

FUTURE_AD = ['此后#AD', '稍后#AD', '而后#AD', '日后#AD', '事后#AD', '在此之后#AD',
             '不久以后#AD', '之后#AD', '即将#AD', '将#AD', '将会#AD', '将要#AD', '后来#AD', '以后#AD']

FUTURE_NN = ['会后#NN', '下周#NN', '下个月#NN', '将会#NN']

FUTURE_NT = ['今后#NT', '日后#NT', '将来#NT']

FUTURE_PHRASES = FUTURE_AD + FUTURE_NN + FUTURE_NT

########################################################################

def calculate_index(sen_tuple, event_index):
    event_list = []
    full_list = []
    tuple_index = 0
    event_set = set()  # build a set to filter the possibly duplicate clauses
    non_event_clause = []
    for i in sen_tuple:
        tuple_index += 1
        full_list.append(i + (tuple_index, ))
    clauses = [list(group) for k, group in itertools.groupby(full_list, lambda x: x[0] == '，') if not k]
    # use the comma as the delimiter, and use itertools.groupby to chain the tuples

    for clause in clauses:
        for item in clause:
            for tuple_index in event_index:
                if tuple_index == item[2]:
                    event_set.update(clause)

    event_clause = sorted(event_set, key=itemgetter(2))
    event_clause_index = map(int, ['%d' % i for k, v, i in event_clause])

    non_event_list = ['%s %s %s' % (k, v, i) for k, v, i in full_list if i not in event_clause_index]
    for i in non_event_list:
        non_event_clause.append(tuple(i.split(' ')))

    # print 'event clause:', ' '.join('(\'%s\', \'%s\', %s),' % (k, v, i) for k, v, i in event_clause)
    # print 'non event clause:', ' '.join('(\'%s\', \'%s\', %s),' % (k, v, i) for k, v, i in non_event_clause)
    #
    # for i in event_index:
    #     event_list.append([x for x in sen_tuple[i]])
    # print 'event list:', ' '.join('%s %s;' % (k, v,) for k, v in event_list)
    # print ' '.join('%s#%s %s;' % (k, v, i) for k, v, i in full_list)

    return event_clause, non_event_clause


########################################################################


cn_year = re.compile('(\d+)年')
cn_month = re.compile('(\d+)月')
cn_day = re.compile('(\d+)日')
current_y = int(str(datetime.now()).split(' ')[0].split('-')[0])
current_m = int(str(datetime.now()).split(' ')[0].split('-')[1])
current_d = int(str(datetime.now()).split(' ')[0].split('-')[2])


def detect_date(clause_tuples, ref_yr=current_y):
    '''
    This function only deals with the expressions starting with explicit year.
    '''

    state = 0
    matched_list = []
    status = ''

    for word, tag, index in clause_tuples:
        if status == '':

            y = cn_year.match(word)
            if y:
                matched_y = int(y.group(1))
                if matched_y < 100:  # if the year only contains two digits
                    m_year = matched_y
                    min_year = m_year + 1900
                    max_year = m_year + 2000
                    if max_year - ref_yr > ref_yr - min_year:
                        matched_y = m_year + 1900  # convert the year to 4 digits
                    else:
                        matched_y = m_year + 2000

                if matched_y > 1900:
                    matched_list.append((word, tag, index))
                    state = current_y - matched_y
                    if state == 0:
                        status = 'HoldingYear'

        elif status == 'HoldingYear':
            y = cn_month.match(word)
            if y:
                matched_list.append((word, tag, index))
                matched_m = int(y.group(1))
                state = current_m - matched_m
                if state == 0:
                    status = 'HoldingMonth'
            else:
                status = 'CURRENT'

        elif status == 'HoldingMonth':
            y = cn_day.match(word)
            if y:
                matched_list.append((word, tag, index))
                matched_d = int(y.group(1))
                state = current_d - matched_d
                if state == 0:
                    status = 'CURRENT'
            else:
                status = 'CURRENT'

        else:
            status = ''

    if state > 0:
        status = 'PAST'
    elif state < 0:
        status = 'FUTURE'

    print status, 'tuple:', ''.join('%s, %s, %s; ' % (k, v, i) for k, v, i in matched_list)
    return status, matched_list


########################################################################


PRESENT_NT = ['目前#NT', '当前#NT', '现在#NT', '当时#NT', '如今#NT', '当代#NT', '现时#NT', '此刻#NT', '同时#NT', '现阶段#NT',
              '此时#NT', '当今#NT', '当季#NT', '当下#NT', '眼下#NT', '时下#NT', '今时#NT', '现#NT', '现如今#NT', '此时#NT', '现今#NT',
              '同年#NT', '今夏#NT', '本季#NT', '当季#NT',
              '本月#NT', '当月#NT', '同月#NT', '该月份#NT', '当月份#NT',
              '本周#NT', '当周#NT', '本周末#NT',
              '今晚#NT', '今日#NT', '今天#NT', '当天#NT', '今#NT', '即日#NT', '今早#NT', '当日#NT', '当晚#NT', '今晨#NT']
PRESENT_NN = ['当下#NN']



CONDITION_CONJ = ['如果#CS', '只要#CS', '一旦#CS', '若#CS', '如果说#CS', '除非#CS', '假如#CS', '要是#CS',
                  '倘若#CS', '只有#CS', '若是#CS', '如#CS', '假如说#CS', '万一#CS', '假使#CS', '若说#CS']


########################################################################


def detect_time(clause, temp_phrases=PAST_PHRASES, temp_suffix=PAST_SUFFIX, temp_prefix=PAST_PREFIX, state='PAST'):
    status, result = '', []

    for tup in clause:
        token, pos, index = tup[0], tup[1], tup[2]
        possed_token = token + '#' + pos

        if status == '':
            for item in temp_phrases:
                if item in possed_token:
                    status = 'PE'; result.append(tup)
                    break
            else:
                for item in TIME_MORPHEMES:
                    if item in possed_token:
                        status = 'TW'
                        break
                    else:
                        for item in temp_prefix:
                            if item in possed_token:
                                status = 'TP'
                                break
                            else:
                                status = ''

        elif status == 'TW':
            for item in temp_suffix:
                if item in possed_token:
                    status = 'TWTS'; result.append(tup)
                    break
                else:
                    for item in temp_prefix:
                        if item in possed_token:
                            status = 'TP'
                            break
                        else:
                            status = ''

        elif status == 'TP':
            for item in TIME_MORPHEMES:
                if item in possed_token:
                    status = 'TPTW'; result.append(tup)
                    break
                else:
                    status = ''

    if status == 'PE' or 'TWTS' or 'TPTW':
        status = state
        print status, ' '.join('%s %s %s' % (k, v, i) for k, v, i in result)
        return result
    else:
        return None


########################################################################


def detect_time_in_sen(sen, temp_phrases=FUTURE_PHRASES, temp_suffix=FUTURE_SUFFIX, temp_prefix=FUTURE_PREFIX):
    status, result = '', []
    for word in sen.split(' '):
        if status == '':
            for item in temp_phrases:
                if item in word:
                    result.append(('TEE   == ' + word + ' ==   ' + sen))
                    status = 'TEE'
                    break
            else:
                status = 'NTE'

            if status == 'NTE':
                for item in TIME_MORPHEMES:
                    if item in word:
                        status = 'TW'
                        word_ = item
                        break
                    else:
                        status = 'NTWTS'
        elif status == 'TW':
            for item in temp_suffix:
                if item in word:
                    result.append(('SUX   == ' + word_ + ' ' + word + ' ==   ' + sen))
                    status = 'SUX'
                    break
                else:
                    status = 'NTWTS'

        if status == 'NTWTS':
            for item in temp_prefix:
                if item in word:
                    status = 'TP'
                    word_ = word
                    break
                else:
                    status = ''
        elif status == 'TP':
            for item in TIME_MORPHEMES:
                if item in word:
                    result.append(('PRX   == ' + word_ + ' ' + word + ' ==   ' + sen))
                    status = 'PRX'
                    break
                else:
                    status = ''
    if status == 'TEE' or 'SUX' or 'PRX':
        return result
    else:
        return None


########################################################################





# def SVO(li):  # S- V -O
#         state = ''
#         result = None
#         for pos, i, word in li:
#             if state == '':
#                 ws = set(word)
#                 if ws.intersection(cores):
#                     state, result = 'S', ("".join(word), )
#             elif state == 'S':
#                 if pos == 'v':
#                     state = 'V'
#                     result += ("".join(word), )
#                 else:
#                     state = ""
#             elif state == "V":
#                 ws = set(word)
#                 if pos == 'n' and ws.intersection(cores):
#                     state = 'O'
#                     result += ("".join(word),)
#                 else:
#                     state = ""
#         if state == 'O':
#             return result
#         else:
#             return None


# def check_string(string, pattern):
#     state, result = 0, ""
#     end = len(pattern)
#     for ch in string:
#         st = pattern[state]
#         if ch == st:
#             state += 1
#             result += ch
#             if state == end:
#                 break
#         else:
#             state, result = 0, ""
#     if state == len(pattern):
#         return result
#     else:
#         return None


# def FSA(sequence, pattern):
#     '''
#     pattern 序列中每个元素是一个条件函数。
#     条件函数默认接受多个参数（单参数需要封装为tuple／list）
#     条件函数默认返回s，r两个值，s 是整数，指向状态的跳转目标， r 是处理当前item的函数。r==None 时不加入
#     '''
#     state, result = 0, ()
#     end = len(pattern)
#     for item in sequence:
#         st = pattern[state]
#         s, r = st(*item)
#         state = s
#         if r: result += (r(item),)
#         if state == 0: result = ()
#         if state == end: break
#     return result if state == end else None
#
#
# def merge_word_tuple(item):
#     p,i,w = item
#     return ''.join(w)
#
# def SVO(li, cores):
#     def _S(pos, i, word):
#         return (1 if cores.intersection(set(word)) else 0, merge_word_tuple)
#     def _V(pos, i, word):
#         return (2 if pos == 'v' else 0, merge_word_tuple)
#     def _O(pos, i, word):
#         return (3 if pos=='n' and cores.intersection(set(word)) else 0, merge_word_tuple)
#     return FSA(li, (_S, _V, _O))
# 0
#
# def SPOVO(li, cores):
#     def _S(pos, i, word):
#         return (1 if cores.intersection(set(word)) else 0, merge_word_tuple)
#     def _P(pos, i, word):
#         return (2 if pos=='p' else 0, None)
#     def _PO(pos, i, word):
#         return (3 if pos=='n' else 0, None)
#     def _V(pos, i, word):
#         return (4 if pos == 'v' else 0, merge_word_tuple)
#     def _VO(pos, i, word):
#         return (5 if pos == 'n' else 0, merge_word_tuple)
#     return FSA(li, (_S, _P, _PO, _V, _VO))


########################################################

if __name__ == '__main__':
    gc.disable()
    a = now_str(hide_microseconds=False)

    result = []
    # raw_data = open('/Users/acepor/work/time/data/possed_news.txt', 'r')
    raw_data = open('/Users/acepor/work/time/data/stf_result.txt', 'r')

    # result = (past_identify(line) for line in raw_data)
    # for i in result:
    #     if i is not None:
    #         print i

    for line in raw_data:
        r = detect_time_in_sen(line)
        for i in r:
            print i

    SEN1 = [('3月', 'NT'), ('7日', 'NT'), ('报道', 'VV'), ('智能', 'NN'), ('手表', 'NN'), ('Apple', 'NN'), ('Watch', 'NN'), ('代表', 'VV'),
       ('着', 'AS'), ('2007年', 'NT'), ('苹果', 'NN'), ('推出', 'VV'), ('智能', 'NN'), ('手机', 'NN'), ('iPhone', 'NN'), ('以来', 'LC'),
       ('最大', 'JJ'), ('赌注', 'NN'), ('，', 'PU'), ('一旦', 'CS'), ('苹果', 'NN'), ('于', 'P'), ('3月', 'NT'), ('9日', 'NT'),
       ('正式', 'AD'), ('公布', 'VV'), ('Apple', 'NN'), ('Watch', 'NN'), ('的', 'DEG'), ('定价', 'NN'), ('等', 'ETC'), ('细节', 'NN'),
       ('后', 'LC'), ('，', 'PU'), ('苹果', 'NN'), ('将', 'AD'), ('变成', 'VV'), ('完全', 'AD'), ('不同', 'VA'), ('的', 'DEC'),
       ('公司', 'NN'), ('。', 'PU')]

    INDEX1 = [20, 21, 22, 23, 25, 26, 27, 28, 29]

    SEN2 = [('根据', 'P'), ('2014年', 'NT'), ('Reuters', 'NR'), ('Institute', 'NN'), ('调查', 'NN'), ('，', 'PU'), ('在', 'P'),
            ('西班牙', 'NR'), ('、', 'PU'), ('意大利', 'NR'), ('和', 'CC'), ('巴西', 'NR'), ('，', 'PU'), ('很多', 'CD'), ('WhatsApp', 'NR'),
            ('用户', 'NN'), ('通过', 'P'), ('这', 'DT'), ('款', 'M'), ('应用', 'NN'), ('来', 'MSP'), ('获取', 'VV'), ('新闻', 'NN'),
            ('资讯', 'NN'), ('。', 'PU')]

    INDEX2 = [13, 14, 15, 16, 18, 19, 21, 22, 23]

    '根据2014年Reuters Institute调查，在西班牙、意大利和巴西，很多WhatsApp用户通过这款应用来获取新闻资讯。'

    '很多 WhatsApp 用户 通 过 款 应用 获取 新闻 资讯'

    SEN3 = [('在', 'P'), ('2015年', 'NT'), ('的', 'DEG'), ('一', 'CD'), ('轮', 'M'), ('融资', 'NN'), ('中', 'LC'), ('，', 'PU'),
            ('Etsy', 'NR'), ('的', 'DEG'), ('估值', 'NN'), ('已', 'AD'), ('突破', 'VV'), ('6亿', 'CD'), ('美元', 'M'), ('。', 'PU')]

    INDEX3 = [8, 10, 12, 13, 14]

    'Etsy 估值 突破 6 亿 美元'

    SEN4 = [('没有', 'AD'), ('出现', 'VV'), ('预料', 'NN'), ('中', 'LC'), ('的', 'DEG'), ('问题', 'NN'), ('对于', 'P'), ('苹果', 'NN'),
            ('来说', 'LC'), ('当然', 'AD'), ('是', 'VC'), ('好事', 'NN'), ('，', 'PU'), ('因为', 'P'), ('iAd', 'NN'), ('从来', 'AD'),
            ('都', 'AD'), ('没', 'AD'), ('能', 'VV'), ('追上', 'VV'), ('谷歌', 'NR'), ('的', 'DEG'), ('广告', 'NN'), ('业务', 'NN'), ('。', 'PU')]

    INDEX4 = [14, 18, 19, 20, 21, 22, 23]

    '没有出现预料中的问题对于苹果来说当然是好事，因为iAd从来都没能追上谷歌的广告业务。'
    'iAd 能 追上 谷歌 的 广告 业务'

    SEN5 = [('目前', 'NT'), ('，', 'PU'), ('特斯拉', 'NR'), ('电动', 'JJ'), ('汽车', 'NN'), ('所需', 'NN'), ('电池', 'NN'), ('在', 'P'),
            ('美国', 'NR'), ('加州', 'NR'), ('弗里蒙特', 'NR'), ('的', 'DEG'), ('工厂', 'NN'), ('生产', 'NN'), ('，', 'PU'), ('但', 'AD'),
            ('这', 'DT'), ('家', 'M'), ('工厂', 'NN'), ('无法', 'AD'), ('满足', 'VV'), ('特斯拉', 'NR'), ('未来', 'NT'), ('的', 'DEG'),
            ('生产', 'NN'), ('需求', 'NN'), ('。', 'PU'), ('昨天上午', 'VV')]

    INDEX5 = [17, 18, 20, 21, 22, 23, 24, 25]

    '目前，特斯拉电动汽车所需电池在美国加州弗里蒙特的工厂生产，但这家工厂无法满足特斯拉未来的生产需求。'
    '家 工厂 满足 特斯拉 未来 的 生产 需求'

    # e, ne = calculate_index(SEN3, INDEX3)
    # r1 = detect_time(e)
    # r2 = detect_time(ne)

    b = now_str(hide_microseconds=False)
    print a,
    print b
