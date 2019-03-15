import socket
import socks
import pika
import re
# After we configured socks5
from urllib.request import urlopen
from urllib.parse import urlsplit, urlunsplit
from bs4 import BeautifulSoup
# from multiprocessing import Pool


def is_url(link):
    # checks using regex if 'link' is a valid url
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*/\\,() ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', link)
    return " ".join(url) == link


def create_connection(addr, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(addr)
    return sock


def set_proxy():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9150, True)
    socket.socket = socks.socksocket
    socket.create_connection = create_connection

'''

def produce_message(message, i):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    channel.exchange_declare(exchange='web_crawler', exchange_type='direct')
    channel.basic_publish(exchange='web_crawler',
                          routing_key='crawler_{}'.format(i),
                          body=message,
                          properties=pika.BasicProperties(delivery_mode=2))
    connection.close()


def new_message(ch, method, properties, body):
    print('New message: {}'.format(body))


def consume_message(i):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    channel.exchange_declare(exchange='web_crawler', exchange_type='direct')
    channel.queue_bind(exchange='web_crawler',
                      queue='task_queue',
                      routing_key='crawler_{}'.format(i))
    channel.basic_consume(new_message,
                          queue='task_queue',
                          no_ack=True)
    channel.start_consuming()
    
 for i in range(2):
    message = 'http://check.torproject.org?key={}'.format(i)
    produce_message(message, i)

pool = Pool(processes=40)
pool.map(start_crawler)

 '''


listUrl = []


def save_file(text):
    f = open('crawler.txt', 'a')
    f.write(text)
    f.close()


def domain_url(url):
    split_url = urlsplit(url)
    return split_url.netloc


def read_url(url, depth):
    if depth == 5:
        return url
    else:
        page = urlopen(url)
        soup = BeautifulSoup(page.read(), 'html.parser')
        links = soup.find_all('a')
        if links is None or len(links) == 0:
            return 1;
        else:

            for link in links:
                url_base = link['href'] if is_url(link['href']) else url + '/' + link['href']

                if is_url(url_base):
                    if url_base not in listUrl:
                        save_file('{};{}\n'.format(url_base, soup.title.get_text()))
                        print('{};{}\n'.format(url_base, soup.title.get_text()))
                        listUrl.append(url_base)
                        read_url(url_base, depth+1)


def start_crawler():
    # consume_message(i)
    read_url('https://dogolachhhnaqa7n.onion', 0)


if __name__ == '__main__':
    set_proxy()
    start_crawler()
