from urllib.parse import urljoin, urlparse
from zipfile import ZipFile
from lxml import etree, html
from pprint import pprint
from typing import BinaryIO, Optional, Set
from lxml.etree import _Element as Element, tostring
from zavod import Zavod, init_context
from followthemoney.proxy import EntityProxy
from followthemoney.util import join_text

INN_URL = "https://egrul.itsoft.ru/%s.xml"
PREFIX = "https://egrul.itsoft.ru/EGRUL_406/01.01.2022_FULL/"


def tag_text(el: Element) -> str:
    return tostring(el, encoding="utf-8").decode("utf-8")


def make_id(
    context: Zavod, entity: EntityProxy, local_id: Optional[str] = None
) -> Optional[str]:
    # FIXME: should we make INN slugs if the nationality is not Russian?
    for inn in sorted(entity.get("innCode", quiet=True)):
        return context.make_slug("inn", inn)
    for ogrn in sorted(entity.get("ogrnCode", quiet=True)):
        return context.make_slug("ogrn", ogrn)
    if local_id is not None:
        # If no INN is present, make a fake entity ID:
        for name in sorted(entity.get("name")):
            return context.make_id(local_id, name)
    return None


def make_person(context: Zavod, el: Element, local_id: str) -> EntityProxy:
    entity = context.make("Person")
    last_name = el.get("Фамилия")
    first_name = el.get("Имя")
    patronymic = el.get("Отчество")
    name = join_text(first_name, patronymic, last_name)
    entity.add("name", name)
    entity.add("firstName", first_name)
    entity.add("fatherName", patronymic)
    entity.add("lastName", last_name)
    entity.add("innCode", el.get("ИННФЛ"))
    entity.id = make_id(context, entity, local_id)
    return entity


def make_org(context: Zavod, el: Element, local_id: str) -> EntityProxy:
    entity = context.make("Organization")
    name_el = el.find("./НаимИННЮЛ")
    if name_el is not None:
        entity.add("name", name_el.get("НаимЮЛПолн"))
        entity.add("innCode", name_el.get("ИНН"))
        entity.add("ogrnCode", name_el.get("ОГРН"))

    name_latin_el = el.find("./СвНаимЮЛПолнИн")
    if name_latin_el is not None:
        entity.add("name", name_latin_el.get("НаимПолн"))

    foreign_reg_el = el.find("./СвРегИн")
    if foreign_reg_el is not None:
        entity.add("jurisdiction", foreign_reg_el.get("НаимСтран"))
        entity.add("registrationNumber", foreign_reg_el.get("РегНомер"))
        entity.add("publisher", foreign_reg_el.get("НаимРегОрг"))
        entity.add("address", foreign_reg_el.get("АдрСтр"))

    entity.id = make_id(context, entity, local_id)
    return entity


def apply_person_country(person: EntityProxy, el: Element):
    country = el.find("./СвГраждФЛ")
    if country is None:
        return

    if country.get("КодГражд") == "1":
        person.add("country", "ru")

    person.add("country", country.get("НаимСтран"))


def parse_founder(context: Zavod, company: EntityProxy, el: Element):
    owner = context.make("LegalEntity")
    ownership = context.make("Ownership")

    meta = el.find("./ГРНДатаПерв")
    local_id = company.id
    if meta is not None:
        ownership.add("startDate", meta.get("ДатаЗаписи"))
        local_id = meta.get("ГРН")

    if el.tag == "УчрФЛ":  # Individual founder
        name_el = el.find("./СвФЛ")
        if name_el is not None:
            owner = make_person(context, name_el, local_id)

        apply_person_country(owner, el)
    elif el.tag == "УчрЮЛИн":  # Foreign company
        owner = make_org(context, el, local_id)
    elif el.tag == "УчрЮЛРос":  # Russian legal entity
        # print(tag_text(el))
        owner = make_org(context, el, local_id)
    elif el.tag == "УчрПИФ":  # Mutual investment fund
        # TODO: nested ownership structure, make Security
        # owner = context.make("Security")
        # FIXME: Security cannot own.
        fund_name_el = el.find("./СвНаимПИФ")
        if fund_name_el is not None:
            # owner.add("name", fund_name_el.get("НаимПИФ"))
            ownership.add("summary", fund_name_el.get("НаимПИФ"))

        manager_el = el.find("./СвУпрКомпПИФ/УпрКомпПиф")
        if manager_el is not None:
            owner.add("name", manager_el.get("НаимЮЛПолн"))
            owner.add("innCode", manager_el.get("ИНН"))
            owner.add("ogrnCode", manager_el.get("ОГРН"))
            owner.id = make_id(context, owner, local_id)
    elif el.tag == "УчрРФСубМО":  # Russian public body
        pb_name_el = el.find("./ВидНаимУчр")
        if pb_name_el is not None:
            # Name of the owning authority
            ownership.add("role", pb_name_el.get("НаимМО"))

        # managing body:
        pb_el = el.find("./СвОргОсущПр")
        if pb_el is not None:
            owner = make_org(context, pb_el, local_id)
    elif el.tag == "УчрДогИнвТов":  # investment partnership agreement.
        # FIXME: should the partnership be its own entity?
        terms_el = el.find("./ИнПрДогИнвТов")
        if terms_el is not None:
            ownership.add("summary", terms_el.get("НаимДог"))
            ownership.add("recordId", terms_el.get("НомерДог"))
            ownership.add("date", terms_el.get("Дата"))

        # managing vehicle
        manager_el = el.find("./СвУпТовЮЛ")
        if manager_el is not None:
            owner.add("name", manager_el.get("НаимЮЛПолн"))
            owner.add("innCode", manager_el.get("ИНН"))
            owner.add("ogrnCode", manager_el.get("ОГРН"))
            owner.id = make_id(context, owner, local_id)
    else:
        context.log.warn("Unknown owner type", tag=el.tag)
        return

    if owner.id is None:
        return

    # pprint(owner.to_dict())
    context.emit(owner)

    ownership.id = context.make_id(company.id, owner.id)
    ownership.add("owner", owner)
    ownership.add("asset", company)

    share_el = el.find("./ДоляУстКап")
    if share_el is not None:
        ownership.add("sharesCount", share_el.get("НоминСтоим"))
        percent_el = share_el.find("./РазмерДоли/Процент")
        if percent_el is not None:
            ownership.add("percentage", percent_el.text)

    reliable_el = el.find("./СвНедДанУчр")
    if reliable_el is not None:
        ownership.add("summary", reliable_el.get("ТекстНедДанУчр"))

    # pprint(ownership.to_dict())
    context.emit(ownership)


def parse_directorship(context: Zavod, company: EntityProxy, el: Element):
    name = el.find("./СвФЛ")
    if name is None:
        # context.log.warn("Directorship has no person", company=company.id)
        return
    # TODO: can we use the ГРН as a fallback ID?
    director = make_person(context, name, company.id)

    # TODO: move this into make_person?
    apply_person_country(director, el)

    context.emit(director)

    role = el.find("./СвДолжн")
    if role is None:
        context.log.warn("Directorship has no role", tag=tag_text(el))
        return

    directorship = context.make("Directorship")
    directorship.id = context.make_id(company.id, director.id, role.get("ВидДолжн"))
    directorship.add("role", role.get("НаимДолжн"))
    directorship.add("summary", role.get("НаимВидДолжн"))
    directorship.add("director", director)
    directorship.add("organization", company)

    date = el.find("./ГРНДатаПерв")
    if date is not None:
        directorship.add("startDate", date.get("ДатаЗаписи"))

    context.emit(directorship)


def parse_company(context: Zavod, el: Element):
    entity = context.make("Company")
    entity.id = context.make_slug("inn", el.get("ИНН"))
    entity.add("jurisdiction", "ru")
    entity.add("ogrnCode", el.get("ОГРН"))
    entity.add("innCode", el.get("ИНН"))
    entity.add("kppCode", el.get("КПП"))
    entity.add("legalForm", el.get("ПолнНаимОПФ"))
    entity.add("incorporationDate", el.get("ДатаОГРН"))

    email_el = el.find("./СвАдрЭлПочты")
    if email_el is not None:
        entity.add("email", email_el.get("E-mail"))

    citizen_el = el.find("./СвГражд")
    if citizen_el is not None:
        entity.add("country", citizen_el.get("НаимСтран"))

    # TODO: address:
    # * СвАдрЮЛФИАС
    # * СвАдресЮЛ / АдресРФ
    for addr_el in el.findall("./СвАдресЮЛ/*"):
        if addr_el.tag == "АдресРФ":  # normal address
            pass
        elif addr_el.tag == "СвМНЮЛ":  # location of legal entity
            pass
        elif addr_el.tag == "СвАдрЮЛФИАС":
            pass
        elif addr_el.tag == "СвНедАдресЮЛ":  # missing address
            pass
        elif addr_el.tag == "СвРешИзмМН":  # address change
            pass
        else:
            print(tag_text(addr_el))

    for name_el in el.findall("./СвНаимЮЛ"):
        entity.add("name", name_el.get("НаимЮЛПолн"))
        entity.add("name", name_el.get("НаимЮЛСокр"))

    entity.id = make_id(context, entity)

    # prokura or directors etc.
    for director in el.findall("./СведДолжнФЛ"):
        parse_directorship(context, entity, director)

    for founder in el.findall("./СвУчредит/*"):
        parse_founder(context, entity, founder)

    # pprint(entity.to_dict())
    context.emit(entity)


def parse_sole_trader(context: Zavod, el: Element):
    entity = context.make("LegalEntity")
    entity.add("country", "ru")
    entity.add("ogrnCode", el.get("ОГРНИП"))
    entity.add("innCode", el.get("ИННФЛ"))
    entity.add("legalForm", el.get("НаимВидИП"))

    entity.id = make_id(context, entity)
    context.emit(entity)


def parse_xml(context: Zavod, handle: BinaryIO):
    doc = etree.parse(handle)
    for el in doc.findall(".//СвЮЛ"):
        parse_company(context, el)
    for el in doc.findall(".//СвИП"):
        parse_sole_trader(context, el)


def parse(context: Zavod):
    for inn in ["7709383684", "7704667322", "9710075695"]:
        path = context.fetch_resource("%s.xml" % inn, INN_URL % inn)
        with open(path, "rb") as fh:
            parse_xml(context, fh)


def crawl_index(context: Zavod, url: str) -> Set[str]:
    archives: Set[str] = set()
    res = context.http.get(url)
    doc = html.fromstring(res.text)
    for a in doc.findall(".//a"):
        link_url = urljoin(url, a.get("href"))
        if not link_url.startswith(url):
            continue
        if link_url.endswith(".zip"):
            archives.add(link_url)
            continue
        archives.update(crawl_index(context, link_url))
    return archives


def crawl_archive(context: Zavod, url: str):
    url_path = urlparse(url).path.lstrip("/")
    path = context.fetch_resource(url_path, url)
    context.log.info("Crawling: %s" % url_path)
    with ZipFile(path, "r") as zip:
        for name in zip.namelist():
            if not name.lower().endswith(".xml"):
                continue
            with zip.open(name, "r") as fh:
                parse_xml(context, fh)


def crawl(context: Zavod):
    # TODO: thread pool execution
    for archive_url in sorted(crawl_index(context, PREFIX)):
        crawl_archive(context, archive_url)


if __name__ == "__main__":
    with init_context("ru_egrul", "ru") as context:
        crawl(context)
        # parse(context)
