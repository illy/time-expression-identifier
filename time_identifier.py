# _*_ coding: utf-8 _*_

__author__ = 'acepor'

import gc
import itertools
from my_tools import now_str
from operator import itemgetter

########################################################################


STF_TIME_WORDS = ['年#NT', '年#NN', '年#M', '年#AD', '年#JJ', '年内#NT',
                  '月#NT', '月#NN', '月#M', '月#CD', '月份#NN', '月份#NT', '月#AD',
                  '周#NN', '周#NT', '周#M', '周#VV', '周#JJ', '礼拜#NN', '礼拜#NT', '礼拜#M', '星期#NN', '星期#NT',
                  '日#NN', '日#NT', '日#AD','日#M', '天#NN', '天#NT', '天#AD', '天#M', '夜#AD', '夜#NT',
                  '节#NN', '节#NT', '底#NN', '底#NT', '初#NN', '初#NT',
                  '季度#NN', '季度#NT', '季#NN', '季#NT',
                  '分#M', '分钟#M', '小时#M', '片刻#AD']

PAST_PREFIX = ['前#DT', '前#LC', '前#JJ', '前面#LC', '上#DT', '上#LC', '上个#DT', '过去#NT', '过去#NN', '过去#NT 的#DEG']

PAST_SUFFIX = ['前#DT', '前#LC', '前#JJ', '前#AD',
               '底#NN', '底#NT', '初#NN', '初#NT', '初#LC', '以来#LC', '以来#AD']

PAST_AD = ['曾经#AD', '曾#AD', '最初#AD', '此前#AD', '之前#AD', '先前#AD', '刚才#AD', '往前#AD', '日前#AD', '早前#AD',
           '早日#AD', '上次#AD', '不久前#AD', '已经#AD', '已#AD', '早已#AD', '早就#AD', '以前#AD',
           '年来#AD', '前不久#AD', '不久以后#AD', '不久#AD', '前一天#AD', '去年同期#AD']

PAST_CD = ['去年底#CD']

PAST_NN = ['此前#NN', '之前#NN', '从前#NN', '先前#NN', '以往#NN', '往前#NN', '不久前#NN', '刚才#NN',
           '上年#NN', '去年#NN', '前年#NN', '上一年#NN', '年初#NN', '近些年#NN', '早年间#NN', '近三年#NN', '去年同期#NN',
           '去年初#NN', '去年底#NN', '近半年#NN', '早年#NN', '前些年#NN', '往年#NN', '年前#NN', '年来#NN',
           '上个月#NN', '上月#NN', '上月底#NN', '月前#NN', '月来#NN', '月末#NN',
           '上周#NN', '上个星期#NN', '上星期#NN', '上礼拜#NN', '上个礼拜#NN',
           '前日#NN', '前夜#NN', '天前#NN', '日前#NN', '昨夜#NN', '昨天#NN', '昨日#NN',
           '前一天#NN', '前三天#NN', '次日#NN', '昨天上午#NN', '昨天中午#NN', '昨天夜里#NN', '近些天#NN', '往日#NN', '近日#NN',
           '上次#NN', '最初#NN', '早前#NN', '生前#NN', '近期#NN', '近期内#NN', '早些时候#NN', '初期#NN', '早期#NN',
           '前半生#NN', '公元前#NN',
           '早已#NN', '早就#NN']

PAST_M = ['年来#M']

PAST_NT = ['之前#NT', '从前#NT', '以往#NT', '最初#NT', '当初#NT', '不久#NT', '先前#NT', '此前#NT', '以前#NT', '最近#NT',
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

PAST_EXPRESSIONS = PAST_AD + PAST_CD + PAST_M + PAST_NN + PAST_NR + PAST_NT + PAST_VV

PRESENT_NT = ['目前#NT', '当前#NT', '现在#NT', '当时#NT', '如今#NT', '当代#NT', '现时#NT', '此刻#NT', '同时#NT', '现阶段#NT',
              '此时#NT', '当今#NT', '当季#NT', '当下#NT', '眼下#NT', '时下#NT', '今时#NT', '现#NT', '现如今#NT', '此时#NT', '现今#NT',
              '同年#NT', '今夏#NT', '本季#NT', '当季#NT',
              '本月#NT', '当月#NT', '同月#NT', '该月份#NT', '当月份#NT',
              '本周#NT', '当周#NT', '本周末#NT',
              '今晚#NT', '今日#NT', '今天#NT', '当天#NT', '今#NT', '即日#NT', '今早#NT', '当日#NT', '当晚#NT', '今晨#NT']

FUTURE_NT = ['今后#NT', '未来#NT', '将来#NT', '后来#NT', '此后#NT', '之后#NT', '日后#NT', '其后#NT', '稍后#NT', '晚些时候#NT',
             '次年#NT', '明年#NT', '来年#NT', '翌年#NT', '下年#NT',
             '下月初#NT', '月后#NT',
             '下周#NT',
             '明天#NT', '次日#NT', '后天#NT', '明后天#NT', '翌日#NT', '明晚#NT', '明早#NT']

########################################################################

# core_words = []
# # data = open('data/qq_coretime.txt', 'r').readlines()
# data = open('/Users/acepor/work/test/stf_qq_coretime.txt', 'r').readlines()
# for line in data:
#     core_words.append(line)
#
# past_expressions = []
# # data_ = open('data/qq_past_20150414.txt', 'r').readlines()
# data_ = open('/Users/acepor/work/test/stf_qq_past.txt', 'r').readlines()
# for line in data_:
#     past_expressions.append(line)


# def clean_words(word_list):
#     for word in word_list:
#         yield word.strip()
#
#
# def compile_pattern(word_list, prefix=None, suffix=None):
#     for word in clean_words(word_list):
#         if prefix:
#             yield prefix + ' ' + word
#         if suffix:
#             yield word + ' ' + suffix


# QIAN_PREFIX = compile_pattern(word_list=core_words, prefix='前/f')
# QM_PREFIX = compile_pattern(word_list=core_words, prefix='前面/f')
# ZQ_PREFIX = compile_pattern(word_list=core_words, prefix='之前/f')
# SHANG_PREFIX = compile_pattern(word_list=core_words, prefix='上/f')

# QIAN_SUFFIX = compile_pattern(word_list=TIME_WORDS, suffix='前')
# ZQ_SUFFIX = compile_pattern(word_list=TIME_WORDS, suffix='之前/f')
# WQ_SUFFIX = compile_pattern(word_list=TIME_WORDS, prefix='往前/f')
# YQ_SUFFIX = compile_pattern(word_list=TIME_WORDS, suffix='以前/f')

# PRE_QIAN_1 = compile_pattern(word_list=STF_TIME_WORDS, prefix='前#LC')
# PRE_QIAN_2 = compile_pattern(word_list=STF_TIME_WORDS, prefix='前#JJ')
# PRE_QIAN_3 = compile_pattern(word_list=STF_TIME_WORDS, prefix='前#DT')
# PRE_QM = compile_pattern(word_list=STF_TIME_WORDS, prefix='前面#LC')
# PRE_ZQ = compile_pattern(word_list=STF_TIME_WORDS, prefix='之前#LC')
# PRE_SHANG_1 = compile_pattern(word_list=STF_TIME_WORDS, prefix='上#DT')
# PRE_SHANG_2 = compile_pattern(word_list=STF_TIME_WORDS, prefix='上#LC')
# PRE_SHANG_3 = compile_pattern(word_list=STF_TIME_WORDS, prefix='上#VV')
# PRE_GQ = compile_pattern(word_list=STF_TIME_WORDS, prefix='过去#NT')
#
# SUF_QIAN_1 = compile_pattern(word_list=STF_TIME_WORDS, suffix='前#LC')
# SUF_QIAN_2 = compile_pattern(word_list=STF_TIME_WORDS, suffix='前#JJ')
# SUF_QIAN_3 = compile_pattern(word_list=STF_TIME_WORDS, suffix='前#AD')
# SUF_ZQ = compile_pattern(word_list=STF_TIME_WORDS, suffix='之前#LC')
# SUF_YQ_1 = compile_pattern(word_list=STF_TIME_WORDS, suffix='以前#LC')
# SUF_YQ_2 = compile_pattern(word_list=STF_TIME_WORDS, suffix='以前#NT')

# PAST_PREFIXES = itertools.chain(QIAN_PREFIX, QM_PREFIX, ZQ_PREFIX, SHANG_PREFIX)
# PAST_SUFFIXES = itertools.chain(QIAN_SUFFIX, ZQ_SUFFIX, WQ_SUFFIX, YQ_SUFFIX)
# PAST_PATTERNS = itertools.chain(PAST_PREFIXES, PAST_SUFFIXES, clean_words(past_expressions))

# PAST_PREFIXES = itertools.chain(PRE_QIAN_1, PRE_QIAN_2, PRE_QIAN_3, PRE_QM, PRE_ZQ, PRE_SHANG_1, PRE_SHANG_2, PRE_SHANG_3)
# PAST_SUFFIXES = itertools.chain(SUF_QIAN_1, SUF_QIAN_2, SUF_QIAN_3, SUF_ZQ, SUF_YQ_1, SUF_YQ_2)
# PAST_PATTERNS = list(itertools.chain(PAST_PREFIXES, PAST_SUFFIXES, clean_words(past_expressions)))


# def past_identify(sen):
#     for pattern in PAST_PATTERNS:
#         if pattern in sen:
#             return pattern + ' @@   ' + sen

########################################################################


def past_fsm(sen):
    state, result = '', []
    for word in sen.split(' '):
        if state == '':
            for item in PAST_EXPRESSIONS:
                if item in word:
                    result.append(('PE   == ' + word + ' ==   ' + sen))
                    state = 'PE'
                    break
            else:
                state = 'NPE'

            if state == 'NPE':
                for item in STF_TIME_WORDS:
                    if item in word:
                        state = 'TW'
                        word_ = item
                        break
                    else:
                        state = 'NTWTS'
        elif state == 'TW':
            for item in PAST_SUFFIX:
                if item in word:
                    result.append(('TWTS   == ' + word_ + ' ' + word + ' ==   ' + sen))
                    state = 'TWTS'
                    break
                else:
                    state = 'NTWTS'

        if state == 'NTWTS':
            for item in PAST_PREFIX:
                if item in word:
                    state = 'TP'
                    word_ = word
                    break
                else:
                    state = ''
        elif state == 'TP':
            for item in STF_TIME_WORDS:
                if item in word:
                    result.append(('TPTW   == ' + word_ + ' ' + word + ' ==   ' + sen))
                    state = 'TPTW'
                    break
                else:
                    state = ''
    if state == 'PE' or 'TWTS' or 'TPTW':
        return result
    else:
        return None


########################################################################

CONDITION_CONJ = ['如果#CS', '只要#CS', '一旦#CS', '若#CS', '如果说#CS', '除非#CS', '假如#CS', '要是#CS',
                  '倘若#CS', '只有#CS', '若是#CS', '如#CS', '假如说#CS', '万一#CS', '假使#CS', '若说#CS']

'3月7日报道智能手表Apple Watch代表着2007年苹果推出智能手机iPhone以来最大赌注，一旦苹果于3月9日正式公布Apple Watch的定价等细节后，苹果将变成完全不同的公司。'

'苹果 于 3月 9日 公布 Apple Watch 的 定价'

SEN = [('3月', 'NT'), ('7日', 'NT'), ('报道', 'VV'), ('智能', 'NN'), ('手表', 'NN'), ('Apple', 'NN'), ('Watch', 'NN'), ('代表', 'VV'), ('着', 'AS'),
                ('2007年', 'NT'), ('苹果', 'NN'), ('推出', 'VV'), ('智能', 'NN'), ('手机', 'NN'), ('iPhone', 'NN'), ('以来', 'LC'), ('最大', 'JJ'), ('赌注', 'NN'),
                ('，', 'PU'), ('一旦', 'CS'), ('苹果', 'NN'), ('于', 'P'), ('3月', 'NT'), ('9日', 'NT'), ('正式', 'AD'), ('公布', 'VV'), ('Apple', 'NN'),
                ('Watch', 'NN'), ('的', 'DEG'), ('定价', 'NN'), ('等', 'ETC'), ('细节', 'NN'), ('后', 'LC'), ('，', 'PU'), ('苹果', 'NN'), ('将', 'AD'),
                ('变成', 'VV'), ('完全', 'AD'), ('不同', 'VA'), ('的', 'DEC'), ('公司', 'NN'), ('。', 'PU')]

INDEX = [20, 21, 22, 23, 25, 26, 27, 28, 29]

'根据2014年Reuters Institute调查，在西班牙、意大利和巴西，很多WhatsApp用户通过这款应用来获取新闻资讯。'

'很多 WhatsApp 用户 通 过 款 应用 获取 新闻 资讯'

SEN2 = [('根据', 'P'), ('2014年', 'NT'), ('Reuters', 'NR'), ('Institute', 'NN'), ('调查', 'NN'), ('，', 'PU'), ('在', 'P'), ('西班牙', 'NR'),
        ('、', 'PU'), ('意大利', 'NR'), ('和', 'CC'), ('巴西', 'NR'), ('，', 'PU'), ('很多', 'CD'), ('WhatsApp', 'NR'), ('用户', 'NN'), ('通过', 'P'),
        ('这', 'DT'), ('款', 'M'), ('应用', 'NN'), ('来', 'MSP'), ('获取', 'VV'), ('新闻', 'NN'), ('资讯', 'NN'), ('。', 'PU')]

'在2012年的一轮融资中，Etsy的估值已突破6亿美元。'
'Etsy 估值 突破 6 亿 美元1'


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
    #event_clause = sorted(event_set, key=lambda tup: tup[2])  # the set of tuples lost the order, so this step reorders
    event_clause_index = map(int, ['%d' % i for k, v, i in event_clause])

    non_event_list = ['%s %s %s' % (k, v, i) for k, v, i in full_list if i not in event_clause_index]
    for i in non_event_list:
        non_event_clause.append(tuple(i.split(' ')))

    print 'event clause:', ' '.join('%s#%s %s;' % (k, v, i) for k, v, i in event_clause)
    print 'non event clause:', ' '.join('%s#%s %s;' % (k, v, i) for k, v, i in non_event_clause)

    # for i in event_index:
    #     event_list.append([x for x in sen_tuple[i]])
    # print 'event list:', ' '.join('%s %s;' % (k, v,) for k, v in event_list)
    # print ' '.join('%s#%s %s;' % (k, v, i) for k, v, i in full_list)

    return event_clause, non_event_list


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

    # for i in PAST_PATTERNS:
    #     print i

    # result = []
    # raw_data = open('/Users/acepor/work/test/possed_news.txt', 'r')
    # raw_data = open('/Users/acepor/work/test/temp.txt', 'r')

    # result = (past_identify(line) for line in raw_data)
    # for i in result:
    #     if i is not None:
    #         print i

    # for line in raw_data:
    #     r = past_fsm(line)
    #     for i in r:
    #         print i


    # r = (past_fsm(line) for line in raw_data)
    # for i in r:
    #     if i != []:
    #         for j in i:
    #             print j


    SEN = [('3月', 'NT'), ('7日', 'NT'), ('报道', 'VV'), ('智能', 'NN'), ('手表', 'NN'), ('Apple', 'NN'), ('Watch', 'NN'), ('代表', 'VV'), ('着', 'AS'),
                ('2007年', 'NT'), ('苹果', 'NN'), ('推出', 'VV'), ('智能', 'NN'), ('手机', 'NN'), ('iPhone', 'NN'), ('以来', 'LC'), ('最大', 'JJ'), ('赌注', 'NN'),
                ('，', 'PU'), ('一旦', 'CS'), ('苹果', 'NN'), ('于', 'P'), ('3月', 'NT'), ('9日', 'NT'), ('正式', 'AD'), ('公布', 'VV'), ('Apple', 'NN'),
                ('Watch', 'NN'), ('的', 'DEG'), ('定价', 'NN'), ('等', 'ETC'), ('细节', 'NN'), ('后', 'LC'), ('，', 'PU'), ('苹果', 'NN'), ('将', 'AD'),
                ('变成', 'VV'), ('完全', 'AD'), ('不同', 'VA'), ('的', 'DEC'), ('公司', 'NN'), ('。', 'PU')]

    INDEX = [20, 21, 22, 23, 25, 26, 27, 28, 29]

    SEN2 = [('根据', 'P'), ('2014年', 'NT'), ('Reuters', 'NR'), ('Institute', 'NN'), ('调查', 'NN'), ('，', 'PU'), ('在', 'P'), ('西班牙', 'NR'),
            ('、', 'PU'), ('意大利', 'NR'), ('和', 'CC'), ('巴西', 'NR'), ('，', 'PU'), ('很多', 'CD'), ('WhatsApp', 'NR'), ('用户', 'NN'), ('通过', 'P'),
            ('这', 'DT'), ('款', 'M'), ('应用', 'NN'), ('来', 'MSP'), ('获取', 'VV'), ('新闻', 'NN'), ('资讯', 'NN'), ('。', 'PU')]

    INDEX2 = [13, 14, 15, 16, 18, 19, 21, 22, 23]

    SEN3 = [('在', 'P'), ('2012年', 'NT'), ('的', 'DEG'), ('一', 'CD'), ('轮', 'M'), ('融资', 'NN'), ('中', 'LC'), ('，', 'PU'), ('Etsy', 'NR'), ('的', 'DEG'),
            ('估值', 'NN'), ('已', 'AD'), ('突破', 'VV'), ('6亿', 'CD'), ('美元', 'M'), ('。', 'PU')]

    INDEX3 = [8, 10, 12, 13, 14]

    'Etsy 估值 突破 6 亿 美元'

    SEN4 = [('没有', 'AD'), ('出现', 'VV'), ('预料', 'NN'), ('中', 'LC'), ('的', 'DEG'), ('问题', 'NN'), ('对于', 'P'), ('苹果', 'NN'), ('来说', 'LC'), ('当然', 'AD'),
            ('是', 'VC'), ('好事', 'NN'), ('，', 'PU'), ('因为', 'P'), ('iAd', 'NN'), ('从来', 'AD'), ('都', 'AD'), ('没', 'AD'), ('能', 'VV'), ('追上', 'VV'),
            ('谷歌', 'NR'), ('的', 'DEG'), ('广告', 'NN'), ('业务', 'NN'), ('。', 'PU')]

    INDEX4 = [14, 18, 19, 20, 21, 22, 23]

    '没有出现预料中的问题对于苹果来说当然是好事，因为iAd从来都没能追上谷歌的广告业务。'
    'iAd 能 追上 谷歌 的 广告 业务'

    SEN5 = [('目前', 'NT'), ('，', 'PU'), ('特斯拉', 'NR'), ('电动', 'JJ'), ('汽车', 'NN'), ('所需', 'NN'), ('电池', 'NN'), ('在', 'P'), ('美国', 'NR'), ('加州', 'NR'),
            ('弗里蒙特', 'NR'), ('的', 'DEG'), ('工厂', 'NN'), ('生产', 'NN'), ('，', 'PU'), ('但', 'AD'), ('这', 'DT'), ('家', 'M'), ('工厂', 'NN'), ('无法', 'AD'),
            ('满足', 'VV'), ('特斯拉', 'NR'), ('未来', 'NT'), ('的', 'DEG'), ('生产', 'NN'), ('需求', 'NN'), ('。', 'PU')]

    INDEX5 = [17, 18, 20, 21, 22, 23, 24, 25]

    '目前，特斯拉电动汽车所需电池在美国加州弗里蒙特的工厂生产，但这家工厂无法满足特斯拉未来的生产需求。'
    '家 工厂 满足 特斯拉 未来 的 生产 需求'

    calculate_index(SEN5, INDEX5)


    b = now_str(hide_microseconds=False)
    print a
    print b