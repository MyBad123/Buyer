import os
from celery import shared_task
import requests
import datetime
import pathlib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email_validate import validate
from .ParseLib.Tables import TemplateTable
from .ParseLib.Tables import SiteTable

from app.models import RequestModel, ResultModel
from .for_task_utils import Mail


def control_mail(mail: str):
    """control mail: valid or no"""

    if type(mail) != str:
        return False

    if not validate(email_address=mail, check_blacklist=False):
        return False

    return True


@shared_task
def wow(id_obj):
    request_object = RequestModel.objects.get(id=id_obj)
    request_object.datetime_site_parsing_started = datetime.datetime.now()
    request_object.save()

    for_i = 0
    for i in ResultModel.objects.filter(request=request_object):
        if for_i < 10:
            i.status = True
            i.mail = 'buyer-vendor@1d61.com'
            i.save()

        for_i += 1

    request_object.datetime_processing_finished = datetime.datetime.now()
    request_object.save()

    # send message to mail
    if request_object.creator is not None and control_mail(request_object.creator.username):
        mail_msg = MIMEMultipart()
        mail_msg['Subject'] = 'Заявка обработана'
        mail_message = 'Ваша заявка обработана'
        mail_msg.attach(MIMEText(mail_message, 'plain'))
        mail_server = smtplib.SMTP('m.1d61.com: 587')
        mail_server.starttls()
        mail_server.login(
            os.environ.get('from', 'buyer-support@1d61.com'),
            os.environ.get('password', 'AJds38Adj3FSDl3as4')
        )
        mail_server.sendmail(
            os.environ.get('from', 'buyer-support@1d61.com'),
            request_object.creator.username,
            mail_msg.as_string()
        )
        mail_server.quit()


def get_csv(data, csv_model_id):
    """parce site and send message to client"""

    # get data for working
    mail = data.get('mail')
    url = data.get('url')

    # create path for csv file
    path_name = str(pathlib.Path(__file__).parent) + '/files/'
    if not os.path.exists(path_name):
        os.mkdir(path_name)

    path_name += str(csv_model_id) + '/'
    if not os.path.exists(path_name):
        os.mkdir(path_name)

    # send message about starting
    mail_object = Mail(mail, path_name)
    mail_object.send_start_mail()

    # work with lib
    from .ParseLib.parser_starting import start
    path_obj = start(path_name, url, str(csv_model_id))

    # send file to
    mail_object.send_file_mail(path_obj)
    os.remove(path_obj)
    try:
        os.rmdir(f"{str(pathlib.Path(__file__).parent)}/files/{str(csv_model_id)}/")
    except Exception as ex:
        print(f"Exception with os.rmdir: {ex}")


def get_catalog(data):
    """get catalog"""
    url = data.get('url')

    # create path for csv file
    path_name = str(pathlib.Path(__file__).parent) + '/files/'
    if not os.path.exists(path_name):
        os.mkdir(path_name)

    path_name += 'catalog/'
    if not os.path.exists(path_name):
        os.mkdir(path_name)

    siteTable = SiteTable()
    import re
    domain = re.findall(r'([\w\-:]+)\/\/', url)[0] + '//' + re.findall(r'\/\/([\w\-.]+)', url)[0]
    domain_without = max(domain.split("//")[-1].split("/")[0].split("."), key=len).replace('-', '_')
    row = siteTable.select(param={"url": url})
    dict_url = {}
    if not row:
        pass
    else:
        import pandas as pd
        templateTable = TemplateTable()
        site_id = row[0]['id']
        df = pd.DataFrame(data=None, columns=["nn", "class"])
        for elDic in templateTable.select(param={"site_id": site_id}):
            new_row = pd.DataFrame(
                [{"text": elDic['text'], "presence_of_ruble": elDic['presence_of_ruble'],
                  "content_element": elDic['content_element'], "url": elDic['url'],
                  "length": elDic['length'],
                  "class_ob": elDic['class_ob'], "id_element": elDic['id_element'],
                  "style": elDic['style'],
                  "enclosure": elDic['enclosure'], "href": elDic['href'], "count": elDic['count'],
                  "location_x": elDic['location_x'], "location_y": elDic['location_y'],
                  "size_width": elDic['size_width'], "size_height": elDic['size_height'],
                  "integer": elDic['integer'], "float": elDic['float'], "n_digits": elDic['n_digits'],
                  "presence_of_vendor": elDic['presence_of_vendor'],
                  "presence_of_link": elDic['presence_of_link'],
                  "presence_of_at": elDic['presence_of_at'], "has_point": elDic['has_point'],
                  "writing_form": elDic['writing_form'], "font_size": elDic['font_size'],
                  "hue": elDic['hue'],
                  "saturation": elDic['saturation'], "brightness": elDic['brightness'],
                  "font_family": elDic['font_family'],
                  "ratio_coordinate_to_height": elDic['ratio_coordinate_to_height'],
                  "distance_btw_el_and_ruble": elDic['distance_btw_el_and_ruble'],
                  "distance_btw_el_and_article": elDic['distance_btw_el_and_article'],
                  "id_xpath": str(elDic['content_element']) + "//" + str(elDic['path']) + "//" + str(elDic['url']),
                  "source": elDic["source"]}])
            df = pd.concat([df, new_row])
        path = os.path.join(path_name, f"{domain_without}.csv")
        df.to_csv(path)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = 'path=https://buyerdev.1d61.com/get-csv-file/?id=catalog'
        try:
            r = requests.post('http://localhost:8000', headers=headers, data=data)
            el_class = r.json()['classes']
            dictionary_class = {
                0: "не определено",
                1: "название",
                2: "цена",
                3: "описание",
                4: "артикул",
                5: "телефон",
                6: "e-mail"
            }
            el_class = list(map(lambda cl: dictionary_class[int(cl)], el_class))
            df["class"] = el_class
            for url_el in df['url'].unique():
                dictionary_class = {
                    "название": None,
                    "цена": None,
                    "описание": None,
                    "артикул": None
                }
                for name_dic in dictionary_class.keys():
                    try:
                        df.loc[df['url'] == url_el and df['class'] == name_dic][:1]['text']
                    except:
                        pass
                dictionary_class["изображение"] = df.loc[df['url'] == url_el
                                                         and df['content_element'] == 'img'][:1]['source']
                dict_url[url_el] = dictionary_class
        except Exception as ex:
            print(log := f"exception with request: {ex}")

        os.remove(path)
    return dict_url
