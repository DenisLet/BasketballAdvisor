import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from statistics import mean
import json
from math import ceil
from TGnotifier import send_to_tg

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


def clarify_coefs(data: list) -> list:
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
    t1_coef, t2_coef = clarify_coefs(coefficients)
    print(t1_coef, t2_coef)

    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(desired_capabilities=caps, options=options)
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
        # time.sleep(5)
        # clicker = browser.find_element(By.CSS_SELECTOR, 'a.event__more.event__more--static').click()
        try:
            browser.execute_script("arguments[0].click();", WebDriverWait(browser, 29).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.event__more.event__more--static"))))
        except:
            print("LOW NUMBERS OF MATCHES ONE OF TEAM")
        finally:
            time.sleep(2)
            dataset = browser.find_elements(By.CSS_SELECTOR, "[id^='g_3']")
            matches = separator(dataset)
            team = browser.find_element(By.CSS_SELECTOR, "div.heading__name").get_attribute("innerHTML")
        return matches, team

    def forming(browser, link1, link2):  # NEED ADD TYPE SPORT AND FIXABLE CSS SELECTOR
        match_list_home, team1 = get_data(browser,link1)
        match_list_away, team2 = get_data(browser,link2)
        return match_list_home, match_list_away, team1, team2

    games = forming(browser, team_home, team_away)
    team1_results = games[0]
    team2_results = games[1]
    team1_name = games[2].split()
    team2_name = games[3].split()
    print(team1_name, team2_name)

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

    def get_total_series(matches, average):
        total_series = []
        for match in matches:
            total_series.append(sum(match[:-1]))

        series_O_U = []
        for val in total_series:
            if val + 0.5 < average:
                series_O_U.append('U')
            else:
                series_O_U.append('O')

        return series_O_U


    true_series1 = get_quarters_winlost_series(team1_scores)


    def get_quarters_totals_series(matches, average):
        quarters_series = []

        for match in matches:
            results = match[:-1]
            quarters = [(results[i] + results[i + 1]) for i in range(0, len(results), 2)]

            for summ in quarters:
                if summ + 0.5 <  average:
                    quarters_series.append('U')
                else:
                    quarters_series.append('O')

        return quarters_series




    def concatenate_matches(lst):
        concatenated = []
        cnt = 1
        for i in range(0, len(lst), 4):
            for k in reversed(lst[i:i + 4]):
                concatenated.append(k)
        return concatenated

    team1_series = concatenate_matches(get_quarters_winlost_series(team1_scores))
    team2_series = concatenate_matches(get_quarters_winlost_series(team2_scores))

    print(team1_scores)
    print(true_series1)
    print(team1_series)

    def get_last_games_series(lst):
        count = 1
        current_value = lst[0]
        for i in range(1, len(lst)):
            if lst[i] == current_value:
                count += 1
            else:
                break
        return count, current_value

    team1_last3_series = get_last_games_series(team1_series)
    team2_last3_series = get_last_games_series(team2_series)


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

        return f'{max_consecutive_W} {max_consecutive_L}'


    def count_max_consecutive_O_U(sequence):
        max_consecutive_O = 0
        max_consecutive_U = 0
        current_consecutive_O = 0
        current_consecutive_U = 0

        for i in range(len(sequence)):
            if sequence[i] == 'O':
                current_consecutive_O += 1
                current_consecutive_U = 0
                if current_consecutive_O > max_consecutive_O:
                    max_consecutive_O = current_consecutive_O
            elif sequence[i] == 'U':
                current_consecutive_U += 1
                current_consecutive_O = 0
                if current_consecutive_U > max_consecutive_U:
                    max_consecutive_U = current_consecutive_U
            if i == len(sequence) - 1 and sequence[i] == 'U':
                if current_consecutive_U > max_consecutive_U:
                    max_consecutive_U = current_consecutive_U

        return f'{max_consecutive_O} {max_consecutive_U}'

    team1_W_L_consecutive = count_max_consecutive_W_L(team1_series)
    team2_W_L_consecutive = count_max_consecutive_W_L(team2_series)


    bets = tuple()
    bet1, bet2, bet3 = (tuple() for i in range(3))


    if team1_last3_series[0]>=4 or team2_last3_series[0]>=4:

        print('TEAM1 QUARTER SERIES WIN / LOST:: ', team1_W_L_consecutive,'LAST SERIES:',*team1_last3_series)
        print('TEAM2 QUARTER SERIES WIN / LOST:: ', team2_W_L_consecutive,'LAST SERIES:',*team2_last3_series)
        print(title)
        print(team1_name)
        print(team2_name)
        print(url)
        bet1 = ('TEAM1 QUARTER SERIES WIN / LOST::', team1_W_L_consecutive,
                'LAST SERIES:',' '.join(map(str,team1_last3_series)),'TEAM2 QUARTER SERIES WIN / LOST:: '
                ,team2_W_L_consecutive,'LAST SERIES:',' '.join(map(str,team2_last3_series)),title,
                str(team1_name), str(team2_name),
                url)
        bets += bet1
        print('----------')


    def get_status_vs_value(coef1, coef2):
        t1_status = "FAVORIT" if coef1 <= coef2 else "UNDERDOG"
        t2_status = "UNDERDOG" if coef1 <= coef2 else "FAVORIT"

        t1_value, t2_value = 0, 0

        if coef1 != 0 and coef2 != 0:
            with open('handicap_tab.json', 'r') as file:
                data = json.load(file)
                min_coef = str(min(coef1, coef2))
                t1_value = data[t1_status].get(min_coef, 0)
                t2_value = data[t2_status].get(min_coef, 0)
        else:
            t1_status = t2_status = "NO DATA"           # need to remake

        return {
            t1_status: int(t1_value),
            t2_status: int(t2_value)
        }

    status_vs_handicap = get_status_vs_value(t1_coef, t2_coef)



    def decorator_for_bet(func):
        def wrapper(*args,**kwargs):
            value, total_value = func(*args,**kwargs)
            if total_value > 60:
                if total_value - value < 5:
                    return True
        return wrapper

    t1_status = "FAVORIT" if t1_coef <= t2_coef else "UNDERDOG"
    t2_status = "UNDERDOG" if t1_coef < t2_coef else "FAVORIT"

    # @decorator_for_bet
    def Case_Favorite_Win_1of4(matches):
        h = status_vs_handicap['FAVORIT']
        total_matches = len(matches); win = 0
        for g in matches:
                location = g[-1]
                if location == 'HOME':
                    if g[0] > g[1] + h or g[2] > g[3] + h or g[4] > g[5] + h or g[6] > g[7] + h:
                        win += 1
                else:
                    if g[0] + h < g[1] or g[2] + h < g[3] or g[4] + h < g[5] or g[6] + h < g[7]:
                        win += 1
        return [win, total_matches]


    # @decorator_for_bet
    def Case_Underdog_Lose_1of4(matches):
        h = status_vs_handicap['FAVORIT']
        total_matches = len(matches)
        lose = 0
        for g in matches:
            location = g[-1]
            if location == 'HOME':
                if g[0] <= g[1] - h or g[2] <= g[3] - h or g[4] <= g[5] - h or g[6] <= g[7] - h:
                    lose += 1
            else:
                if g[0] >= g[1] + h or g[2] >= g[3] + h or g[4] >= g[5] + h or g[6] >= g[7] + h:
                    lose += 1

        return [lose, total_matches]

    betflag1 = betflag2 = None
    if t1_coef <= t2_coef:
        case1 = Case_Favorite_Win_1of4(team1_scores)
        case2 = Case_Underdog_Lose_1of4(team2_scores)
        if case1[1] > 50 and case2[1] > 50:
            if case1[1] - case1[0] < 6 and case2[1] - case2[0] < 6:
                print(url)
                betflag1 = True
        print(case1)
        print(case2)


    else:
        case1 = Case_Favorite_Win_1of4(team2_scores)
        case2 = Case_Underdog_Lose_1of4(team1_scores)
        if case1[1] > 50 and case2[1] > 50:
            if case1[1] - case1[0] < 6 and case2[1] - case2[0] < 6:
                print(url)
                betflag2 = True
        print(case1)
        print(case2)


    if betflag1 or betflag2:
        bet2 = (str(case1),str(case2),title,
                str(team1_name), str(team2_name),
                url)
        bets += bet2


    def each_total(data, case=None):
        if case == 'quarter':
            denominator = len(data)*4
        else:
            denominator = len(data)
        return sum([sum(i[:8]) for i in data]) / denominator






    average_per_quarter = ceil(each_total(team1_scores, 'quarter')/2 + each_total(team2_scores, 'quarter')/2)
    avarage_per_match = ceil(each_total(team1_scores)/2 + each_total(team2_scores)/2)
    print(avarage_per_match, url)
    # print(average_per_quarter)
    team1_total_series = concatenate_matches(get_quarters_totals_series(team1_scores, average_per_quarter))
    team2_total_series = concatenate_matches(get_quarters_totals_series(team2_scores, average_per_quarter))
    team1_total_match_series = get_total_series(team1_scores, avarage_per_match)
    print('answer',count_max_consecutive_O_U(team1_total_match_series)) ### stop here 31.05
    # print(team1_total_series)
    # print(team2_total_series)
    team1_last_total_series = get_last_games_series(team1_total_series)
    team2_last_total_series = get_last_games_series(team2_total_series)
    # print(team1_last_total_series)
    # print(team2_last_total_series)
    team1_O_U_consecutive = count_max_consecutive_O_U(team1_total_series)
    team2_O_U_consecutive = count_max_consecutive_O_U(team2_total_series)
    # print(team1_O_U_consecutive)
    # print(team2_O_U_consecutive)

    if team1_last_total_series[0]>=3 or team2_last_total_series[0]>=3:
        print('TEAM1 QUARTER SERIES OVER / UNDER:: ', *team1_O_U_consecutive,'LAST SERIES:',*team1_last_total_series)
        print('TEAM2 QUARTER SERIES OVER / UNDER:: ', *team2_O_U_consecutive,'LAST SERIES:',*team2_last_total_series)
        print('TOTAL VALUE::', average_per_quarter)
        print(title)
        print(team1_name)
        print(team2_name)
        print(url)
        bet3 = ('TEAM1 QUARTER SERIES OVER / UNDER::', team1_O_U_consecutive,
                'LAST SERIES:',' '.join(map(str,team1_last_total_series)),'TEAM2 QUARTER SERIES OVER / UNDER:: '
                ,team2_O_U_consecutive,'LAST SERIES:',' '.join(map(str,team2_last_total_series)),title,
                str(team1_name), str(team2_name),
                url)
        bets += bet3
        print('----------')

    if len(bets)> 1:
        send_to_tg(bets)

    print()

for url, coefs in schedule.items():
    try:
        main(url, coefs)
    except:
        continue
