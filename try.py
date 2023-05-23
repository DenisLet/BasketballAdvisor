import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from statistics import mean
import json


class ScheduleScraper:
    def __init__(self, url):
        self.url = url
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument('--headless')
        self.browser = webdriver.Chrome()

    def scrape(self):
        try:
            self.browser.get(self.url)
            resume = input("Select matches and press enter to continue(Add to favorite) ")
            self.browser.implicitly_wait(1)
            matches = self.browser.find_elements(By.CSS_SELECTOR, "[id^='g_3']")
            checklist = dict()

            for match in matches:
                link = match.get_attribute("id")
                url_match = f"https://www.basketball24.com/match/{link[4:]}"
                coefficients = []
                # print(match.text.split())
                for line in match.text.split():
                    try:
                        if line == '-':
                            coefficients.append('-')
                        if float(line) and '.' in line:
                            coefficients.append(float(line))
                    except Exception as ex:
                        # print(ex)
                        continue

                if not coefficients:
                    coefficients = [0, 0]

                checklist[url_match] = coefficients
                # print(checklist)
            return checklist
        finally:
            self.browser.quit()


url = "https://www.basketball24.com"
scraper = ScheduleScraper(url)
schedule = scraper.scrape()
# print(schedule)


def clarify_coefs(data: list):
    coefs = tuple()
    if len(data) == 4:
        data = data[2:]
    if data.count('-') > 1:
        coefs = (0, 0)
    elif data[0] == '-':
        coefs= (1., data[1])
    elif data[1] == '-':
        coef = (data[0], 1.)
    else:
        coefs = (data)
    return coefs


def main(url, coefficients):
    # t1_coef, t2_coef = clarify_coefs(coefficients)
    # print(t1_coef, t2_coef)

    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    browser = webdriver.Chrome(desired_capabilities=caps)
    browser.get(url)

    browser.implicitly_wait(1)

    team_home = browser.find_elements(By.CSS_SELECTOR, "a.participant__participantName")[0].get_attribute(
            "href") + "results/"
    team_away = browser.find_elements(By.CSS_SELECTOR, "a.participant__participantName")[1].get_attribute(
            "href") + "results/"
    title = browser.find_element(By.CSS_SELECTOR, ".tournamentHeader__country").text


    # print(title)
    def separator(matches):
        match_list = list()
        for i in matches:
            line = i.text
            # print(line)
            if "(" in line or "Awrd" in line or "Abn" in line:
                continue
            if len([i for i in line.split() if i.isdigit()]) < 6:
                continue
            match_list.append(line.split())
        return match_list

    def get_data(browser,link):
        browser.get(link)
        dataset = browser.find_elements(By.CSS_SELECTOR, "[id^='g_3']")
        matches = separator(dataset)
        team = browser.find_element(By.CSS_SELECTOR, "div.heading__name").get_attribute("innerHTML")
        return matches,team

    def forming(browser, link1, link2):  # NEED ADD TYPE SPORT AND FIXABLE CSS SELECTOR
        match_list_home, team1 = get_data(browser,link1)
        match_list_away, team2 = get_data(browser,link2)
        return match_list_home, match_list_away, team1, team2

    games = forming(browser, team_home, team_away)
    team1_results = games[0]
    team2_results = games[1]
    team1_name = games[2].split()
    team2_name = games[3].split()

    def separation_home_away(team_, all_matches):
        home_matches = list()
        away_matches = list()
        waste = ["W", "U18", "U20", "U21", "U23"]  # WASTE - U20 and another juniors and woman champs//
        for i in waste:
            if i in team_:
                team_ = [j for j in team_ if j not in waste]
        # print(team_)
        for k in all_matches:
            i = [j for j in k[:len(k) - 1] if j not in waste] + k[-1:]
            x = i.index(team_[len(team_) - 1])
            if i[x + 1].isdigit():
                away_matches.append(i)
            elif "(" in i[x + 1] and i[x + 2].isdigit():
                away_matches.append(i)
            else:
                home_matches.append(i)
        return home_matches, away_matches

    team1_home, team1_away = separation_home_away(team1_name, games[0])
    team2_home, team2_away = separation_home_away(team2_name, games[1])



    def get_scores(results):
        scorelines = []
        for match in results:
            if len([ i for i in match if i.isdigit() ]) < 10:
                continue
            if "AOT" in match:
                scoreline = match[-13:-1]
            else:
                scoreline = match[-11:-1]
            scorelines.append(list(map(int,scoreline)))
        return scorelines


    team1_all_games = get_scores(games[0])
    team2_all_games = get_scores(games[1])
    team1_results_home = get_scores(team1_home)
    team1_results_away = get_scores(team1_away)
    team2_results_home = get_scores(team2_home)
    team2_results_away = get_scores(team2_away)

    def each_total(data):
        return [sum(i[2:10]) for i in data]

    def mark_home_away(team, all_matches):
        marked_list = []
        waste = ["W", "U18", "U19", "U20", "U21", "U22", "U23"]
        for i in waste:
            if i in team:
                team = [j for j in team if j not in waste]
        # print(team)
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
        # print(marked_list)
        scorelines = []
        for match in marked_list:
            if len([i for i in match if i.isdigit()]) < 10:
                continue
            if "AOT" in match:
                scoreline = match[-12:-4] + match[-1:]
            else:
                scoreline = match[-10:-2] + match[-1:]
            scorelines.append([i if not i.isdigit() else int(i) for i in scoreline])

        return scorelines


    team1_scores = mark_home_away(team1_name, team1_results)
    team2_scores = mark_home_away(team2_name, team2_results)
    print(len(team1_scores))

    def get_quarters_winlost_series(matches):
        quarters_series = []

        for match in matches:
            location = match[-1]
            results = match[:-1]
            if len(results) % 2 != 0:
                raise ValueError("Invalid match: odd number of results")
            quarters = [(results[i], results[i + 1]) for i in range(0, len(results), 2)]

            for q in quarters:
                if location == 'HOME':
                    quarters_series.append('W' if q[0] > q[1] else 'L')
                elif location == 'AWAY':
                    quarters_series.append('W' if q[0] < q[1] else 'L')
        # print(quarters_series)
        return quarters_series

    def concatenate_matches(lst):
        concatenated = []
        cnt = 1
        for i in range(0, len(lst), 4):
            for k in reversed(lst[i:i + 4]):
                concatenated.append(k)
        return concatenated


    # print(concatenate_matches(wl))

    team1_series = concatenate_matches(get_quarters_winlost_series(team1_scores))
    team2_series = concatenate_matches(get_quarters_winlost_series(team2_scores))
    # print(team1_series)
    # print(team2_series)

    def get_last_3games_series(lst):
        count = 1
        current_value = lst[0]
        for i in range(1, len(lst)):
            if lst[i] == current_value:
                count += 1
            else:
                break
        return count, current_value

    team1_last3_series = get_last_3games_series(team1_series)
    team2_last3_series = get_last_3games_series(team2_series)



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

    team1_W_L_consecutive = count_max_consecutive_W_L(team1_series)
    team2_W_L_consecutive = count_max_consecutive_W_L(team2_series)
    print()
    if team1_last3_series[0]>=4 or team2_last3_series[0]>=4:
        print('TEAM1 QUARTER SERIES WIN / LOST:: ', *team1_W_L_consecutive,'LAST SERIES:',*team1_last3_series)
        print('TEAM2 QUARTER SERIES WIN / LOST:: ', *team2_W_L_consecutive,'LAST SERIES:',*team2_last3_series)
        print(title)
        print(team1_name)
        print(team2_name)
        print(url)
        print()

    def check_condition_to_bet(team1_WL, team2_WL, team1_Last, team2_Last):

        team1_winstreak_max, team1_losestreak_max = team1_WL
        team2_winstreak_max, team2_losestreak_max = team2_WL
        team1_nowstreak_len, team1_nowstreak_sign = team1_Last
        team2_nowstreak_len, team2_nowstreak_sign = team2_Last

        bet = ''

        if team1_nowstreak_sign == 'W':
            if team1_winstreak_max - team1_nowstreak_len <=2:
                bet += f'{team1_name} QUARTER SERIES WIN: {team1_winstreak_max}, NOW: {team1_nowstreak_len}\n'


    def find_handicap_value(coef, coef1):
        position, handicap_value = '',''
        if 1 <= coef < 2:
            position = "FAVORIT"
        else:
            position = "UNDERDOG"
            coef = coef1
        with open('handicap_tab.json', 'r') as file:
            add_value = json.load(file)[position][str(coef)]
        print(add_value)
        return position, int(add_value)

    # if t1_coef != 0 or t2_coef != 0:
    #     handicap1 = find_handicap_value(t1_coef, t2_coef)
    #     handicap2 = find_handicap_value(t2_coef, t1_coef)




    def CheckWin1to4Quarters(matches_team1, matches_team2, coef_team1, coef_team2):

        if coef_team1 != 0 or coef_team2!= 0:
            handicap1 = find_handicap_value(t1_coef, t2_coef)
            handicap2 = find_handicap_value(t2_coef, t1_coef)
        else:
            handicap1 = ('NO DATA', 0)
            handicap2 = ('NO DATA', 0)

        t1_win_one_of_4 = 0
        for match in matches_team1:
            location = match[-1]
            if location == 'HOME' and handicap1[0] == 'FAVORIT':
                print(match[0],match[1]+handicap1[1])
                if match[0] > match[1]+handicap1[1] or match[2] > match[3] + handicap1[1] or match[4] > match[5]+ handicap1[1] or match[6] > match[7] + handicap1[1]:
                    t1_win_one_of_4 += 1

            print('LOCATION: ',location)
            print('STATUS: ', handicap1[0])
            print('HANDICAP: ',handicap1[1])
            print(t1_win_one_of_4)


    # CheckWin1to4Quarters(team1_scores, team2_scores, t1_coef, t2_coef)











for url, coefs in schedule.items():
    main(url, coefs)
