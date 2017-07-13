# -*- coding: utf-8 -*-

import re
import scrapy
from v_crawler.items import CarItem


class otomotoSpider(scrapy.Spider):
    name = 'otomotoSpider'
    allowed_domains = ['otomoto.pl']
    
    
    def start_requests(self):
        start_urls = ['https://www.otomoto.pl/osobowe/?search%5Bcountry%5D=polska&search%5Bnew_used%5D=used&l=1&page=' + str(x) for x in range(7021)]
        for url in start_urls:
            yield scrapy.Request(url = url, callback = self.parse_page)
       
            
    def parse_page(self, response):
        hrefs = response.xpath('//div[@class="offer-item__content"]/div[@class="offer-item__title"]/h2/a/@href')
        for href in hrefs:
            yield scrapy.Request(url = href.extract(), callback = self.parse_car)
            
            
    def parse_car(self, response):
        parameters = response.xpath('//ul[@class="offer-params__list"]/li')
        parsed_parameters = {}
        
        for parameter in parameters:
            type = parameter.xpath('./span/text()').extract_first()
            
            if type is not None:
                if u'skokowa' in type:
                    type = type.split(' ')[1]
                if u'Skrzynia' in type:
                    type = type.split(' ')[0]
                    
     
            value = parameter.xpath('./div/text()').extract_first()
            if value is not None and len(value.strip()) == 0:
                value = parameter.xpath('./div/a/text()').extract_first()
                
            if value is not None:
                value = value.strip()
                    
            parsed_parameters[type] = value
            
            final_parameters = {'Oferta od': '',
             'Kategoria':'',
             'Marka':'',
             'Model':'',
             'Kod Silnika':'',
             'Wersja':'',
             'Rok produkcji':'',
             'Przebieg':'',
             'skokowa':'',
             'Rodzaj paliwa':'',
             'Moc':'',
             'Skrzynia': '',
             #'Napęd':'',
             'Typ':'',
             'Liczba miejsc':'',
             'Liczba drzwi':'',
             'Kolor':'',
             'Stan':'',
             'Uszkodzony': ''}
             
            final_parameters.update(parsed_parameters)
            
        price = response.xpath('//div[@class="offer-price"]/span[@class="offer-price__number"]/text()').extract_first()
        price = price.replace(' ', '')
        currency = response.xpath('//div[@class="offer-price"]/span[@class="offer-price__number"]/span[@class="offer-price__currency"]/text()').extract_first()
        
        if currency == 'EUR':
            converted_price = 4.23 * int(price)
            price = str(converted_price)
        
        # creating scrapy items
        car = CarItem() 
        
        if final_parameters['Oferta od'] == 'Osoby prywatnej':
            final_parameters['Oferta od'] = 'Osoba prywatna'
        else:
            final_parameters['Oferta od'] = 'Firma'
            
        car['seller'] = final_parameters['Oferta od']
        car['category'] = final_parameters['Kategoria']
        car['make'] = final_parameters['Marka']
        car['model'] = final_parameters['Model']
        car['production_year'] = final_parameters['Rok produkcji']
        car['mileage'] = final_parameters['Przebieg'].replace('km', '').replace(' ', '')
        car['engine_volume'] = final_parameters['skokowa'].replace('cm3', '').replace(' ', '')
        car['fuel'] = final_parameters['Rodzaj paliwa']
        car['horse_power'] = final_parameters['Moc'].replace('KM', '').replace(' ', '')
        
        if u'Automatyczna' in final_parameters['Skrzynia']:
            final_parameters['Skrzynia'] = 'Automatyczna'
            
        car['transimission'] = final_parameters['Skrzynia']
        car['car_type'] = final_parameters['Typ']
        car['seats_number'] = final_parameters['Liczba miejsc']
        car['doors_number'] = final_parameters['Liczba drzwi']
        car['colour'] = final_parameters['Kolor']
        
        try:
            car['version']= re.search(r'[ (].+', '', final_parameters['Wersja'])
        except TypeError:
            pass
            
        try:
            car['engine_code'] = final_parameters['Kod silnika']
        except KeyError:
            car['engine_code'] = ''
        

        if final_parameters['Uszkodzony'] == 'Tak':
            car['condition'] = 'Damaged'
        else:
            car['condition'] = 'Fine'
            
        car['price'] = price
        car['url'] = response.url
        
        yield car
        