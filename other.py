# import json
# """
# favorites
# 1.02 : 6.5
# 1.03 - 1.04 : 5.5
# 1.05 - 1.08 : 4.5
# 1.09 - 1.17 : 3.5
# 1.18 - 1.26 : 2.5
# 1.27 - 1.35 : 2
# 1.36 - 1.6  : 1.5
# 1.61 - 2.00 : 0.5
#
# underdogs
# 1.02 : 5.5
# 1.03 - 1.04 : 4.5
# 1.05 - 1.08 : 3.5
# 1.09 - 1.17 : 2.5
# 1.27 - 1.35 : 1.5
# 1.35 - 2.00 : 0.5
#
# """
#
#
# def float_range(start, stop):
#     arr = []
#     while start < stop:
#         arr.append(round(start, 2))
#         start += 0.01
#     return tuple(arr)
#
# dict_favor = {}
#
# cnt= 1
#
# while cnt <=2:
#     x = round(cnt,2)
#     if x == 1:
#         dict_favor['-'] = 11
#     elif x == 1.01:
#         dict_favor[x] = 9
#     elif x == 1.02:
#         dict_favor[x] = 7
#     elif x == 1.03 or x == 1.04:
#         dict_favor[x] = 6
#     elif 1.05 <=x<=1.08:
#         dict_favor[x] = 5
#     elif 1.09<=x<=1.17:
#         dict_favor[x] = 4
#     elif 1.18<=x<=1.26:
#         dict_favor[x] = 3
#     elif 1.27 <=x<=1.35:
#         dict_favor[x]= 2
#     elif 1.36<=x<=1.60:
#         dict_favor[x] = 2
#     else:
#         dict_favor[x] = 1
#     cnt+=0.01
#
# '''underdogs
# 1.02 : 5.5
# 1.03 - 1.04 : 4.5
# 1.05 - 1.08 : 3.5
# 1.09 - 1.17 : 2.5
# 1.18 - 1.35 : 1.5
# 1.35 - 2.00 : 0.5
# '''
# dict_under = {}
# cnt = 1
# while cnt<2:
#     x = round(cnt,2)
#     if x == 1:
#         dict_under['-'] = 8
#     elif x == 1.01:
#         dict_under[x] = 7
#     elif x == 1.02:
#         dict_under[x] = 5
#     elif x == 1.03 or x == 1.04:
#         dict_under[x] = 4
#     elif 1.05 <=x<=1.08:
#         dict_under[x] = 3
#     elif 1.09<=x<=1.17:
#         dict_under[x] = 2
#     elif 1.18<=x<=1.35:
#         dict_under[x] = 1
#     else:
#         dict_under[x] = 0
#     cnt += 0.01
#
# for i,j in dict_under.items():
#     print(i,j)
#
#
#
#
# d = {'FAVORIT' : dict_favor, 'UNDERDOG' : dict_under}
#
# with open('handicap_tab.json', 'w') as js:
#     json.dump(d, js, indent=2)


""""""""""""""""""""""""""""""""""""""""""""""""""
ls = [['08.05.', '02:00', 'Phoenix', 'Suns', 'Denver', 'Nuggets', '129', '124', '32', '34', '31', '27', '35', '31', '31', '32', 'W'], ['06.05.', '04:00', 'Phoenix', 'Suns', 'Denver', 'Nuggets', '121', '114', '29', '31', '38', '21', '23', '36', '31', '26', 'W'], ['02.05.', '04:00', 'Denver', 'Nuggets', 'Phoenix', 'Suns', '97', '87', '18', '21', '22', '21', '30', '31', '27', '14', 'L'], ['30.04.', '02:30', 'Denver', 'Nuggets', 'Phoenix', 'Suns', '125', '107', '31', '32', '37', '19', '26', '30', '31', '26', 'L'], ['26.04.', '04:00', 'Phoenix', 'Suns', 'Los', 'Angeles', 'Clippers', '136', '130', '32', '30', '29', '40', '50', '24', '25', '36', 'W'], ['22.04.', '21:30', 'Los', 'Angeles', 'Clippers', 'Phoenix', 'Suns', '100', '112', '30', '23', '17', '25', '31', '35', '22', '29', 'W'], ['21.04.', '04:30', 'Los', 'Angeles', 'Clippers', 'Phoenix', 'Suns', '124', '129', '27', '27', '24', '27', '34', '40', '39', '35', 'W'], ['19.04.', '04:00', 'Phoenix', 'Suns', 'Los', 'Angeles', 'Clippers', '123', '109', '24', '29', '35', '30', '33', '28', '31', '22', 'W'], ['17.04.', '02:00', 'Phoenix', 'Suns', 'Los', 'Angeles', 'Clippers', '110', '115', '18', '30', '36', '29', '27', '22', '29', '34', 'L'], ['09.04.', '21:30', 'Phoenix', 'Suns', 'Los', 'Angeles', 'Clippers', '114', '119', '28', '19', '25', '29', '33', '34', '28', '37', 'L'], ['08.04.', '04:30', 'Los', 'Angeles', 'Lakers', 'Phoenix', 'Suns', '121', '107', '30', '34', '31', '28', '35', '27', '25', '18', 'L'], ['07.04.', '04:00', 'Phoenix', 'Suns', 'Denver', 'Nuggets', '119', '115', '27', '25', '29', '30', '33', '31', '30', '29', 'W'], ['05.04.', '04:00', 'Phoenix', 'Suns', 'San', 'Antonio', 'Spurs', '115', '94', '42', '25', '27', '26', '28', '25', '18', '18', 'W'], ['03.04.', '01:00', 'Oklahoma', 'City', 'Thunder', 'Phoenix', 'Suns', '118', '128', '27', '27', '28', '42', '34', '29', '29', '30', 'W'], ['01.04.', '04:30', 'Phoenix', 'Suns', 'Denver', 'Nuggets', '100', '93', '32', '20', '28', '20', '24', '34', '16', '19', 'W'], ['30.03.', '04:00', 'Phoenix', 'Suns', 'Minnesota', 'Timberwolves', '107', '100', '25', '24', '23', '27', '33', '23', '26', '26', 'W'], ['28.03.', '03:00', 'Utah', 'Jazz', 'Phoenix', 'Suns', '103', '117', '26', '37', '26', '20', '29', '27', '22', '33', 'W'], ['26.03.', '04:00', 'Phoenix', 'Suns', 'Philadelphia', '76ers', '125', '105', '26', '24', '32', '29', '31', '30', '36', '22', 'W'], ['25.03.', '03:00', 'Sacramento', 'Kings', 'Phoenix', 'Suns', '135', '127', '24', '30', '32', '37', '45', '26', '34', '34', 'L'], ['23.03.', '03:00', 'Los', 'Angeles', 'Lakers', 'Phoenix', 'Suns', '122', '111', '23', '26', '36', '26', '29', '33', '34', '26', 'L'], ['19.03.', '20:30', 'Oklahoma', 'City', 'Thunder', 'Phoenix', 'Suns', '124', '120', '25', '31', '32', '38', '33', '27', '34', '24', 'L'], ['17.03.', '03:00', 'Phoenix', 'Suns', 'Orlando', 'Magic', '116', '113', '30', '31', '33', '27', '31', '27', '22', '28', 'W'], ['15.03.', '03:00', 'Phoenix', 'Suns', 'Milwaukee', 'Bucks', '104', '116', '24', '29', '24', '28', '36', '28', '20', '31', 'L'], ['14.03.', '03:00', 'Golden', 'State', 'Warriors', 'Phoenix', 'Suns', '123', '112', '43', '21', '32', '37', '23', '30', '25', '24', 'L'], ['12.03.', '03:00', 'Phoenix', 'Suns', 'Sacramento', 'Kings', '119', '128', '32', '31', '27', '36', '36', '29', '24', '32', 'L'], ['09.03.', '03:00', 'Phoenix', 'Suns', 'Oklahoma', 'City', 'Thunder', '132', '101', '34', '21', '26', '31', '44', '28', '28', '21', 'W'], ['05.03.', '19:00', 'Dallas', 'Mavericks', 'Phoenix', 'Suns', '126', '130', '25', '31', '37', '28', '33', '37', '31', '34', 'W'], ['04.03.', '02:00', 'Chicago', 'Bulls', 'Phoenix', 'Suns', '104', '125', '29', '40', '35', '20', '21', '34', '19', '31', 'W'], ['02.03.', '01:00', 'Charlotte', 'Hornets', 'Phoenix', 'Suns', '91', '105', '22', '27', '19', '30', '32', '22', '18', '26', 'W'], ['26.02.', '19:00', 'Milwaukee', 'Bucks', 'Phoenix', 'Suns', '104', '101', '33', '26', '20', '20', '22', '28', '29', '27', 'L'], ['25.02.', '04:00', 'Phoenix', 'Suns', 'Oklahoma', 'City', 'Thunder', '124', '115', '29', '30', '36', '30', '29', '27', '30', '28', 'W'], ['17.02.', '04:00', 'Phoenix', 'Suns', 'Los', 'Angeles', 'Clippers', '107', '116', '23', '28', '29', '26', '32', '37', '23', '25', 'L'], ['15.02.', '03:00', 'Phoenix', 'Suns', 'Sacramento', 'Kings', '120', '109', '27', '29', '35', '29', '28', '28', '30', '23', 'W'], ['11.02.', '01:00', 'Indiana', 'Pacers', 'Phoenix', 'Suns', '104', '117', '24', '30', '23', '30', '30', '35', '27', '22', 'W'], ['10.02.', '01:30', 'Atlanta', 'Hawks', 'Phoenix', 'Suns', '116', '107', '36', '22', '20', '25', '37', '28', '23', '32', 'L'], ['08.02.', '01:30', 'Brooklyn', 'Nets', 'Phoenix', 'Suns', '112', '116', '25', '24', '26', '33', '30', '30', '31', '29', 'W'], ['05.02.', '01:00', 'Detroit', 'Pistons', 'Phoenix', 'Suns', '100', '116', '27', '30', '22', '28', '27', '30', '24', '28', 'W'], ['04.02.', '01:30', 'Boston', 'Celtics', 'Phoenix', 'Suns', '94', '106', '20', '24', '24', '33', '29', '17', '21', '32', 'W'], ['02.02.', '04:00', 'Phoenix', 'Suns', 'Atlanta', 'Hawks', '100', '132', '23', '26', '24', '40', '20', '36', '33', '30', 'L'], ['31.01.', '03:00', 'Phoenix', 'Suns', 'Toronto', 'Raptors', '114', '106', '31', '28', '31', '25', '20', '31', '32', '22', 'W'], ['29.01.', '02:00', 'AOT', 'San', 'Antonio', 'Spurs', 'Phoenix', 'Suns', '118', '128', '26', '33', '22', '22', '28', '32', '34', '23', '8', '18', 'W'], ['27.01.', '04:00', 'Phoenix', 'Suns', 'Dallas', 'Mavericks', '95', '99', '32', '32', '16', '22', '21', '22', '26', '23', 'L'], ['25.01.', '03:00', 'Phoenix', 'Suns', 'Charlotte', 'Hornets', '128', '97', '36', '15', '22', '32', '40', '30', '30', '20', 'W']]
team = ['Phoenix', 'Suns']


def mark_home_away(team, all_matches):
    marked_list = []
    waste = ["W", "U18","U19", "U20", "U21","U22", "U23"]
    for i in waste:
        if i in team:
            team = [j for j in team if j not in waste]
    print(team)
    for match in all_matches:
        matchline = [j for j in match[:len(match) - 1] if j not in waste] + match[-1:]
        team_index = matchline.index(team[len(team) - 1])
        if matchline[team_index + 1].isdigit():
            matchline.append('AWAY')
        elif "(" in matchline[team_index + 1] and matchline[team_index + 2].isdigit():
            matchline.append('AWAY')
        else:
            matchline.append('HOME')
        marked_list.append(matchline)

    scorelines = []
    for match in marked_list:
        if len([i for i in match if i.isdigit()]) < 10:
            continue
        if "AOT" in match:
            scoreline = match[-13:-2]+match[-1:]
        else:
            scoreline = match[-11:-2]+match[-1:]
        scorelines.append([i if not i.isdigit() else int(i) for i in scoreline])

    return marked_list, scorelines


wl = ['L', 'W', 'L', 'L', 'L', 'W', 'L', 'W', 'W', 'L', 'W', 'L', 'L', 'W', 'W', 'L', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'L', 'L', 'W', 'L', 'W', 'L', 'W', 'L', 'L', 'L', 'L', 'W', 'W', 'W', 'L', 'L', 'W', 'L', 'W', 'L', 'W', 'W', 'W', 'W', 'L', 'W', 'L', 'L', 'W', 'L', 'W', 'L', 'W', 'W', 'L', 'W', 'L', 'W', 'L', 'W', 'W', 'L', 'W', 'W', 'L', 'W', 'W', 'W', 'L', 'W', 'L', 'W', 'W', 'W', 'W', 'L', 'W', 'W', 'L', 'L', 'L', 'L', 'L', 'L', 'W', 'L', 'W', 'W', 'W', 'L', 'W', 'L', 'W', 'W', 'W', 'L', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'L', 'W', 'W', 'W', 'W', 'L', 'L', 'W', 'W', 'W', 'L', 'W', 'W', 'L', 'W', 'L', 'W', 'L', 'L', 'W', 'L', 'W', 'L', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'L', 'W', 'W', 'L', 'W', 'L', 'L', 'L', 'W', 'W', 'W', 'W', 'W', 'L', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'L', 'W', 'W', 'L', 'L', 'W', 'W', 'L', 'L']
s = ['W','W','W','L','L', 'W', 'L', 'L', 'L', 'W', 'L', 'W', 'W', 'L', 'W', 'L']
print(len(wl))

def concatenate_matches(lst):
    concatenated = []
    cnt  = 1
    for i in range(0,len(lst),4):
        for k in reversed(lst[i:i+4]):
            concatenated.append(k)
    return concatenated
print(concatenate_matches(wl))

# for i in range(0,160,4):
#     print(i)


def get_last_3games_series(lst):
    count = 1
    current_value = lst[0]
    for i in range(1, len(lst)):
        if lst[i] == current_value:
            count += 1
        else:
            break
    return count, current_value

print(get_last_3games_series(s[::-1]))


def count_max_consecutive_W_L(sequence):
    max_consecutive_W = 0
    max_consecutive_L = 0
    current_consecutive_W = 0
    current_consecutive_L = 0

    for i in range(len(sequence)):
        if sequence[i] == 'W':
            current_consecutive_W += 1
            current_consecutive_L = 0
            if current_consecutive_W > max_consecutive_W:
                max_consecutive_W = current_consecutive_W
        elif sequence[i] == 'L':
            current_consecutive_L += 1
            current_consecutive_W = 0
            if current_consecutive_L > max_consecutive_L:
                max_consecutive_L = current_consecutive_L
        if i == len(sequence) - 1 and sequence[i] == 'L':
            if current_consecutive_L > max_consecutive_L:
                max_consecutive_L = current_consecutive_L

    return max_consecutive_W, max_consecutive_L

#
# browser.execute_script("arguments[0].click();", WebDriverWait(browser, 20).until(
#     EC.element_to_be_clickable((By.CSS_SELECTOR, "a.event__more.event__more--static"))))
#
#
# k1 = 'd'
# k2 = 1
# print(all([k1!=0, k2!=0]))
#
# print(min(1,2))
#
#
# def get_quarters_totals_series(matches, average):
#     quarters_series = []
#
#     for match in matches:
#         results = match[:-1]
#         quarters = [(results[i] + results[i + 1]) for i in range(0, len(results), 2)]
#         print(quarters)
#         for summ in quarters:
#             if summ + 0.5 < average:
#                 quarters_series.append('U')
#             else:
#                 quarters_series.append('O')
#
#     return quarters_series
#
# bets = ()
#
# bets += (111,222,33)
# print(' '.join(map(str,(1,10))))
# print(str([1,2,3]))