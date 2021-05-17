def create_rank_list(match_type, ranks):
    rank_str_list = list(ranks)
    if match_type + 1 <= len(rank_str_list) <= match_type + 3:
        rank_str_list[-2] += rank_str_list[-1]
        del rank_str_list[-1]
    if match_type + 1 <= len(rank_str_list) <= match_type + 2:
        rank_str_list[-3] += rank_str_list[-2]
        del rank_str_list[-2]
    if len(rank_str_list) == match_type + 1:
        rank_str_list[-4] += rank_str_list[-3]
        del rank_str_list[-3]
    rank_list = list(map(int, rank_str_list))
    return sorted(rank_list)

def create_rank_lists(match_type, multiple_ranks, rank_lists):
    never_rank_set = {1,2,3,4,5,6,7,8,9,10,11,12}
    for i in reversed(range(len(rank_lists))):
        rank_list = rank_lists[i]
        if 0 in rank_list:
            del rank_lists[i]
        else:
            never_rank_set -= set(rank_list)
    for ranks in multiple_ranks.split(' '):
        rank_list = create_rank_list(match_type, ranks)
        if not check_rank_list(match_type, rank_list, never_rank_set):
            return
        elif len(rank_lists) <= 12 // match_type:
            rank_lists.append(rank_list)
            never_rank_set -= set(rank_list)
    if len(never_rank_set) == match_type:
        rank_lists.append(sorted(list(never_rank_set)))
    return rank_lists

def check_rank_list(match_type, rank_list, never_rank_set):
    if rank_list == None:
        return False
    elif match_type != len(rank_list):
        return False
    elif not len(set(rank_list) & never_rank_set) == match_type:
        return False
    else:
        return True

def calc_score(rank_list):
    to_score_dict = {1:15,2:12,3:10,4:9,5:8,6:7,7:6,8:5,9:4,10:3,11:2,12:1,0:0}
    score = 0
    for rank in rank_list:
        score += to_score_dict[rank]
    return score

def to_main_match_dict(main_embed_dict):
    main_match_dict = {'match_type':0, 'enemy_list':[], 'sum_score_list':[], 'race_list':[], 'run_track_dict':{}}
    main_match_dict['match_type'] = int(main_embed_dict['title'][5])
    if 'vs' in main_embed_dict['title']:
        main_match_dict['enemy_list'] = list(main_embed_dict['title'].split('vs ')[1].split(' '))
    main_match_dict['sum_score_list'] = list(map(lambda x: int(x.split(' (')[0]), main_embed_dict['description'].split(' @')[0].split(' : ')))
    if 'fields' in main_embed_dict:
        for field in main_embed_dict['fields']:
            score_list = []
            for score_str in field['value'].split(' | ')[0].split(' : '):
                score_list.append(int(score_str.split(' (')[0]))
            rank_list = list(map(int, field['value'].split(' | ')[1].split(',')))
            main_match_dict['race_list'].append({'score_list':score_list, 'rank_list':rank_list})
            if '  (' in field['name']:
                main_match_dict['run_track_dict'][int(field['name'].split('  ')[0].replace('race',''))] = field['name'].split('  (')[1][:-1]
    return main_match_dict

def to_sub_match_dict(sub_embed_dict):
    sub_match_dict = {'match_type':0, 'enemy_list':[], 'race':0, 'score_list':[], 'rank_lists':[], 'run_track':None}
    sub_match_dict['race'] = int(sub_embed_dict['title'].split('  ')[0].replace('race',''))
    if '  (' in sub_embed_dict['title']:
        sub_embed_dict['run_track'] = sub_embed_dict['title'].split('  (')[1][:-1]
    for field in sub_embed_dict['fields']:
        enemy = field['name']
        if enemy == 'Your team':
            pass
        else:
            sub_match_dict['enemy_list'].append(enemy)
        score_text, rank_text = field['value'].split(' | ')
        sub_match_dict['score_list'].append(int(score_text.split('score : ')[-1]))
        sub_match_dict['rank_lists'].append(list(map(int, rank_text.split('rank : ')[-1].split(','))))
    sub_match_dict['match_type'] = len(sub_match_dict['enemy_list']) + 1
    return sub_match_dict

def create_sub_match_dict(match_type, enemy_list, race, rank_lists, run_track):
    new_rank_lists = [[0]*match_type]*(12//match_type)
    score_list = []
    for i, rank_list in enumerate(rank_lists):
        new_rank_lists[i] = rank_list
    for rank_list in new_rank_lists:
        score_list.append(calc_score(rank_list))
    sub_match_dict = {'match_type':0, 'enemy_list':enemy_list, 'race':race, 'score_list':score_list, 'rank_lists':new_rank_lists, 'run_track':run_track}
    return sub_match_dict

def create_score_text(score_list):
    score_text = ''
    for score in score_list:
        if score_text == '':
            score_text = str(score)
        else:
            score_dif = score_list[0] - score
            if score_dif >= 0:
                score_text += f' : {score} (+{score_dif})'
            else:
                score_text += f' : {score} ({score_dif})'
    return score_text

def to_main_embed_dict(main_match_dict):
    match_type = main_match_dict['match_type']
    enemy_list = main_match_dict['enemy_list']
    sum_score_list = main_match_dict['sum_score_list']
    race_list = main_match_dict['race_list']
    run_track_dict = main_match_dict['run_track_dict']
    if enemy_list == []:
        title = f'即時集計 {match_type}v{match_type}'
    else:
        title = f'即時集計 {match_type}v{match_type}\nvs {" ".join(enemy_list)}'
    description = create_score_text(sum_score_list) + f' @{12 - len(race_list)}'
    fields = []
    for i, race in enumerate(race_list):
        field = {}
        name = f'race{i+1}'
        if i+1 in run_track_dict:
            name += f'  ({run_track_dict[i+1]})'
        score_list = race['score_list']
        rank_list = race['rank_list']
        value = create_score_text(score_list) + ' | ' + ','.join(map(str, rank_list))
        field['name'] = name
        field['value'] = value
        fields.append(field)
    main_embed_dict = {'title':title, 'description':description, 'fields':fields}
    return main_embed_dict

def to_sub_embed_dict(sub_match_dict):
    match_type = sub_match_dict['match_type']
    enemy_list = sub_match_dict['enemy_list']
    race = sub_match_dict['race']
    score_list = sub_match_dict['score_list']
    rank_lists = sub_match_dict['rank_lists']
    run_track = sub_match_dict['run_track']
    title = f'race{race}'
    if not run_track == None:
        title += f'  ({run_track})'
    fields = []
    for i, team in enumerate(['Your team'] + enemy_list):
        fields.append({'name':team, 'value':f'score : {score_list[i]} | rank : {",".join(map(str, rank_lists[i]))}'})
    sub_embed_dict = {'title':title, 'fields':fields}
    return sub_embed_dict

def calculation(main_match_dict, rank_lists, run_track):
    new_score_list = []
    for rank_list in rank_lists:
        new_score_list.append(calc_score(rank_list))
    main_match_dict['race_list'].append({'score_list':new_score_list, 'rank_list':rank_lists[0]})
    new_sum_score_list = []
    for i in range(12//main_match_dict['match_type']):
        new_sum_score_list.append(main_match_dict['sum_score_list'][i] + new_score_list[i])
    main_match_dict['sum_score_list'] = new_sum_score_list
    if not run_track == None:
        main_match_dict['run_track_dict'][len(main_match_dict['race_list'])] = run_track
    return to_main_embed_dict(main_match_dict)

def back(main_match_dict):
    if main_match_dict['race_list'] == []:
        return
    for i in range(12//main_match_dict['match_type']):
        main_match_dict['sum_score_list'][i] -= main_match_dict['race_list'][-1]['score_list'][i]
    del main_match_dict['race_list'][-1]
    return main_match_dict

def create_dif_text(score0, score):
    dif = score0 - score
    if dif >= 0:
        return f'+{dif}'
    else:
        return f'{dif}'

def create_status(main_match_dict):
    sum_score_list = main_match_dict['sum_score_list']
    enemy_list = main_match_dict['enemy_list']
    if enemy_list == []:
        enemy_list = ['enemy team']
    team_list = ['Your team'] + enemy_list
    sorted_list = sorted(list(set(sum_score_list)), reverse=True)
    status_list = []
    rank_set = set()
    for j, score in enumerate(sorted_list):
        index_num = [n for n, v in enumerate(sum_score_list) if v == score]
        for i in index_num:
            status_list.append({'team':team_list[i], 'score':score, 'rank':j+1})
            rank_set.add(j+1)
    rank = 0
    score = main_match_dict['sum_score_list'][0]
    description = ''
    value = ''
    for i, status_dict in enumerate(status_list):
        dif = score - status_dict['score']
        if status_dict['team'] == 'Your team':
            value += f'**Your team : {score}**\n'
            rank = i + 1
            if i == 0:
                if i+2 in rank_set:
                    for j in status_list[i+1:]:
                        if j['rank'] == i+2:
                            description += f'{i+2}位との点差 : {create_dif_text(score, j["score"])} '
                            break
            else:
                if i in rank_set:
                    for j in status_list[:i]:
                        if j['rank'] == i:
                            description += f'{i}位との点差 : {create_dif_text(score, j["score"])} '
                            break
        else:
            value += f'{status_dict["team"]} : {status_dict["score"]} ({create_dif_text(score, status_dict["score"])})\n'
    description += f'@{12-len(main_match_dict["race_list"])}'
    return {'title':f'現在{rank}位', 'description':description, 'fields':[{'name':'score', 'value':value}]}

def content(content):
    new_list = []
    if '-' in content:
        if content.startswith('-'):
            content = '1' + content
        if content.endswith('-'):
            content = content + '12'
        content_list = list(content.split('-'))
        for i, c in enumerate(content_list):
            if i == 0:
                pass
            else:
                if c[0] == '1':
                    if len(c) == 1:
                        new_list.append('')
                    else:
                        b = int(c[:2])
                        if content_list[i-1].endswith('10'):
                            a = 10
                        elif content_list[i-1].endswith('11'):
                            a = 11
                        else:
                            a = int(content_list[i-1][-1])
                        if b - a > 1 :
                            new = ''
                            while b - a > 1:
                                a += 1
                                new += str(a)
                            new_list.append(new)
                        else:
                            new_list.append('')
                else:
                    a = int(content_list[i-1][-1])
                    b = int(c[0])
                    if b - a > 1 :
                        new = ''
                        while b - a > 1:
                            a += 1
                            new += str(a)
                        new_list.append(new)
                    else:
                        new_list.append('')
        if len(content_list) - len(new_list) == 1:
            content = ''
            for i in range(len(new_list)):
                content += content_list[i] + new_list[i]
            content += content_list[-1]
            return content
        else:
            return content.replace('-', '')
    return content