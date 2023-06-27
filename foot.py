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
            matches = self.browser.find_elements(By.CSS_SELECTOR, "[id^='g_1']")
            checklist = dict()

            for match in matches:
                link = match.get_attribute("id")
                url_match = f"https://www.soccer24.com/match/{link[4:]}"
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


url = "https://www.soccer24.com"
scraper = ScheduleScraper(url)
schedule = scraper.scrape()






def main(url):

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
    print(title,'\n', team_home,team_away)


    def separator(matches):
        match_list = list()
        for i in matches:
            line =[j.strip('()') for j in  i.text.split()]
            if "Awrd" in line or "Cancelled" in line or 'Postponed' in line:
                continue
            match_list.append(line)
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
            dataset = browser.find_elements(By.CSS_SELECTOR, "[id^='g_1']")
            matches = separator(dataset)
            team = browser.find_element(By.CSS_SELECTOR, "div.heading__name").get_attribute("innerHTML")
        return matches, [team_name.strip('()') for team_name in team.split()]

    def forming(browser, link1, link2):  # NEED ADD TYPE SPORT AND FIXABLE CSS SELECTOR
        match_list_home, team1 = get_data(browser,link1)
        match_list_away, team2 = get_data(browser,link2)
        return match_list_home, match_list_away, team1, team2

    games = forming(browser, team_home, team_away)
    team1_results = games[0]
    team2_results = games[1]
    team1_name = games[2]
    team2_name = games[3]
    print(team1_name, team2_name)
    print(team1_results)
    print(team2_results)



    def mark_home_away(team, all_matches):
        marked_list = []
        waste = ["W", "U18", "U19", "U20", "U21", "U22", "U23"]
        for i in waste:
            if i in team:
                team = [j for j in team if j not in waste]
        # print(team)
        for match in all_matches:
            matchline = [j for j in match[:len(match) - 1] if j not in waste] + match[-1:]
            # print(matchline)
            # print(team)
            team_index = matchline.index(team[len(team) - 1])

            # print()
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
            if len([i for i in match if i.isdigit()]) < 4:
                continue
            if "After" in match:
                scoreline = match[-8:-4] + match[-1:]
            else:
                scoreline = match[-6:-2] + match[-1:]
            scorelines.append([i if not i.isdigit() else int(i) for i in scoreline])

        return scorelines


    def get_all_series(matches):
        win_lost_series = []

        for match in matches:
            location = match[-1]
            match_scores = match[:2]
            first_half = match[2:4]; total_first_half = sum(first_half)
            second_half = [match_scores[0] - first_half[0], match_scores[1] - first_half[1]];
            total_second_half = sum(second_half)







            # for q in results:
            #     if location == 'HOME':
            #         win_lost_series.append('W' if q[0] > q[1] else ('L' if q[0] < q[1] else 'D'))
            #
            #     elif location == 'AWAY':
            #         win_lost_series.append('W' if q[0] < q[1] else ('L' if q[0] > q[1] else 'D'))

        return win_lost_series



    team1_scores = mark_home_away(team1_name, team1_results)
    team2_scores = mark_home_away(team2_name, team2_results)
    series1 = get_matches_winlost_series(team1_scores)
    series2 = get_matches_winlost_series(team2_scores)
    print(team1_scores)
    print(series1)
    print(team2_scores)
    print(series2)






for i in schedule:
    main(i)