# _*_ coding: utf-8 _*_

__author__ = 'acepor'

import gc
from my_tools import now_str
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
           '前半生#NT', '近期#NT', '近期内#NT', '近来#NT', '上世纪#NT', '节前#NT', '上季#NT', '前段时间#NT', '前不久#NT',
           '近几年#NT', '前一阵子#NT', '过季#NT']

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


def recover_index(sen_list, result_tup):
    comma_index, event_clause, non_event_clause = [0], [], []
    full_list = [item + (ind,) for ind, item in enumerate(sen_list)]

    for item, tag, index in full_list:
        if item[0] == u'\uff0c':  # u'\uff0c' stands for the full-width comma
            comma_index.append(index)
    comma_index.extend([full_list[-1][2]])  # capture all commas in the sentence

    i, j = 0, 0
    result, result_size = [], 0
    while i < len(sen_list):
        item = sen_list[i][0]
        if item == result_tup[j:j+1][0]:
            j += 1
            result.append((sen_list[i][0], i))  # extract the matched tuple
            result_size += 1
        else:
            result, result_size, j = [], 0, 0
        i += 1
        if result_size == len(result_tup): break

    min_comma, max_comma = result[0][1], result[-1][1]  # capture the boundaries of the event tuple

    k = 0
    while k < len(comma_index)-1:
        left_comma, right_comma = comma_index[k], comma_index[k+1]  # set the boundaries according to the comma list
        if left_comma <= min_comma <= right_comma:
            if full_list[left_comma-1] == u'\uff0c':
                event_clause = full_list[left_comma+1: right_comma]  # exclude the left comma
                non_event_clause = full_list[0:left_comma+1]
            else:
                event_clause = full_list[left_comma+1: right_comma]
                non_event_clause = full_list[0:left_comma]
            non_event_clause.extend(full_list[right_comma+1:])
            break
        k += 1

    return event_clause, non_event_clause


########################################################################


cn_date = re.compile(u'((\d{2,4})年)?((\d{1,2})月)?((\d{1,2})日)?')
current = str(datetime.now()).split(' ')[0].split('-')
current_y, current_m, current_d = int(current[0]), int(current[1]), int(current[2])


def detect_date(clause_tuples, ref_yr=current_y, clause_type='e'):
    '''
    This function only deals with the expressions starting with explicit temporal expressions.
    '''

    state, pattern, status, tokens = 0, '', '', ''
    for token, pos, index in clause_tuples:
        tokens += token

    # matched_date = cn_date.search(tokens)
    # _, matched_y, _, matched_m, _, matched_d = matched_date.groups()

    for _, matched_y, _, matched_m, _, matched_d in cn_date.findall(tokens):

        matched_d = int(matched_d) if matched_d else None # convert day
        matched_m = int(matched_m) if matched_m else None # convert month
        matched_y = int(matched_y) if matched_y else None # convert year

        if matched_y and matched_y < 100:
            m_year = matched_y
            min_year, max_year = m_year + 1900, m_year + 2000
            matched_y = min_year if max_year - ref_yr > ref_yr - min_year else max_year

        if matched_y and matched_m is None and matched_d is None:
            pattern = str(matched_y) + '年'
            state = current_y - matched_y

        elif matched_y and matched_m and matched_d is None:
            pattern = str(matched_y) + '年' + str(matched_m) + '月'
            if current_y - matched_y == 0:
                state = current_m - matched_m
            else:
                state = current_y - matched_y

        elif matched_y and matched_m and matched_d:
            pattern = str(matched_y) + '年' + str(matched_m) + '月' + str(matched_d) + '日'
            if current_y - matched_y == 0:
                if current_m - matched_m == 0:
                    state = current_d - matched_d
                else:
                    state = current_m - matched_m
            else:
                state = current_y - matched_y

        elif matched_y is None and matched_m and matched_d is None:
            pattern = str(matched_m) + '月'
            state = current_m - matched_m

        elif matched_y is None and matched_m and matched_d:
            pattern = str(matched_m) + '月' + str(matched_d) + '日'
            if current_m - matched_m == 0:
                state = current_d - matched_d
            else:
                state = current_m - matched_m

        elif matched_y is None and matched_m is None and matched_d:
            pattern = str(matched_d) + '日'
            state = current_d - matched_d

    if state > 0:
        status = -1
    elif state < 0:
        status = 1

    if clause_type == 'ne:':
        status = status /2

    return (status, pattern, u'NT', 0) if status == 1 or status == -1 else None


########################################################################

PAST_PARAS = (PAST_PHRASES, PAST_SUFFIX, PAST_PREFIX, -1)
FUTURE_PARAS = (FUTURE_PHRASES, FUTURE_SUFFIX, FUTURE_PREFIX, 1)

def detect_time(clause, paras = PAST_PARAS):
    t_phrases, prefix, suffix, state = paras
    status, matched_tuple = '', ()
    possed_tokens = []

    for token, pos, index in clause:
        possed_token = token + '#' + pos
        possed_tokens.append(possed_token.encode('utf-8'))

        if status == '':
            for item in possed_tokens:
                if item in t_phrases:
                    status, matched_tuple = 'PE', (token, pos, index)
                    break
                elif item in TIME_MORPHEMES:
                    status = 'TW'
                    break
                elif item in prefix:
                    status = 'TP'
                    break
                else:
                    status = ''

        elif status == 'TW':
            for item in possed_tokens:
                if item in suffix:
                    status, matched_tuple = 'TWTS', (token, pos, index)
                    break
                else:
                    status = ''

        elif status == 'TP':
            for item in possed_tokens:
                if item in TIME_MORPHEMES:
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


def detect_overall(clause_tuples, type='e'):

    status, matched_tuple, result = '', (), []

    result.append(detect_date(clause_tuples, ref_yr=current_y, clause_type=type))
    result.append(detect_time(clause_tuples, paras=PAST_PARAS))
    result.append(detect_time(clause_tuples, paras=FUTURE_PARAS))
    # 1 indicates a future event，  -1 indicates a past event

    return set([a for a in result if a is not None if len(a) > 1])


########################################################################


def evaluate_status(time_set, event_tuple, type='e'):
    time_score, distance, pattern_list = 0, 0, []
    index_list = [int(i[2]) for i in event_tuple]  # each tuple has three elements
    b_min, b_max = min(index_list)-1, max(index_list)+1
    for j in time_set:
        if b_min < int(j[3]) < b_max:  # each tuple has four elements
            time_score += j[0]
            distance = 0
        elif time_score == 0 and int(j[3]) < b_min:
            # If the event clause does not contain any expression, or the expressions are controversial.
            # Only evaluate the clause appeared in front of the event clause.
            time_score += j[0] / 2.0
            distance += (b_min - int(j[3]))
        else:
            time_score = 0

    for i in [b for (a, b, c, d) in time_set]:
        pattern_list.append(i) if isinstance(i, str) else pattern_list.append(i.encode('utf-8'))

    return time_score, distance, pattern_list


########################################################################


if __name__ == '__main__':
    gc.disable()
    a = now_str(hide_microseconds=False)

    # data = [[[(u'Apple', u'NR'), (u'Watch', u'NN'), (u'\u53d1\u5e03', u'VV'), (u'\u540e', u'LC'), (u'\u82f9\u679c', u'NN'), (u'\u5c06', u'AD'), (u'\u5b8c\u5168', u'AD'), (u'\u4e0d\u540c', u'JJ'), (u'BI', u'NN'), (u'\u4e2d\u6587', u'NN'), (u'\u7ad9', u'VV'), (u'3\u6708', u'NT'), (u'7\u65e5', u'NT'), (u'\u62a5\u9053', u'VV'), (u'\u667a\u80fd', u'NN'), (u'\u624b\u8868', u'NN'), (u'Apple', u'NN'), (u'Watch', u'NN'), (u'\u4ee3\u8868', u'VV'), (u'\u7740', u'AS'), (u'2007\u5e74', u'NT'), (u'\u82f9\u679c', u'NN'), (u'\u63a8\u51fa', u'VV'), (u'\u667a\u80fd', u'NN'), (u'\u624b\u673a', u'NN'), (u'iPhone', u'NN'), (u'\u4ee5\u6765', u'LC'), (u'\u6700\u5927', u'JJ'), (u'\u8d4c\u6ce8', u'NN'), (u'\uff0c', u'PU'), (u'\u4e00\u65e6', u'CS'), (u'\u82f9\u679c', u'NN'), (u'\u4e8e', u'P'), (u'3\u6708', u'NT'), (u'9\u65e5', u'NT'), (u'\u6b63\u5f0f', u'AD'), (u'\u516c\u5e03', u'VV'), (u'Apple', u'NN'), (u'Watch', u'NN'), (u'\u7684', u'DEG'), (u'\u5b9a\u4ef7', u'NN'), (u'\u7b49', u'ETC'), (u'\u7ec6\u8282', u'NN'), (u'\u540e', u'LC'), (u'\uff0c', u'PU'), (u'\u82f9\u679c', u'NN'), (u'\u5c06', u'AD'), (u'\u53d8\u6210', u'VV'), (u'\u5b8c\u5168', u'AD'), (u'\u4e0d\u540c', u'VA'), (u'\u7684', u'DEC'), (u'\u516c\u53f8', u'NN'), (u'\u3002', u'PU')],
    #         (u'Apple', u'Watch', u'\u53d1\u5e03', u'\u540e', u'\u82f9\u679c', u'\u5c06', u'\u5b8c\u5168', u'\u4e0d\u540c', u'BI', u'\u4e2d\u6587', u'\u7ad9', u'3\u6708', u'7\u65e5', u'\u62a5\u9053', u'\u667a\u80fd', u'\u624b\u8868', u'Apple', u'Watch', u'\u4ee3\u8868', u'\u7740', u'2007\u5e74', u'\u82f9\u679c', u'\u63a8\u51fa', u'\u667a\u80fd', u'\u624b\u673a', u'iPhone', u'\u4ee5\u6765', u'\u6700\u5927', u'\u8d4c\u6ce8')],
    #         [[(u'\u4ee5\u4e0b', u'AD'), (u'\u56db', u'CD'), (u'\u5927', u'JJ'), (u'\u56e0\u7d20', u'NN'),
    #         (u'\u4e5f', u'AD'), (u'\u8868\u660e', u'VV'), (u'\u5e93\u514b', u'NR'), (u'\u4ecd', u'AD'),
    #          (u'\u662f', u'VC'), (u'\u5f15\u9886', u'VV'), (u'\u82f9\u679c', u'NN'), (u'\u8d70\u5411', u'VV'),
    #          (u'\u672a\u6765', u'NT'), (u'\u7684', u'DEG'), (u'\u5408\u9002', u'JJ'), (u'\u4eba\u9009', u'NN'),
    #          (u'\u3002', u'PU')],
    #             (u'\u5e93\u514b', u'\u4ecd', u'\u662f', u'\u5f15\u9886', u'\u82f9\u679c', u'\u8d70\u5411',
    #              u'\u672a\u6765', u'\u7684', u'\u5408\u9002', u'\u4eba\u9009')],
    #             [[(u'\u5f53\u7136', u'AD'), (u'\uff0c', u'PU'), (u'\u5e93\u514b', u'NR'), (u'\u4e5f', u'AD'),
    #              (u'\u6ca1\u6709', u'AD'), (u'\u4f4e\u4f30', u'VV'), (u'\u82f9\u679c', u'NN'), (u'\u7684', u'DEC'),
    #              (u'\u672a\u6765', u'NT'), (u'\u3002', u'PU')],
    #             (u'\u5e93\u514b', u'\u4e5f', u'\u6ca1\u6709', u'\u4f4e\u4f30', u'\u82f9\u679c', u'\u7684', u'\u672a\u6765')],
    #             [[(u'\u9c8d\u5c14\u9ed8', u'NR'), (u'\u9000\u4f11', u'VV'), (u'\u6d88\u606f', u'NN'), (u'\u523a\u6fc0', u'VV'),
    #              (u'\u5fae\u8f6f', u'NR'), (u'\u80a1\u4ef7', u'NN'), (u'\u6da8', u'VV'), (u'7.29%', u'CD'), (u'\u53d7', u'LB'),
    #              (u'\u9c8d\u5c14', u'NR'), (u'\u9ed8', u'NT'), (u'\u4e00', u'CD'), (u'\u5e74', u'M'), (u'\u5185', u'LC'),
    #              (u'\u5c06', u'BA'), (u'\u9000\u4f11', u'VV'), (u'\u7684', u'DEC'), (u'\u6d88\u606f', u'NN'),
    #              (u'\u523a\u6fc0', u'NN'), (u'\uff0c', u'PU'), (u'\u5fae\u8f6f', u'NR'), (u'\u80a1\u4ef7', u'NN'),
    #              (u'\u5468\u4e94', u'NT'), (u'\u5927', u'AD'), (u'\u6da8', u'VV'), (u'7.29%', u'CD'), (u'\uff0c', u'PU'),
    #              (u'\u62a5', u'VV'), (u'\u6536\u4e8e', u'VV'), (u'34.75', u'CD'), (u'\u7f8e\u5143', u'M'), (u'\u3002', u'PU')],
    #             (u'\u5fae\u8f6f', u'\u80a1\u4ef7', u'\u6da8', u'7.29%', u'\u53d7', u'\u9c8d\u5c14', u'\u9ed8', u'\u4e00',
    #              u'\u5e74', u'\u5185', u'\u5c06', u'\u9000\u4f11', u'\u7684', u'\u6d88\u606f', u'\u523a\u6fc0')]]

    data = read_pickle('/Users/acepor/work/time/data/events_result.pkl')
    outf = open('/Users/acepor/work/time/data/output_full8.txt','w')
    for line in data:
        sen, event = line
        # print 'sen', ' '.join([a for a, b in sen])
        # print  'event', ' '.join(event)
        e, ne = recover_index(sen, event)
        # print 'e', ' '.join([a for a, b, c in e])
        # print 'ne', ' '.join([a for a, b, c in ne])
        # print e

        re_e = detect_overall(e, 'e')
        re_ne = detect_overall(ne, 'ne')
        time_score1, distance1, p1 = evaluate_status(re_e, e, 'e')
        time_score2, distance2, p2 = evaluate_status(re_ne, e, 'ne')

        total_score = time_score1 + time_score2

        s4 = str(total_score) + ' ' + str(time_score1) + ' ' + str(time_score2)  + '\n'
        ss = 'original: ' + ' '.join(''.join(a) for a, b in sen) + '\n\n'
        s1 = 'score ' + str(total_score) + ' e: ' + ', '.join(p1) + ' ne: ' + ', '.join(p2) + '\n'
        s2 = ' '.join(k for k in event) + '\n'
        # print s1; print s2; print s4; print ss

        outf.write(s1)
        outf.write(s4)
        outf.write(s2.encode('utf-8'))
        outf.write(ss.encode('utf-8'))
    outf.flush()
    outf.close()