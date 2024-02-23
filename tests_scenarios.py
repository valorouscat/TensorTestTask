import logging
import Pages

logging.getLogger(__name__)

def test_1(browser):
    # 1)
    sbis_main_page = Pages.SBISMainPage(browser)
    sbis_main_page.go_to_site()
    sbis_main_page.click_to_header('Контакты')
    
    # 2)
    sbis_contact_page = Pages.SBISContactPage(browser)
    sbis_contact_page.click_to_the_logo()

    # 3-4)
    tensor_main_page = Pages.TensorMainPage(browser)
    wanted_card = tensor_main_page.check_card(cards=tensor_main_page.find_cards(), card_text='Сила в людях')
    assert wanted_card is not None

    # 5)
    tensor_main_page.click_to_the_detail_link(wanted_card)
    tensor_about_page = Pages.TensorAboutPage(browser)
    assert 'https://tensor.ru/about' == tensor_about_page.get_url()

    # 6)
    assert tensor_about_page.check_photos('Работаем')

def test_2(browser):
    # 1)
    sbis_main_page = Pages.SBISMainPage(browser)
    sbis_main_page.go_to_site()
    sbis_main_page.click_to_header('Контакты')
    
    # 2)
    sbis_contact_page = Pages.SBISContactPage(browser)
    assert 'Амурская обл.' == sbis_contact_page.check_region_chooser().text
    original_parnters = sbis_contact_page.check_partners_list()
    assert len(original_parnters) > 0

    # 3)
    sbis_contact_page.change_region('Камчатский край')

    # 4)
    assert 'Камчатский край' == sbis_contact_page.check_region_chooser().text
    assert sbis_contact_page.check_partners_list() != original_parnters
    assert '41-kamchatskij-kraj' in sbis_contact_page.get_url()
    assert 'Камчатский край' in sbis_contact_page.get_title()
 
def test_3(browser):
    # 1)
    sbis_main_page = Pages.SBISMainPage(browser)
    sbis_main_page.go_to_site()

    # 2)
    sbis_main_page.click_to_footer('Скачать')

    # 3)
    sbis_download_page = Pages.SBISDownloadPage(browser)
    sbis_download_page.click_vertical_menu('СБИС Плагин')
    assert 'plugin' in sbis_download_page.get_url()
    sbis_download_page.switch_os('Windows')
    assert 'default' in sbis_download_page.get_url()
    download_link = sbis_download_page.click_download_link('Веб-установщик')

    # 4-5)
    downloaded_file_check = sbis_download_page.wait_for_download(download_dir='\\downloads', file_name=download_link['name'], file_size=float(download_link['size']))
    assert downloaded_file_check