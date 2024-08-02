import requests as rq

from bs4 import BeautifulSoup , NavigableString

from playwright.sync_api import sync_playwright

flip_URL = 'https://www.flipkart.com/laptops/pr?sid=6bo,b5g&otracker=categorytree&fm=neo%2Fmerchandising&iid=M_c0b2bdd4-d847-40ec-8cb9-0b80f6522ad8_1_372UD5BXDFYS_MC.34WHNYFH5V2Y&otracker=hp_rich_navigation_8_1.navigationCard.RICH_NAVIGATION_Electronics~Laptop%2Band%2BDesktop_34WHNYFH5V2Y&otracker1=hp_rich_navigation_PINNED_neo%2Fmerchandising_NA_NAV_EXPANDABLE_navigationCard_cc_8_L1_view-all&cid=34WHNYFH5V2Y'

flip_resp = rq.get(flip_URL)

print('URL status code :- ' ,flip_resp.status_code)

print('---------------------------------------------------------------------------------------------')

bSoup = BeautifulSoup(flip_resp.content , 'html.parser')

def removeExtra(itration):
    return list(filter(lambda x: type(x) != NavigableString, itration))

# print(bSoup.prettify())

def scrape_lap (lap_page) :
    all_divs = lap_page.find_all('div' , attrs = 'col col-7-12' )
    print('Number of laptops in lap page :-' , len(all_divs))
    print('---------------------------------------------------------------------------------------------')
    # print(list(all_divs[0].children))   #----------NO NavigableString here. Why ??-------------
    # print(list(all_divs[0].children)[1].getText())


if __name__ == '__main__' :
    with sync_playwright() as p :
        browser = p.chromium.launch(headless=False)

        page = browser.new_page()
        page.goto(flip_URL)

        page.wait_for_load_state('networkidle')
        page.evaluate('()=> window.scroll(0,document.body.scrollHeight)')
        page.screenshot(path='flip_lap.png' , full_page=True)

        lap_html = page.inner_html('body')
        # print(lap_html)
        
        bSoup = BeautifulSoup(lap_html , 'html.parser')
        # print(bSoup.prettify())

        scrape_lap(bSoup)

lap_list = bSoup.find_all('div' , attrs='cPHDOP col-12-12')
print('Total (div class= cPHDOP col-12-12 :-' ,len(lap_list))
print('---------------------------------------------------------------------------------------------')
# print(lap_list[2])


# TITLE
# print(removeExtra(lap_list[2].find('div' , attrs='col col-7-12').children)[1].getText())

# Rating
print(removeExtra(lap_list[2].find('div' , attrs='col col-7-12').children)[2].div.getText())
print('---------------------------------------------------------------------------------------------')

#Price
# print(lap_list[2].find('div' , attrs='col col-5-12 BfVC2z').div.div.div.getText())

def getTRP (lap) :
    return {
        'Title' : removeExtra(lap.find('div' , attrs='col col-7-12').children)[1].getText() ,
        'Rating' : removeExtra(lap.find('div' , attrs='col col-7-12').children)[2].find('div').getText() ,
        'Price' : lap.find('div' , attrs='col col-5-12 BfVC2z').div.div.div.getText()
    }


laptop_data = [ getTRP(lap)  for lap in lap_list[2:26]]

print(laptop_data)
