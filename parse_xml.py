from typing import TextIO
from lxml import etree
from pprint import pprint

from zavod import Zavod, init_context

EXAMPLE_URL = "https://egrul.itsoft.ru/7709383684.xml"


def parse_company(context: Zavod, el):
    entity = context.make("Company")
    entity.id = context.make_slug("ogrn", el.get("ОГРН"))
    entity.add("jurisdiction", "ru")
    entity.add("ogrnCode", el.get("ОГРН"))
    entity.add("innCode", el.get("ИНН"))
    entity.add("kppCode", el.get("КПП"))
    entity.add("legalForm", el.get("ПолнНаимОПФ"))
    entity.add("incorporationDate", el.get("ДатаОГРН"))

    for name_el in el.findall("./СвНаимЮЛ"):
        entity.add("name", name_el.get("НаимЮЛПолн"))
        entity.add("name", name_el.get("НаимЮЛСокр"))

    pprint(entity.to_dict())


## FOUnder:
# <СвУчредит>
# <УчрФЛ>
# <ГРНДатаПерв ГРН="2047709040180" ДатаЗаписи="2004-06-25"/>
# <СвФЛ Фамилия="ТАРАСОВ" Имя="ИГОРЬ" Отчество="АЛЕКСАНДРОВИЧ" ИННФЛ="770300584079">
# <ГРНДата ГРН="2047709040180" ДатаЗаписи="2004-06-25"/>
# </СвФЛ>
# <ДоляУстКап НоминСтоим="10000">
# <РазмерДоли>
# <Процент>100</Процент>
# </РазмерДоли>
# <ГРНДата ГРН="7137747735085" ДатаЗаписи="2013-09-10"/>
# </ДоляУстКап>
# </УчрФЛ>
# </СвУчредит>


def parse_sole_trader(context: Zavod, el):
    pass


def parse_xml(context: Zavod, handle: TextIO):
    doc = etree.parse(handle)
    for el in doc.findall(".//СвЮЛ"):
        parse_company(context, el)
    for el in doc.findall(".//СвИП"):
        parse_sole_trader(context, el)


def parse(context: Zavod):
    path = context.fetch_resource("example.xml", EXAMPLE_URL)
    with open(path, "r") as fh:
        parse_xml(context, fh)


if __name__ == "__main__":
    with init_context("ru_egrul", "ru") as context:
        parse(context)
