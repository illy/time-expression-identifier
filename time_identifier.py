# _*_ coding: utf-8 _*_

__author__ = 'acepor'

import gc
import itertools
from my_tools import now_str
from operator import itemgetter
from datetime import datetime
import re
from pickle import load


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

PAST_NT = ['之前#NT', '从前#NT', '以往#NT', '最初#NT', '当初#NT', '不久#NT', '先前#NT', '此前#NT', '以前#NT', '最近#NT',
           '当初#AD', '以往#NT',
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

PRESENT_NT = ['目前#NT', '当前#NT', '现在#NT', '如今#NT', '现时#NT', '此刻#NT', '同时#NT', '现阶段#NT', '现时#NT',
              '此时#NT', '当今#NT', '当下#NT', '眼下#NT', '时下#NT', '今时#NT', '现#NT', '此时#NT', '现今#NT',
              '同年#NT', '今夏#NT', '本季#NT', '当季#NT',
              '本月#NT', '当月#NT', '同月#NT', '当月份#NT',
              '本周#NT', '当周#NT', '本周末#NT',
              '今晚#NT', '今日#NT', '今天#NT', '当天#NT', '今#NT', '即日#NT', '今早#NT', '当日#NT', '当晚#NT', '今晨#NT']
PRESENT_NN = ['当下#NN', '现阶段#NN', '目前#NN']

PRESENT_AD = ['正在#AD', '正#AD']

PAST_PHRASES = PAST_AD + PAST_CD + PAST_M + PAST_NN + PAST_NR + PAST_NT + PAST_VV + PRESENT_NT + PRESENT_NN + PRESENT_AD


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

FUTURE_PHRASES = FUTURE_AD + FUTURE_NN + FUTURE_NT


########################################################################


CONDITION_CONJ = ['如果#CS', '只要#CS', '一旦#CS', '若#CS', '如果说#CS', '除非#CS', '假如#CS', '要是#CS',
                  '倘若#CS', '只有#CS', '若是#CS', '如#CS', '假如说#CS', '万一#CS', '假使#CS', '若说#CS']


########################################################################


def read_pickle(filename):
    data_list = []
    data = load(open(filename, 'r'))
    for line in data:
        data_list.append(line)
    return data_list


def calculate_index(sen_tuple, event_index):
    full_list, non_event_clause = [], []
    tuple_index, event_set = 0, set()  # build a set to filter the possibly duplicated clauses
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

    event_clause = sorted(event_set, key=itemgetter(2))  # the generated set might lose the order
    event_clause_index = map(int, ['%d' % i for k, v, i in event_clause])  # generate an index of th event clause

    non_event_list = ['%s %s %s' % (k, v, i) for k, v, i in full_list if i not in event_clause_index]
    for i in non_event_list:
        non_event_clause.append(tuple(i.split(' ')))
    return event_clause, non_event_clause


def recover_index(sen_list, result_tup):
    full_sen, non_event_clause = [], []
    tuple_index, event_set = 0, set()  # build a set to filter the possibly duplicated clauses
    for i in sen_list:
        tuple_index += 1
        full_sen.append(i + (tuple_index, ))
    clauses = [list(group) for k, group in itertools.groupby(full_sen, lambda x: x[0][0] == u'\uff0c') if not k]

    for clause in clauses:
        for word in result_tup:
            for item in clause:
                if word == item[0][0]:
                    event_set.update((item,))

    event_clause = sorted(event_set, key=itemgetter(2))
    non_event_list = [(k, v, i) for k, v, i in full_sen if k[0] not in result_tup]
    non_event_clause = sorted(non_event_list, key=itemgetter(2))

    return event_clause, non_event_clause


########################################################################


cn_year = re.compile(u'(\d+)年')
cn_month = re.compile(u'(\d+)月')
cn_day = re.compile(u'(\d+)日')
current_y = int(str(datetime.now()).split(' ')[0].split('-')[0])
current_m = int(str(datetime.now()).split(' ')[0].split('-')[1])
current_d = int(str(datetime.now()).split(' ')[0].split('-')[2])


def detect_date(clause_tuples, ref_yr=current_y):
    '''
    This function only deals with the expressions starting with explicit temporal expressions.
    '''

    state, matched_tuple, status = 0, (), ''

    for token, pos, index in clause_tuples:
        token = token[0]
        if status == '':
            matched_time = cn_year.match(token)
            if matched_time:
                matched_y = int(matched_time.group(1))
                if matched_y < 100:  # if the year only contains two digits
                    m_year = matched_y
                    min_year = m_year + 1900
                    max_year = m_year + 2000
                    if max_year - ref_yr > ref_yr - min_year:
                        matched_y = m_year + 1900  # convert the year to 4 digits
                    else:
                        matched_y = m_year + 2000

                if matched_y > 1900:
                    matched_tuple = (token, pos, index)
                    state = current_y - matched_y
                    if state == 0:
                        status = 'HoldingYear'

        elif status == 'HoldingYear':
            matched_time = cn_month.match(token)
            if matched_time:
                matched_tuple = (token, pos, index)
                matched_m = int(matched_time.group(1))
                state = current_m - matched_m
                if state == 0:
                    status = 'HoldingMonth'
            else:
                status = 'CURRENT'

        elif status == 'HoldingMonth':
            matched_time = cn_day.match(token)
            if matched_time:
                matched_tuple = (token, pos, index)
                matched_d = int(matched_time.group(1))
                state = current_d - matched_d
                if state == 0:
                    status = 'CURRENT'
            else:
                status = 'CURRENT'

        else:
            status = ''

    if state > 0:
        status = -1
    elif state < 0:
        status = 1
    # print status, matched_tuple

    if status == 'HoldingMonth' or status == 'HoldingYear' or status == 'CURRENT':
        status = -1

    return (status, ) + matched_tuple if status == 1 or status == -1 else None


########################################################################


def detect_time(clause, t_phrases=PAST_PHRASES, suffix=PAST_SUFFIX, prefix=PAST_PREFIX, state=0):
    status, matched_tuple = '', ()

    for token, pos, index in clause:
        token, pos = token[0].encode('utf-8'), pos.encode('utf-8')
        possed_token = token + '#' + pos

        if status == '':
            for item in t_phrases:
                if item in possed_token:
                    status, matched_tuple = 'PE', (token, pos, index)
                    break
            else:
                for item in TIME_MORPHEMES:
                    if item in possed_token:
                        status = 'TW'
                        break
                    else:
                        for item in prefix:
                            if item in possed_token:
                                status = 'TP'
                                break
                            else:
                                status = ''

        elif status == 'TW':
            for item in suffix:
                if item in possed_token:
                    status, matched_tuple = 'TWTS', (token, pos, index)
                    break
                else:
                    for item in prefix:
                        if item in possed_token:
                            status = 'TP'
                            break
                        else:
                            status = ''

        elif status == 'TP':
            for item in TIME_MORPHEMES:
                if item in possed_token:
                    status, matched_tuple = 'TPTW', (token, pos, index)
                    break
                else:
                    status = ''

    if status == 'PE' or status == 'TWTS' or status == 'TPTW':
        status = state
        return (status, ) + matched_tuple
    else:
        return None


########################################################################


def detect_overall(clause_tuples):

    status, matched_tuple, result = '', (), []

    result.append(detect_date(clause_tuples, ref_yr=current_y))
    # -1 indicates a past event
    result.append(detect_time(clause_tuples, t_phrases=FUTURE_PHRASES, suffix=FUTURE_PREFIX, prefix=FUTURE_SUFFIX, state=1))
    result.append(detect_time(clause_tuples, t_phrases=PAST_PHRASES, suffix=PAST_SUFFIX, prefix=PAST_PREFIX, state=-1))

    # 1 indicates a future event

    return set([a for a in result if a is not None if len(a) > 1])


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


def evaluate_status(time_set, event_tuple, type='e'):
    time_score, distance = 0, 0
    index_list = [int(i[2]) for i in event_tuple]  # each tuple has three elements
    b_min, b_max = min(index_list)-1, max(index_list)+1

    for j in time_set:
        if b_min < int(j[3]) < b_max:  # each tuple has four elements
            time_score += j[0]
        elif time_score == 0 and int(j[3]) < b_min:
            # If the event clause does not contain any expression, or the expressions are controversial.
            time_score += j[0] / 2.0
            distance += (b_min - int(j[3]))

        else:
            time_score = 0
    pattern = [b for (a, b, c, d) in time_set]

    return time_score, distance, pattern


########################################################################


if __name__ == '__main__':
    gc.disable()
    a = now_str(hide_microseconds=False)

    data = read_pickle('/Users/acepor/work/time/data/events_result')
    outf = open('/Users/acepor/work/time/data/output_full1.txt','w')
    for line in data:
        sen, event = line
        e, ne = recover_index(sen, event)
        re_e = detect_overall(e)
        re_ne = detect_overall(ne)
        time_score1, distance1, p1 = evaluate_status(re_e, e, 'e')
        time_score2, distance2, p2 = evaluate_status(re_ne, e, 'e')

        total_score = time_score1 + time_score2

        ss = 'original: ' + ' '.join(' '.join(a) for a, b in sen) + '\n\n'
        s1 = 'score ' + str(total_score)  + '\n' + ' '.join(p1)
        s2 = ' '.join(k for k in event) + '\n'

        # print [i.encode('utf-8') for i in p1 if type(i) == 'utf-8']

        outf.write(s1)
        outf.write(s2.encode('utf-8'))
        outf.write(ss.encode('utf-8'))
    outf.flush()
    outf.close()