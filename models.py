# -*- coding: utf-8 -*-
from app import db


class AmoCrmContact(db.Model):
    __tablename__ = 'amocrm_contacts'
    __humanname__ = 'Параметры контактов'
    __order__ = 3

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': gettext('Идентификатор контакта'), 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': gettext('Идентификатор подключенного аккаунта'), 'category': 'table_id'})
    contact_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Внутренний идентификатор контакта'})
    name = db.Column(db.Unicode(64), info={'verbose_name': 'Имя контакта', 'category': 'name'})
    company = db.Column(db.Unicode(128), info={'verbose_name': 'Компания'})
    post = db.Column(db.Unicode(256), info={'verbose_name': 'Должность'})
    phone = db.Column(db.Unicode(256), info={'verbose_name': 'Телефон', 'category': 'phone'})
    email = db.Column(db.Unicode(256), info={'verbose_name': 'e-mail', 'category': 'email'})
    request_id = db.Column(db.Unicode(64), info={'verbose_name': 'Идентификатор заявки'})
    is_deleted = db.Column(db.Boolean, nullable=False, info={'verbose_name': 'Контакт удален', 'category': 'excluded'})

    __table_args__ = (
        db.UniqueConstraint(account_id, contact_id, name='amocrm_contacts_idx_1'),
    )

    def __repr__(self):
        return '<AmoCrmContact %r>' % self.id


class AmoCrmCompany(db.Model):
    __tablename__ = 'amocrm_companies'
    __humanname__ = 'Параметры компаний'
    __order__ = 3

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор компании', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    company_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Внутренний идентификатор компании'})
    name = db.Column(db.Unicode(128), info={'verbose_name': 'Название компании'})
    phone = db.Column(db.Unicode(256), info={'verbose_name': 'Контактный телефон', 'category': 'phone'})
    email = db.Column(db.Unicode(256), info={'verbose_name': 'Контактный email', 'category': 'email'})
    site = db.Column(db.Unicode(256), info={'verbose_name': 'Сайт компании'})
    is_deleted = db.Column(db.Boolean, nullable=False, info={'verbose_name': 'Компания удалена', 'category': 'excluded'})

    __table_args__ = (
        db.UniqueConstraint(account_id, company_id, name='amocrm_companies_idx_1'),
    )

    def __repr__(self):
        return '<AmoCrmCompany %r>' % self.id


class AmoCrmLeadFact(db.Model):
    __tablename__ = 'amocrm_leads_facts'
    __humanname__ = 'Сделки'
    __order__ = 1

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    clientids_id = db.Column(db.Integer, db.ForeignKey('general_clientids.id', name='amocrm_leads_facts_general_clientids'), nullable=False, info={'verbose_name': 'Идентификатор клиента', 'category': 'table_id'})
    traffic_id = db.Column(db.Integer, db.ForeignKey('general_traffic.id', name='amocrm_leads_facts_general_traffic'), nullable=False, info={'verbose_name': 'Идентификатор источника трафика'})
    users_id = db.Column(db.Integer, db.ForeignKey('amocrm_users.id', name='amocrm_leads_facts_amocrm_users'), nullable=False, info={'verbose_name': 'Идентификатор пользователя', 'category': 'table_id'})
    leads_id = db.Column(db.Integer, db.ForeignKey('amocrm_leads.id', name='amocrm_leads_facts_amocrm_leads'), nullable=False, info={'verbose_name': 'Идентификатор сделки', 'category': 'table_id'})
    contacts_id = db.Column(db.Integer, db.ForeignKey('amocrm_contacts.id', name='amocrm_leads_facts_amocrm_contacts'), nullable=False, info={'verbose_name': 'Идентификатор контакта', 'category': 'table_id'})
    companies_id = db.Column(db.Integer, db.ForeignKey('amocrm_companies.id', name='amocrm_leads_facts_amocrm_companies'), nullable=False, info={'verbose_name': 'Идентификатор компании', 'category': 'table_id'})
    unsorteds_id = db.Column(db.Integer, db.ForeignKey('amocrm_unsorted.id', name='amocrm_leads_facts_amocrm_unsorted'), nullable=False, info={'verbose_name': 'Идентификатор неразобранного', 'category': 'table_id'})
    created_id = db.Column(db.Integer, db.ForeignKey('general_dates.id', name='amocrm_leads_facts_general_dates_created'), nullable=False, info={'verbose_name': 'Идентификатор даты открытия сделки', 'category': 'table_id'})
    closed_id = db.Column(db.Integer, db.ForeignKey('general_dates.id', name='amocrm_leads_facts_general_dates_paid'), nullable=False, info={'verbose_name': 'Идентификатор даты закрытия сделки', 'category': 'table_id'})
    price = db.Column(db.Numeric(18,2), nullable=False, info={'verbose_name': 'Сумма'})

    amocrm_contacts = db.relationship('AmoCrmContact', foreign_keys=contacts_id)
    amocrm_companies = db.relationship('AmoCrmCompany', foreign_keys=companies_id)
    amocrm_leads = db.relationship('AmoCrmLead', foreign_keys=leads_id)
    amocrm_users = db.relationship('AmoCrmUser', foreign_keys=users_id)
    general_dates = db.relationship('GeneralDate', foreign_keys=created_id)
    general_dates = db.relationship('GeneralDate', foreign_keys=closed_id)
    general_clientids = db.relationship('GeneralClientId', foreign_keys=clientids_id)
    amocrm_unsorted = db.relationship('AmoCrmUnsorted', foreign_keys=unsorteds_id)
    general_traffic = db.relationship('GeneralTraffic', foreign_keys=traffic_id)

    __table_args__ = (
        db.UniqueConstraint(account_id, leads_id, name='amocrm_leads_facts_idx_1'),
        db.Index('amocrm_leads_facts_idx_2', clientids_id),
        db.Index('amocrm_leads_facts_idx_3', created_id),
        db.Index('amocrm_leads_facts_idx_4', closed_id),
    )

    def __repr__(self):
        return '<AmoCrmLeadFact %r>' % self.id


class AmoCrmLead(db.Model):
    __tablename__ = 'amocrm_leads'
    __humanname__ = 'Параметры сделок'
    __order__ = 3

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор сделки', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    lead_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Внутренний идентификатор сделки'})
    name = db.Column(db.Unicode(128), info={'verbose_name': 'Название сделки'})
    pipeline = db.Column(db.Unicode(64), info={'verbose_name': 'Название воронки'})
    pipeline_id = db.Column(db.Integer, info={'verbose_name': 'Идентификатор воронки'})
    status = db.Column(db.Unicode(128), info={'verbose_name': 'Статус сделки'})
    status_id = db.Column(db.Integer, info={'verbose_name': 'Идентификатор этапа'})
    status_order = db.Column(db.Integer, info={'verbose_name': 'Очередность статуса сделки'})
    request_id = db.Column(db.Unicode(64), info={'verbose_name': 'Идентификатор заявки'})
    loss_reason = db.Column(db.Unicode(128), info={'verbose_name': 'Причина отказа'})
    loss_reason_id = db.Column(db.Integer, info={'verbose_name': 'Идентификатор причины отказа'})
    is_deleted = db.Column(db.Boolean, nullable=False, info={'verbose_name': 'Сделка удалена', 'category': 'excluded'})

    __table_args__ = (
        db.UniqueConstraint(account_id, lead_id, name='amocrm_leads_idx_1'),
    )

    def __repr__(self):
        return '<AmoCrmLead %r>' % self.id


class AmoCrmUser(db.Model):
    __tablename__ = 'amocrm_users'
    __humanname__ = 'Параметры пользователей'
    __order__ = 3

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор пользователя', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    user_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Внутренний идентификатор пользователя'})
    login = db.Column(db.Unicode(64), info={'verbose_name': 'Логин'})
    name = db.Column(db.Unicode(64), info={'verbose_name': 'Имя', 'category': 'name'})
    phone = db.Column(db.Unicode(64), info={'verbose_name': 'Телефон', 'category': 'phone'})
    group_name = db.Column(db.Unicode(64), info={'verbose_name': 'Группа пользователя'})
    email = db.Column(db.Unicode(64), info={'verbose_name': 'Электронный адрес', 'category': 'email'})
    is_admin = db.Column(db.Boolean, info={'verbose_name': 'Администратор'})
    is_active = db.Column(db.Boolean, info={'verbose_name': 'Активный пользователь'})
    is_free = db.Column(db.Boolean, info={'verbose_name': 'Бесплатный пользователь'})
    mail_access = db.Column(db.Boolean, info={'verbose_name': 'Доступ к функционалу почты'})
    catalog_access = db.Column(db.Boolean, info={'verbose_name': 'Доступ к функционалу списков'})
    role_id = db.Column(db.Integer, info={'verbose_name': 'Идентификатор роли'})
    role_name = db.Column(db.Unicode(64), info={'verbose_name': 'Роль пользователя'})
    group_id = db.Column(db.Integer, info={'verbose_name': 'Идентификатор группы'})

    __table_args__ = (
        db.UniqueConstraint(account_id, user_id, name='amocrm_users_idx_1'),
    )

    def __repr__(self):
        return '<AmoCrmUser %r>' % self.id


class AmoCrmCompanyFact(db.Model):
    __tablename__ = 'amocrm_companies_facts'
    __humanname__ = 'Компании'
    __order__ = 1

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    users_id = db.Column(db.Integer, db.ForeignKey('amocrm_users.id', name='amocrm_companies_facts_amocrm_users'), nullable=False, info={'verbose_name': 'Идентификатор пользователя', 'category': 'table_id'})
    companies_id = db.Column(db.Integer, db.ForeignKey('amocrm_companies.id', name='amocrm_companies_facts_amocrm_companies'), nullable=False, info={'verbose_name': 'Идентификатор компании', 'category': 'table_id'})
    registered_id = db.Column(db.Integer, db.ForeignKey('general_dates.id', name='amocrm_companies_facts_general_dates_registered'), nullable=False, info={'verbose_name': 'Идентификатор даты', 'category': 'table_id'})

    amocrm_users = db.relationship('AmoCrmUser', foreign_keys=users_id)
    amocrm_companies = db.relationship('AmoCrmCompany', foreign_keys=companies_id)
    general_dates = db.relationship('GeneralDate', foreign_keys=registered_id)

    __table_args__ = (
        db.UniqueConstraint(account_id, companies_id, name='amocrm_companies_facts_idx_1'),
        db.Index('amocrm_companies_facts_idx_2', registered_id),
    )

    def __repr__(self):
        return '<AmoCrmCompanyFact %r>' % self.id


class AmoCrmCallFact(db.Model):
    __tablename__ = 'amocrm_calls_facts'
    __humanname__ = 'Звонки'
    __order__ = 1

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    dates_id = db.Column(db.Integer, db.ForeignKey('general_dates.id', name='amocrm_calls_facts_general_dates'), nullable=False, info={'verbose_name': 'Идентификатор даты', 'category': 'table_id'})
    users_id = db.Column(db.Integer, db.ForeignKey('amocrm_users.id', name='amocrm_calls_facts_amocrm_users'), nullable=False, info={'verbose_name': 'Идентификатор пользователя', 'category': 'table_id'})
    calls_id = db.Column(db.Integer, db.ForeignKey('amocrm_calls.id', name='amocrm_calls_facts_amocrm_calls'), nullable=False, info={'verbose_name': 'Идентификатор звонка', 'category': 'table_id'})
    contacts_id = db.Column(db.Integer, db.ForeignKey('amocrm_contacts.id', name='amocrm_calls_facts_amocrm_contacts'), nullable=False, info={'verbose_name': 'Идентификатор контакта', 'category': 'table_id'})
    companies_id = db.Column(db.Integer, db.ForeignKey('amocrm_companies.id', name='amocrm_calls_facts_amocrm_companies'), nullable=False, info={'verbose_name': 'Идентификатор компании', 'category': 'table_id'})
    leads_id = db.Column(db.Integer, db.ForeignKey('amocrm_leads.id', name='amocrm_calls_facts_amocrm_leads'), nullable=False, info={'verbose_name': 'Идентификатор сделки', 'category': 'table_id'})
    customers_id = db.Column(db.Integer, db.ForeignKey('amocrm_customers.id', name='amocrm_calls_facts_amocrm_customers'), nullable=False, info={'verbose_name': 'Идентификатор покупателя', 'category': 'table_id'})
    duration = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Продолжительность звонка'})

    amocrm_calls = db.relationship('AmoCrmCall', foreign_keys=calls_id)
    amocrm_users = db.relationship('AmoCrmUser', foreign_keys=users_id)
    amocrm_contacts = db.relationship('AmoCrmContact', foreign_keys=contacts_id)
    general_dates = db.relationship('GeneralDate', foreign_keys=dates_id)
    amocrm_companies = db.relationship('AmoCrmCompany', foreign_keys=companies_id)
    amocrm_leads = db.relationship('AmoCrmLead', foreign_keys=leads_id)
    amocrm_customers = db.relationship('AmoCrmCustomer', foreign_keys=customers_id)

    __table_args__ = (
        db.UniqueConstraint(account_id, calls_id, name='amocrm_calls_facts_idx_1'),
        db.Index('amocrm_calls_facts_idx_2', dates_id),
    )

    def __repr__(self):
        return '<AmoCrmCallFact %r>' % self.id


class AmoCrmCall(db.Model):
    __tablename__ = 'amocrm_calls'
    __humanname__ = 'Параметры звонков'
    __order__ = 3

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор звонка', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    note_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Внутренний идентификатор примечания'})
    call_id = db.Column(db.Unicode(64), info={'verbose_name': 'Внутренний идентификатор звонка'})
    call_type = db.Column(db.Unicode(16), info={'verbose_name': 'Тип звонка'})
    call_status = db.Column(db.Unicode(32), info={'verbose_name': 'Статус звонка'})
    call_result = db.Column(db.Unicode(128), info={'verbose_name': 'Результат звонка'})
    phone = db.Column(db.Unicode(64), info={'verbose_name': 'Номер телефона', 'category': 'phone'})
    link = db.Column(db.Unicode(512), info={'verbose_name': 'Ссылка на запись звонка'})

    __table_args__ = (
        db.UniqueConstraint(account_id, note_id, name='amocrm_calls_idx_1'),
    )

    def __repr__(self):
        return '<AmoCrmCall %r>' % self.id


class AmoCrmLeadAttribute(db.Model):
    __tablename__ = 'amocrm_leads_attributes'
    __humanname__ = 'Дополнительные параметры сделок'
    __order__ = 2

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    leads_id = db.Column(db.Integer, db.ForeignKey('amocrm_leads.id', name='amocrm_leads_attributes_amocrm_leads'), nullable=False, info={'verbose_name': 'Идентификатор сделки', 'category': 'table_id'})
    attribute_id = db.Column(db.Unicode(64), nullable=False, info={'verbose_name': 'Внутренний идентификатор параметра'})
    name = db.Column(db.Unicode(256), nullable=False, info={'verbose_name': 'Название'})
    value = db.Column(db.UnicodeText, info={'verbose_name': 'Значение'})

    amocrm_leads = db.relationship('AmoCrmLead', foreign_keys=leads_id)

    __table_args__ = (
        db.UniqueConstraint(account_id, leads_id, attribute_id, name='amocrm_leads_attributes_idx_1'),
    )

    def __repr__(self):
        return '<AmoCrmLeadAttribute %r>' % self.id


class AmoCrmContactAttribute(db.Model):
    __tablename__ = 'amocrm_contacts_attributes'
    __humanname__ = 'Дополнительные параметры контактов'
    __order__ = 2

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    contacts_id = db.Column(db.Integer, db.ForeignKey('amocrm_contacts.id', name='amocrm_contacts_attributes_amocrm_contacts'), nullable=False, info={'verbose_name': 'Идентификатор контакта', 'category': 'table_id'})
    attribute_id = db.Column(db.Unicode(64), nullable=False, info={'verbose_name': 'Внутренний идентификатор параметра'})
    name = db.Column(db.Unicode(256), nullable=False, info={'verbose_name': 'Название'})
    value = db.Column(db.UnicodeText, info={'verbose_name': 'Значение'})

    amocrm_contacts = db.relationship('AmoCrmContact', foreign_keys=contacts_id)

    __table_args__ = (
        db.UniqueConstraint(account_id, contacts_id, attribute_id, name='amocrm_contacts_attributes_idx_1'),
    )

    def __repr__(self):
        return '<AmoCrmContactAttribute %r>' % self.id


class AmoCrmCompanyAttribute(db.Model):
    __tablename__ = 'amocrm_companies_attributes'
    __humanname__ = 'Дополнительные параметры компаний'
    __order__ = 2

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    companies_id = db.Column(db.Integer, db.ForeignKey('amocrm_companies.id', name='amocrm_companies_attributes_amocrm_companies'), nullable=False, info={'verbose_name': 'Идентификатор компании', 'category': 'table_id'})
    attribute_id = db.Column(db.Unicode(64), nullable=False, info={'verbose_name': 'Внутренний идентификатор параметра'})
    name = db.Column(db.Unicode(256), nullable=False, info={'verbose_name': 'Название'})
    value = db.Column(db.UnicodeText, info={'verbose_name': 'Значение'})

    amocrm_companies = db.relationship('AmoCrmCompany', foreign_keys=companies_id)

    __table_args__ = (
        db.UniqueConstraint(account_id, companies_id, attribute_id, name='amocrm_companies_attributes_idx_1'),
    )

    def __repr__(self):
        return '<AmoCrmCompanyAttribute %r>' % self.id


class AmoCrmContactFact(db.Model):
    __tablename__ = 'amocrm_contacts_facts'
    __humanname__ = 'Контакты'
    __order__ = 1

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    contacts_id = db.Column(db.Integer, db.ForeignKey('amocrm_contacts.id', name='amocrm_contacts_facts_amocrm_contacts'), nullable=False, info={'verbose_name': 'Идентификатор контакта', 'category': 'table_id'})
    companies_id = db.Column(db.Integer, db.ForeignKey('amocrm_companies.id', name='amocrm_contacts_facts_amocrm_companies'), nullable=False, info={'verbose_name': 'Идентификатор компании', 'category': 'table_id'})
    users_id = db.Column(db.Integer, db.ForeignKey('amocrm_users.id', name='amocrm_contacts_facts_amocrm_users'), nullable=False, info={'verbose_name': 'Идентификатор пользователя', 'category': 'table_id'})
    registered_id = db.Column(db.Integer, db.ForeignKey('general_dates.id', name='amocrm_contacts_facts_general_dates'), nullable=False, info={'verbose_name': 'Идентификатор даты', 'category': 'table_id'})

    amocrm_contacts = db.relationship('AmoCrmContact', foreign_keys=contacts_id)
    general_dates = db.relationship('GeneralDate', foreign_keys=registered_id)
    amocrm_companies = db.relationship('AmoCrmCompany', foreign_keys=companies_id)
    amocrm_users = db.relationship('AmoCrmUser', foreign_keys=users_id)

    __table_args__ = (
        db.UniqueConstraint(account_id, contacts_id, name='amocrm_contacts_facts_idx_1'),
        db.Index('amocrm_contacts_facts_idx_2', registered_id),
    )

    def __repr__(self):
        return '<AmoCrmContactFact %r>' % self.id


class AmoCrmLeadTag(db.Model):
    __tablename__ = 'amocrm_leads_tags'
    __humanname__ = 'Метки сделок'
    __order__ = 2

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    leads_id = db.Column(db.Integer, db.ForeignKey('amocrm_leads.id', name='amocrm_leads_tags_amocrm_leads'), nullable=False, info={'verbose_name': 'Идентификатор сделки', 'category': 'table_id'})
    tag_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Внутренний идентификатор метки'})
    name = db.Column(db.Unicode(128), nullable=False, info={'verbose_name': 'Название'})

    amocrm_leads = db.relationship('AmoCrmLead', foreign_keys=leads_id)

    __table_args__ = (
        db.UniqueConstraint(account_id, leads_id, tag_id, name='amocrm_leads_tags_idx_1'),
    )

    def __repr__(self):
        return '<AmoCrmLeadTag %r>' % self.id


class AmoCrmContactTag(db.Model):
    __tablename__ = 'amocrm_contacts_tags'
    __humanname__ = 'Метки контактов'
    __order__ = 2

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    contacts_id = db.Column(db.Integer, db.ForeignKey('amocrm_contacts.id', name='Copy_of_amocrm_leads_tags_amocrm_contacts'), nullable=False, info={'verbose_name': 'Идентификатор контакта', 'category': 'table_id'})
    tag_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Внутренний идентификатор метки'})
    name = db.Column(db.Unicode(128), nullable=False, info={'verbose_name': 'Название'})

    amocrm_contacts = db.relationship('AmoCrmContact', foreign_keys=contacts_id)

    __table_args__ = (
        db.UniqueConstraint(account_id, contacts_id, tag_id, name='amocrm_contacts_tags_idx_1'),
    )

    def __repr__(self):
        return '<AmoCrmContactTag %r>' % self.id


class AmoCrmTask(db.Model):
    __tablename__ = 'amocrm_tasks'
    __humanname__ = 'Параметры задач'
    __order__ = 3

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор задачи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    task_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Внутренний идентификатор задачи'})
    task_type = db.Column(db.Unicode(32), info={'verbose_name': 'Тип задачи'})
    text = db.Column(db.Unicode(256), info={'verbose_name': 'Текст'})
    result = db.Column(db.Unicode(512), info={'verbose_name': 'Результат выполнения'})
    status_code = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Статус'})
    is_deleted = db.Column(db.Boolean, nullable=False, info={'verbose_name': 'Задача удалена', 'category': 'excluded'})

    __table_args__ = (
        db.UniqueConstraint(account_id, task_id, name='amocrm_tasks_idx_1'),
    )

    def __repr__(self):
        return '<AmoCrmTask %r>' % self.id


class AmoCrmTaskFact(db.Model):
    __tablename__ = 'amocrm_tasks_facts'
    __humanname__ = 'Задачи'
    __order__ = 1

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    users_id = db.Column(db.Integer, db.ForeignKey('amocrm_users.id', name='amocrm_tasks_facts_amocrm_users'), nullable=False, info={'verbose_name': 'Идентификатор пользователя', 'category': 'table_id'})
    contacts_id = db.Column(db.Integer, db.ForeignKey('amocrm_contacts.id', name='amocrm_tasks_facts_amocrm_contacts'), nullable=False, info={'verbose_name': 'Идентификатор контакта', 'category': 'table_id'})
    companies_id = db.Column(db.Integer, db.ForeignKey('amocrm_companies.id', name='amocrm_tasks_facts_amocrm_companies'), nullable=False, info={'verbose_name': 'Идентификатор компании', 'category': 'table_id'})
    leads_id = db.Column(db.Integer, db.ForeignKey('amocrm_leads.id', name='amocrm_tasks_facts_amocrm_leads'), nullable=False, info={'verbose_name': 'Идентификатор сделки', 'category': 'table_id'})
    customers_id = db.Column(db.Integer, db.ForeignKey('amocrm_customers.id', name='amocrm_tasks_facts_amocrm_customers'), nullable=False, info={'verbose_name': 'Идентификатор покупателя', 'category': 'table_id'})
    tasks_id = db.Column(db.Integer, db.ForeignKey('amocrm_tasks.id', name='amocrm_tasks_facts_amocrm_tasks'), nullable=False, info={'verbose_name': 'Идентификатор задачи', 'category': 'table_id'})
    created_id = db.Column(db.Integer, db.ForeignKey('general_dates.id', name='amocrm_tasks_facts_general_dates_created'), nullable=False, info={'verbose_name': 'Идентификатор даты создания задачи', 'category': 'table_id'})
    modified_id = db.Column(db.Integer, db.ForeignKey('general_dates.id', name='amocrm_tasks_facts_general_dates'), nullable=False, info={'verbose_name': 'Идентификатор даты изменения задачи', 'category': 'table_id'})
    completed_id = db.Column(db.Integer, db.ForeignKey('general_dates.id', name='amocrm_tasks_facts_general_dates_completed'), nullable=False, info={'verbose_name': 'Идентификатор даты завершения задачи', 'category': 'table_id'})
    duration = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Длительность задачи'})

    amocrm_users = db.relationship('AmoCrmUser', foreign_keys=users_id)
    amocrm_leads = db.relationship('AmoCrmLead', foreign_keys=leads_id)
    amocrm_contacts = db.relationship('AmoCrmContact', foreign_keys=contacts_id)
    amocrm_tasks = db.relationship('AmoCrmTask', foreign_keys=tasks_id)
    general_dates = db.relationship('GeneralDate', foreign_keys=created_id)
    general_dates = db.relationship('GeneralDate', foreign_keys=completed_id)
    general_dates = db.relationship('GeneralDate', foreign_keys=modified_id)
    amocrm_companies = db.relationship('AmoCrmCompany', foreign_keys=companies_id)
    amocrm_customers = db.relationship('AmoCrmCustomer', foreign_keys=customers_id)

    __table_args__ = (
        db.UniqueConstraint(account_id, tasks_id, name='amocrm_tasks_facts_idx_1'),
        db.Index('amocrm_tasks_facts_idx_2', created_id),
    )

    def __repr__(self):
        return '<AmoCrmTaskFact %r>' % self.id


class AmoCrmCompanyTag(db.Model):
    __tablename__ = 'amocrm_companies_tags'
    __humanname__ = 'Метки компаний'
    __order__ = 2

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    companies_id = db.Column(db.Integer, db.ForeignKey('amocrm_companies.id', name='amocrm_companies_tags_amocrm_companies'), nullable=False, info={'verbose_name': 'Идентификатор компании', 'category': 'table_id'})
    tag_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Внутренний идентификатор метки'})
    name = db.Column(db.Unicode(128), nullable=False, info={'verbose_name': 'Название'})

    amocrm_companies = db.relationship('AmoCrmCompany', foreign_keys=companies_id)

    __table_args__ = (
        db.UniqueConstraint(account_id, companies_id, tag_id, name='amocrm_companies_tags_idx_1'),
    )

    def __repr__(self):
        return '<AmoCrmCompanyTag %r>' % self.id


class AmoCrmCustomer(db.Model):
    __tablename__ = 'amocrm_customers'
    __humanname__ = 'Параметры покупателей'
    __order__ = 3

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор покупателя', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    customer_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Внутренний идентификатор покупателя'})
    name = db.Column(db.Unicode(128), info={'verbose_name': 'Название покупателя', 'category': 'name'})
    period = db.Column(db.Unicode(64), info={'verbose_name': 'Период'})
    period_order = db.Column(db.Integer, info={'verbose_name': 'Порядок периода'})

    __table_args__ = (
        db.UniqueConstraint(account_id, customer_id, name='amocrm_customers_idx_1'),
    )

    def __repr__(self):
        return '<AmoCrmCustomer %r>' % self.id


class AmoCrmCustomerAttribute(db.Model):
    __tablename__ = 'amocrm_customers_attributes'
    __humanname__ = 'Дополнительные параметры покупателей'
    __order__ = 2

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    customers_id = db.Column(db.Integer, db.ForeignKey('amocrm_customers.id', name='amocrm_customers_attributes_amocrm_customers'), nullable=False, info={'verbose_name': 'Идентификатор покупателя', 'category': 'table_id'})
    attribute_id = db.Column(db.Unicode(64), nullable=False, info={'verbose_name': 'Внутренний идентификатор параметра'})
    name = db.Column(db.Unicode(256), nullable=False, info={'verbose_name': 'Название'})
    value = db.Column(db.UnicodeText, info={'verbose_name': 'Значение'})

    amocrm_customers = db.relationship('AmoCrmCustomer', foreign_keys=customers_id)

    __table_args__ = (
        db.UniqueConstraint(account_id, customers_id, attribute_id, name='amocrm_customers_attributes_idx_1'),
    )

    def __repr__(self):
        return '<AmoCrmCustomerAttribute %r>' % self.id


class AmoCrmCustomerTag(db.Model):
    __tablename__ = 'amocrm_customers_tags'
    __humanname__ = 'Метки покупателей'
    __order__ = 2

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    customers_id = db.Column(db.Integer, db.ForeignKey('amocrm_customers.id', name='amocrm_customers_tags_amocrm_customers'), nullable=False, info={'verbose_name': 'Идентификатор покупателя', 'category': 'table_id'})
    tag_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Внутренний идентификатор метки'})
    name = db.Column(db.Unicode(128), nullable=False, info={'verbose_name': 'Название'})

    amocrm_customers = db.relationship('AmoCrmCustomer', foreign_keys=customers_id)

    __table_args__ = (
        db.UniqueConstraint(account_id, customers_id, tag_id, name='amocrm_customers_tags_idx_1'),
    )

    def __repr__(self):
        return '<AmoCrmCustomerTag %r>' % self.id


class AmoCrmCustomerFact(db.Model):
    __tablename__ = 'amocrm_customers_facts'
    __humanname__ = 'Покупатели'
    __order__ = 1

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    customers_id = db.Column(db.Integer, db.ForeignKey('amocrm_customers.id', name='amocrm_customers_facts_amocrm_customers'), nullable=False, info={'verbose_name': 'Идентификатор покупателя', 'category': 'table_id'})
    created_id = db.Column(db.Integer, db.ForeignKey('general_dates.id', name='amocrm_customers_facts_general_dates_created'), nullable=False, info={'verbose_name': 'Идентификатор даты создания', 'category': 'table_id'})
    expected_id = db.Column(db.Integer, db.ForeignKey('general_dates.id', name='amocrm_customers_facts_general_dates_expected'), nullable=False, info={'verbose_name': 'Идентификатор даты следующей покупки', 'category': 'table_id'})
    companies_id = db.Column(db.Integer, db.ForeignKey('amocrm_companies.id', name='amocrm_customers_facts_amocrm_companies'), nullable=False, info={'verbose_name': 'Идентификатор компании', 'category': 'table_id'})
    contacts_id = db.Column(db.Integer, db.ForeignKey('amocrm_contacts.id', name='amocrm_customers_facts_amocrm_contacts'), nullable=False, info={'verbose_name': 'Идентификатор контакта', 'category': 'table_id'})
    users_id = db.Column(db.Integer, db.ForeignKey('amocrm_users.id', name='amocrm_customers_facts_amocrm_users'), nullable=False, info={'verbose_name': 'Идентификатор пользователя', 'category': 'table_id'})
    periodicity = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Периодичность'})
    purchases = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Покупки'})
    average_check = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Средняя сумма'})
    next_price = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Ожидаемая сумма'})
    ltv = db.Column(db.Integer, nullable=False, info={'verbose_name': 'LTV'})

    general_dates = db.relationship('GeneralDate', foreign_keys=created_id)
    amocrm_customers = db.relationship('AmoCrmCustomer', foreign_keys=customers_id)
    amocrm_companies = db.relationship('AmoCrmCompany', foreign_keys=companies_id)
    amocrm_contacts = db.relationship('AmoCrmContact', foreign_keys=contacts_id)
    amocrm_users = db.relationship('AmoCrmUser', foreign_keys=users_id)
    general_dates = db.relationship('GeneralDate', foreign_keys=expected_id)

    __table_args__ = (
        db.UniqueConstraint(account_id, customers_id, name='amocrm_customers_facts_idx_1'),
        db.Index('amocrm_customers_facts_idx_2', created_id),
    )

    def __repr__(self):
        return '<AmoCrmCustomerFact %r>' % self.id


class AmoCrmLeadNote(db.Model):
    __tablename__ = 'amocrm_leads_notes'
    __humanname__ = 'Примечания сделок'
    __order__ = 2

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    leads_id = db.Column(db.Integer, db.ForeignKey('amocrm_leads.id', name='amocrm_leads_notes_amocrm_leads'), nullable=False, info={'verbose_name': 'Идентификатор сделки', 'category': 'table_id'})
    creator_id = db.Column(db.Integer, info={'verbose_name': 'Внутренний идентификатор создавшего'})
    responsible_id = db.Column(db.Integer, info={'verbose_name': 'Внутренний идентификатор ответственного'})
    note_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Внутренний идентификатор примечания'})
    note_type = db.Column(db.Unicode(64), info={'verbose_name': 'Тип примечания'})
    note_type_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор типа примечания'})
    created_at = db.Column(db.DateTime, nullable=False, info={'verbose_name': 'Дата создания'})
    updated_at = db.Column(db.DateTime, nullable=False, info={'verbose_name': 'Дата изменения'})
    text = db.Column(db.UnicodeText, info={'verbose_name': 'Текст примечания'})
    params = db.Column(db.UnicodeText, info={'verbose_name': 'Дополнительные параметры'})

    amocrm_leads = db.relationship('AmoCrmLead', foreign_keys=leads_id)

    __table_args__ = (
        db.UniqueConstraint(account_id, note_id, name='amocrm_leads_notes_idx_1'),
        db.Index('amocrm_leads_notes_idx_2', leads_id),
        db.Index('amocrm_leads_notes_idx_3', created_at),
    )

    def __repr__(self):
        return '<AmoCrmLeadNote %r>' % self.id


class AmoCrmTaskNote(db.Model):
    __tablename__ = 'amocrm_tasks_notes'
    __humanname__ = 'Примечания задач'
    __order__ = 2

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    tasks_id = db.Column(db.Integer, db.ForeignKey('amocrm_tasks.id', name='amocrm_tasks_notes_amocrm_tasks'), nullable=False, info={'verbose_name': 'Идентификатор задачи', 'category': 'table_id'})
    creator_id = db.Column(db.Integer, info={'verbose_name': 'Внутренний идентификатор создавшего'})
    responsible_id = db.Column(db.Integer, info={'verbose_name': 'Внутренний идентификатор ответственного'})
    note_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Внутренний идентификатор примечания'})
    note_type = db.Column(db.Unicode(64), info={'verbose_name': 'Тип примечания'})
    note_type_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор типа примечания'})
    created_at = db.Column(db.DateTime, nullable=False, info={'verbose_name': 'Дата создания'})
    updated_at = db.Column(db.DateTime, nullable=False, info={'verbose_name': 'Дата изменения'})
    text = db.Column(db.UnicodeText, info={'verbose_name': 'Текст примечания'})
    params = db.Column(db.UnicodeText, info={'verbose_name': 'Дополнительные параметры'})

    amocrm_tasks = db.relationship('AmoCrmTask', foreign_keys=tasks_id)

    __table_args__ = (
        db.UniqueConstraint(account_id, note_id, name='amocrm_tasks_notes_idx_1'),
        db.Index('amocrm_tasks_notes_idx_2', tasks_id),
        db.Index('amocrm_tasks_notes_idx_3', created_at),
    )

    def __repr__(self):
        return '<AmoCrmTaskNote %r>' % self.id


class AmoCrmContactNote(db.Model):
    __tablename__ = 'amocrm_contacts_notes'
    __humanname__ = 'Примечания контактов'
    __order__ = 2

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    contacts_id = db.Column(db.Integer, db.ForeignKey('amocrm_contacts.id', name='amocrm_contacts_notes_amocrm_contacts'), nullable=False, info={'verbose_name': 'Идентификатор контакта', 'category': 'table_id'})
    creator_id = db.Column(db.Integer, info={'verbose_name': 'Внутренний идентификатор создавшего'})
    responsible_id = db.Column(db.Integer, info={'verbose_name': 'Внутренний идентификатор ответственного'})
    note_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Внутренний идентификатор примечания'})
    note_type = db.Column(db.Unicode(64), info={'verbose_name': 'Тип примечания'})
    note_type_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор типа примечания'})
    created_at = db.Column(db.DateTime, nullable=False, info={'verbose_name': 'Дата создания'})
    updated_at = db.Column(db.DateTime, nullable=False, info={'verbose_name': 'Дата изменения'})
    text = db.Column(db.UnicodeText, info={'verbose_name': 'Текст примечания'})
    params = db.Column(db.UnicodeText, info={'verbose_name': 'Дополнительные параметры'})

    amocrm_contacts = db.relationship('AmoCrmContact', foreign_keys=contacts_id)

    __table_args__ = (
        db.UniqueConstraint(account_id, note_id, name='amocrm_contacts_notes_idx_1'),
        db.Index('amocrm_contacts_notes_idx_2', contacts_id),
        db.Index('amocrm_contacts_notes_idx_3', created_at),
    )

    def __repr__(self):
        return '<AmoCrmContactNote %r>' % self.id


class AmoCrmCompanyNote(db.Model):
    __tablename__ = 'amocrm_companies_notes'
    __humanname__ = 'Примечания компаний'
    __order__ = 2

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    companies_id = db.Column(db.Integer, db.ForeignKey('amocrm_companies.id', name='amocrm_companies_notes_amocrm_companies'), nullable=False, info={'verbose_name': 'Идентификатор компании', 'category': 'table_id'})
    creator_id = db.Column(db.Integer, info={'verbose_name': 'Внутренний идентификатор создавшего'})
    responsible_id = db.Column(db.Integer, info={'verbose_name': 'Внутренний идентификатор ответственного'})
    note_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Внутренний идентификатор примечания'})
    note_type = db.Column(db.Unicode(64), info={'verbose_name': 'Тип примечания'})
    note_type_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор типа примечания'})
    created_at = db.Column(db.DateTime, nullable=False, info={'verbose_name': 'Дата создания'})
    updated_at = db.Column(db.DateTime, nullable=False, info={'verbose_name': 'Дата изменения'})
    text = db.Column(db.UnicodeText, info={'verbose_name': 'Текст примечания'})
    params = db.Column(db.UnicodeText, info={'verbose_name': 'Дополнительные параметры'})

    amocrm_companies = db.relationship('AmoCrmCompany', foreign_keys=companies_id)

    __table_args__ = (
        db.UniqueConstraint(account_id, note_id, name='amocrm_companies_notes_idx_1'),
        db.Index('amocrm_companies_notes_idx_2', companies_id),
        db.Index('amocrm_companies_notes_idx_3', created_at),
    )

    def __repr__(self):
        return '<AmoCrmCompanyNote %r>' % self.id


class AmoCrmElement(db.Model):
    __tablename__ = 'amocrm_elements'
    __humanname__ = 'Параметры элементов'
    __order__ = 3

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор элемента', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    element_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Внутренний идентификатор элемента'})
    name = db.Column(db.Unicode(256), info={'verbose_name': 'Название'})
    catalog = db.Column(db.Unicode(128), info={'verbose_name': 'Список'})
    catalog_order = db.Column(db.Integer, info={'verbose_name': 'Порядок списка'})

    __table_args__ = (
        db.UniqueConstraint(account_id, element_id, name='amocrm_elements_idx_1'),
    )

    def __repr__(self):
        return '<AmoCrmElement %r>' % self.id


class AmoCrmElementAttribute(db.Model):
    __tablename__ = 'amocrm_elements_attributes'
    __humanname__ = 'Дополнительные параметры элементов'
    __order__ = 2

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    elements_id = db.Column(db.Integer, db.ForeignKey('amocrm_elements.id', name='amocrm_elements_attributes_amocrm_elements'), nullable=False, info={'verbose_name': 'Идентификатор элемента', 'category': 'table_id'})
    attribute_id = db.Column(db.Unicode(64), nullable=False, info={'verbose_name': 'Внутренний идентификатор параметра'})
    name = db.Column(db.Unicode(256), nullable=False, info={'verbose_name': 'Название'})
    value = db.Column(db.UnicodeText, nullable=False, info={'verbose_name': 'Значение'})

    amocrm_elements = db.relationship('AmoCrmElement', foreign_keys=elements_id)

    __table_args__ = (
        db.UniqueConstraint(account_id, elements_id, attribute_id, name='amocrm_elements_attributes_idx_1'),
    )

    def __repr__(self):
        return '<AmoCrmElementAttribute %r>' % self.id


class AmoCrmLeadElementFact(db.Model):
    __tablename__ = 'amocrm_leads_elements_facts'
    __humanname__ = 'Элементы сделок'
    __order__ = 1

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    clientids_id = db.Column(db.Integer, db.ForeignKey('general_clientids.id', name='amocrm_leads_elements_facts_general_clientids'), nullable=False, info={'verbose_name': 'Идентификатор клиента', 'category': 'table_id'})
    users_id = db.Column(db.Integer, db.ForeignKey('amocrm_users.id', name='amocrm_leads_elements_facts_amocrm_users'), nullable=False, info={'verbose_name': 'Идентификатор пользователя', 'category': 'table_id'})
    elements_id = db.Column(db.Integer, db.ForeignKey('amocrm_elements.id', name='amocrm_leads_elements_facts_amocrm_elements'), nullable=False, info={'verbose_name': 'Идентификатор элемента', 'category': 'table_id'})
    leads_id = db.Column(db.Integer, db.ForeignKey('amocrm_leads.id', name='amocrm_leads_elements_facts_amocrm_leads'), nullable=False, info={'verbose_name': 'Идентификатор сделки', 'category': 'table_id'})
    contacts_id = db.Column(db.Integer, db.ForeignKey('amocrm_contacts.id', name='amocrm_leads_elements_facts_amocrm_contacts'), nullable=False, info={'verbose_name': 'Идентификатор контакта', 'category': 'table_id'})
    companies_id = db.Column(db.Integer, db.ForeignKey('amocrm_companies.id', name='amocrm_leads_elements_facts_amocrm_companies'), nullable=False, info={'verbose_name': 'Идентификатор компании', 'category': 'table_id'})
    created_id = db.Column(db.Integer, db.ForeignKey('general_dates.id', name='amocrm_leads_elements_facts_general_dates_created'), nullable=False, info={'verbose_name': 'Идентификатор даты открытия сделки', 'category': 'table_id'})
    closed_id = db.Column(db.Integer, db.ForeignKey('general_dates.id', name='amocrm_leads_elements_facts_general_dates_closed'), nullable=False, info={'verbose_name': 'Идентификатор даты закрытия сделки', 'category': 'table_id'})

    amocrm_elements = db.relationship('AmoCrmElement', foreign_keys=elements_id)
    amocrm_leads = db.relationship('AmoCrmLead', foreign_keys=leads_id)
    general_dates = db.relationship('GeneralDate', foreign_keys=created_id)
    general_dates = db.relationship('GeneralDate', foreign_keys=closed_id)
    amocrm_contacts = db.relationship('AmoCrmContact', foreign_keys=contacts_id)
    amocrm_companies = db.relationship('AmoCrmCompany', foreign_keys=companies_id)
    general_clientids = db.relationship('GeneralClientId', foreign_keys=clientids_id)
    amocrm_users = db.relationship('AmoCrmUser', foreign_keys=users_id)

    __table_args__ = (
        db.UniqueConstraint(account_id, elements_id, leads_id, name='amocrm_leads_elements_facts_idx_1'),
        db.Index('amocrm_leads_elements_facts_idx_2', created_id),
    )

    def __repr__(self):
        return '<AmoCrmLeadElementFact %r>' % self.id


class AmoCrmPipeline(db.Model):
    __tablename__ = 'amocrm_pipelines'
    __humanname__ = 'Справочник воронок'
    __order__ = 4

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    pipeline_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор воронки'})
    name = db.Column(db.Unicode(64), nullable=False, info={'verbose_name': 'Название воронки'})
    sort = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Порядковый номер воронки'})
    is_main = db.Column(db.Boolean, nullable=False, info={'verbose_name': 'Главная воронка'})
    is_unsorted_on = db.Column(db.Boolean, nullable=False, info={'verbose_name': 'Неразобранное в воронке включено'})
    is_archive = db.Column(db.Boolean, nullable=False, info={'verbose_name': 'Архивная воронка'})

    __table_args__ = (
        db.UniqueConstraint(account_id, pipeline_id, name='amocrm_pipelines_idx_1'),
    )

    def __repr__(self):
        return '<AmoCrmPipeline %r>' % self.id


class AmoCrmStatus(db.Model):
    __tablename__ = 'amocrm_statuses'
    __humanname__ = 'Справочник этапов продаж'
    __order__ = 4

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    pipeline_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор воронки'})
    status_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор этапа'})
    name = db.Column(db.Unicode(128), nullable=False, info={'verbose_name': 'Название этапа'})
    color = db.Column(db.Unicode(8), nullable=False, info={'verbose_name': 'Цвет этапа'})
    sort = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Порядковый номер этапа'})
    is_editable = db.Column(db.Boolean, nullable=False, info={'verbose_name': 'Редактируемый этап'})
    type = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Тип статуса'})

    __table_args__ = (
        db.UniqueConstraint(account_id, pipeline_id, status_id, name='amocrm_statuses_idx_1'),
    )

    def __repr__(self):
        return '<AmoCrmStatus %r>' % self.id


class AmoCrmTransactionFact(db.Model):
    __tablename__ = 'amocrm_transactions_facts'
    __humanname__ = 'Транзакции'
    __order__ = 1

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    customers_id = db.Column(db.Integer, db.ForeignKey('amocrm_customers.id', name='amocrm_transactions_facts_amocrm_customers'), nullable=False, info={'verbose_name': 'Идентификатор покупателя', 'category': 'table_id'})
    transactions_id = db.Column(db.Integer, db.ForeignKey('amocrm_transactions.id', name='amocrm_transactions_facts_amocrm_transactions'), nullable=False, info={'verbose_name': 'Идентификатор транзакции', 'category': 'table_id'})
    dates_id = db.Column(db.Integer, db.ForeignKey('general_dates.id', name='amocrm_transactions_facts_general_dates'), nullable=False, info={'verbose_name': 'Идентификатор даты', 'category': 'table_id'})
    companies_id = db.Column(db.Integer, db.ForeignKey('amocrm_companies.id', name='amocrm_transactions_facts_amocrm_companies'), nullable=False, info={'verbose_name': 'Идентификатор компании', 'category': 'table_id'})
    contacts_id = db.Column(db.Integer, db.ForeignKey('amocrm_contacts.id', name='amocrm_transactions_facts_amocrm_contacts'), nullable=False, info={'verbose_name': 'Идентификатор контакта', 'category': 'table_id'})
    users_id = db.Column(db.Integer, db.ForeignKey('amocrm_users.id', name='amocrm_transactions_facts_amocrm_users'), nullable=False, info={'verbose_name': 'Идентификатор пользователя', 'category': 'table_id'})
    price = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Сумма'})

    general_dates = db.relationship('GeneralDate', foreign_keys=dates_id)
    amocrm_customers = db.relationship('AmoCrmCustomer', foreign_keys=customers_id)
    amocrm_companies = db.relationship('AmoCrmCompany', foreign_keys=companies_id)
    amocrm_contacts = db.relationship('AmoCrmContact', foreign_keys=contacts_id)
    amocrm_transactions = db.relationship('AmoCrmTransaction', foreign_keys=transactions_id)
    amocrm_users = db.relationship('AmoCrmUser', foreign_keys=users_id)

    __table_args__ = (
        db.UniqueConstraint(account_id, transactions_id, name='amocrm_transactions_facts_idx_1'),
        db.Index('amocrm_transactions_facts_idx_2', dates_id),
        db.Index('amocrm_transactions_facts_idx_3', customers_id),
    )

    def __repr__(self):
        return '<AmoCrmTransactionFact %r>' % self.id


class AmoCrmTransaction(db.Model):
    __tablename__ = 'amocrm_transactions'
    __humanname__ = 'Параметры транзакций'
    __order__ = 3

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор транзакции', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    transaction_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Внутренний идентификатор транзакции'})
    comment = db.Column(db.Unicode(256), info={'verbose_name': 'Комментарий'})

    __table_args__ = (
        db.UniqueConstraint(account_id, transaction_id, name='amocrm_transactions_idx_1'),
    )

    def __repr__(self):
        return '<AmoCrmTransaction %r>' % self.id


class AmoCrmCustomerElementFact(db.Model):
    __tablename__ = 'amocrm_customers_elements_facts'
    __humanname__ = 'Элементы покупателей'
    __order__ = 1

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    elements_id = db.Column(db.Integer, db.ForeignKey('amocrm_elements.id', name='amocrm_customers_elements_facts_amocrm_elements'), nullable=False, info={'verbose_name': 'Идентификатор элемента', 'category': 'table_id'})
    customers_id = db.Column(db.Integer, db.ForeignKey('amocrm_customers.id', name='amocrm_customers_elements_facts_amocrm_customers'), nullable=False, info={'verbose_name': 'Идентификатор покупателя', 'category': 'table_id'})
    created_id = db.Column(db.Integer, db.ForeignKey('general_dates.id', name='amocrm_customers_elements_facts_general_dates_created'), nullable=False, info={'verbose_name': 'Идентификатор даты создания', 'category': 'table_id'})
    expected_id = db.Column(db.Integer, db.ForeignKey('general_dates.id', name='amocrm_customers_elements_facts_general_dates_expected'), nullable=False, info={'verbose_name': 'Идентификатор даты следующей покупки', 'category': 'table_id'})
    companies_id = db.Column(db.Integer, db.ForeignKey('amocrm_companies.id', name='amocrm_customers_elements_facts_amocrm_companies'), nullable=False, info={'verbose_name': 'Идентификатор компании', 'category': 'table_id'})
    contacts_id = db.Column(db.Integer, db.ForeignKey('amocrm_contacts.id', name='amocrm_customers_elements_facts_amocrm_contacts'), nullable=False, info={'verbose_name': 'Идентификатор контакта', 'category': 'table_id'})
    users_id = db.Column(db.Integer, db.ForeignKey('amocrm_users.id', name='amocrm_customers_elements_facts_amocrm_users'), nullable=False, info={'verbose_name': 'Идентификатор пользователя', 'category': 'table_id'})

    amocrm_elements = db.relationship('AmoCrmElement', foreign_keys=elements_id)
    general_dates = db.relationship('GeneralDate', foreign_keys=created_id)
    general_dates = db.relationship('GeneralDate', foreign_keys=expected_id)
    amocrm_customers = db.relationship('AmoCrmCustomer', foreign_keys=customers_id)
    amocrm_contacts = db.relationship('AmoCrmContact', foreign_keys=contacts_id)
    amocrm_companies = db.relationship('AmoCrmCompany', foreign_keys=companies_id)
    amocrm_users = db.relationship('AmoCrmUser', foreign_keys=users_id)

    __table_args__ = (
        db.UniqueConstraint(account_id, elements_id, customers_id, name='amocrm_customers_elements_facts_idx_1'),
        db.Index('amocrm_customers_elements_facts_idx_2', created_id),
    )

    def __repr__(self):
        return '<AmoCrmCustomerElementFact %r>' % self.id


class AmoCrmElementProduct(db.Model):
    __tablename__ = 'amocrm_elements_products'
    __humanname__ = 'Параметры товаров'
    __order__ = 2

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    elements_id = db.Column(db.Integer, db.ForeignKey('amocrm_elements.id', name='amocrm_elements_products_amocrm_elements'), nullable=False, info={'verbose_name': 'Идентификатор элемента', 'category': 'table_id'})
    sku = db.Column(db.Unicode(32), info={'verbose_name': 'Внутренний идентификатор товара'})
    description = db.Column(db.Unicode(256), info={'verbose_name': 'Описание'})
    unit_price = db.Column(db.Integer, info={'verbose_name': 'Цена за единицу'})
    quantity = db.Column(db.Integer, info={'verbose_name': 'Количество'})
    unit_type = db.Column(db.Unicode(16), info={'verbose_name': 'Единица измерения'})
    discount_type = db.Column(db.Unicode(16), info={'verbose_name': 'Тип скидки'})
    discount_value = db.Column(db.Integer, info={'verbose_name': 'Сумма скидки'})
    vat_rate_id = db.Column(db.Integer, info={'verbose_name': 'Идентификатор налога'})
    external_uid = db.Column(db.Unicode(32), info={'verbose_name': 'Внешний идентификатор товара'})

    amocrm_elements = db.relationship('AmoCrmElement', foreign_keys=elements_id)

    __table_args__ = (
        db.Index('amocrm_elements_products_idx_1', account_id),
        db.Index('amocrm_elements_products_idx_2', elements_id),
    )

    def __repr__(self):
        return '<AmoCrmElementProduct %r>' % self.id


class AmoCrmLeadEvent(db.Model):
    __tablename__ = 'amocrm_leads_events'
    __humanname__ = 'События сделок'
    __order__ = 2

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    leads_id = db.Column(db.Integer, db.ForeignKey('amocrm_leads.id', name='amocrm_leads_events_amocrm_leads'), nullable=False, info={'verbose_name': 'Идентификатор сделки', 'category': 'table_id'})
    event_id = db.Column(db.Unicode(32), nullable=False, info={'verbose_name': 'Внутренний идентификатор события'})
    type = db.Column(db.Unicode(64), nullable=False, info={'verbose_name': 'Тип события'})
    created_by = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Внутренний идентификатор создавшего'})
    created_at = db.Column(db.DateTime, nullable=False, info={'verbose_name': 'Дата создания'})
    value_after = db.Column(db.UnicodeText, nullable=False, info={'verbose_name': 'Состояние после'})
    value_before = db.Column(db.UnicodeText, nullable=False, info={'verbose_name': 'Состояние до'})

    amocrm_leads = db.relationship('AmoCrmLead', foreign_keys=leads_id)

    __table_args__ = (
        db.UniqueConstraint(account_id, event_id, name='amocrm_leads_events_idx_1'),
        db.Index('amocrm_leads_events_idx_2', leads_id),
        db.Index('amocrm_leads_events_idx_3', created_at),
    )

    def __repr__(self):
        return '<AmoCrmLeadEvent %r>' % self.id


class AmoCrmContactEvent(db.Model):
    __tablename__ = 'amocrm_contacts_events'
    __humanname__ = 'События контактов'
    __order__ = 2

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    contacts_id = db.Column(db.Integer, db.ForeignKey('amocrm_contacts.id', name='amocrm_contacts_events_amocrm_contacts'), nullable=False, info={'verbose_name': 'Идентификатор контакта', 'category': 'table_id'})
    event_id = db.Column(db.Unicode(32), nullable=False, info={'verbose_name': 'Внутренний идентификатор события'})
    type = db.Column(db.Unicode(64), nullable=False, info={'verbose_name': 'Тип события'})
    created_by = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Внутренний идентификатор создавшего'})
    created_at = db.Column(db.DateTime, nullable=False, info={'verbose_name': 'Дата создания'})
    value_after = db.Column(db.UnicodeText, nullable=False, info={'verbose_name': 'Состояние после'})
    value_before = db.Column(db.UnicodeText, nullable=False, info={'verbose_name': 'Состояние до'})

    amocrm_contacts = db.relationship('AmoCrmContact', foreign_keys=contacts_id)

    __table_args__ = (
        db.UniqueConstraint(account_id, event_id, name='amocrm_contacts_events_idx_1'),
        db.Index('amocrm_contacts_events_idx_2', contacts_id),
        db.Index('amocrm_contacts_events_idx_3', created_at),
    )

    def __repr__(self):
        return '<AmoCrmContactEvent %r>' % self.id


class AmoCrmCompanyEvent(db.Model):
    __tablename__ = 'amocrm_companies_events'
    __humanname__ = 'События компаний'
    __order__ = 2

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    companies_id = db.Column(db.Integer, db.ForeignKey('amocrm_companies.id', name='amocrm_companies_events_amocrm_companies'), nullable=False, info={'verbose_name': 'Идентификатор компании', 'category': 'table_id'})
    event_id = db.Column(db.Unicode(32), nullable=False, info={'verbose_name': 'Внутренний идентификатор события'})
    type = db.Column(db.Unicode(64), nullable=False, info={'verbose_name': 'Тип события'})
    created_by = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Внутренний идентификатор создавшего'})
    created_at = db.Column(db.DateTime, nullable=False, info={'verbose_name': 'Дата создания'})
    value_after = db.Column(db.UnicodeText, nullable=False, info={'verbose_name': 'Состояние после'})
    value_before = db.Column(db.UnicodeText, nullable=False, info={'verbose_name': 'Состояние до'})

    amocrm_companies = db.relationship('AmoCrmCompany', foreign_keys=companies_id)

    __table_args__ = (
        db.UniqueConstraint(account_id, event_id, name='amocrm_companies_events_idx_1'),
        db.Index('amocrm_companies_events_idx_2', companies_id),
        db.Index('amocrm_companies_events_idx_3', created_at),
    )

    def __repr__(self):
        return '<AmoCrmCompanyEvent %r>' % self.id


class AmoCrmUnsorted(db.Model):
    __tablename__ = 'amocrm_unsorted'
    __humanname__ = 'Параметры неразобранного'
    __order__ = 3

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор неразобранного', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    unsorted_id = db.Column(db.Unicode(64), nullable=False, info={'verbose_name': 'Внутренний идентификатор неразобранного'})
    source_uid = db.Column(db.Unicode(64), info={'verbose_name': 'Внутренний идентификатор источника заявки'})
    source_name = db.Column(db.Unicode(128), info={'verbose_name': 'Название источника заявки'})
    category = db.Column(db.Unicode(16), info={'verbose_name': 'Категория неразобранного'})
    unsorted_metadata = db.Column(db.UnicodeText, info={'verbose_name': 'Метаданные заявки'})
    is_deleted = db.Column(db.Boolean, nullable=False, info={'verbose_name': 'Неразобранное удалено', 'category': 'excluded'})

    __table_args__ = (
        db.Index('amocrm_unsorted_idx_1', account_id, unsorted_id),
    )

    def __repr__(self):
        return '<AmoCrmUnsorted %r>' % self.id


class AmoCrmTaskEvent(db.Model):
    __tablename__ = 'amocrm_tasks_events'
    __humanname__ = 'События задач'
    __order__ = 2

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    tasks_id = db.Column(db.Integer, db.ForeignKey('amocrm_tasks.id', name='amocrm_tasks_events_amocrm_tasks'), nullable=False, info={'verbose_name': 'Идентификатор задачи', 'category': 'table_id'})
    event_id = db.Column(db.Unicode(32), nullable=False, info={'verbose_name': 'Внутренний идентификатор события'})
    type = db.Column(db.Unicode(64), nullable=False, info={'verbose_name': 'Тип события'})
    created_by = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Внутренний идентификатор создавшего'})
    created_at = db.Column(db.DateTime, nullable=False, info={'verbose_name': 'Дата создания'})
    value_after = db.Column(db.UnicodeText, nullable=False, info={'verbose_name': 'Состояние после'})
    value_before = db.Column(db.UnicodeText, nullable=False, info={'verbose_name': 'Состояние до'})

    amocrm_tasks = db.relationship('AmoCrmTask', foreign_keys=tasks_id)

    __table_args__ = (
        db.UniqueConstraint(account_id, event_id, name='amocrm_tasks_events_idx_1'),
        db.Index('amocrm_tasks_events_idx_2', tasks_id),
        db.Index('amocrm_tasks_events_idx_3', created_at),
    )

    def __repr__(self):
        return '<AmoCrmTaskEvent %r>' % self.id


class AmoCrmCustomerNote(db.Model):
    __tablename__ = 'amocrm_customers_notes'
    __humanname__ = 'Примечания покупателей'
    __order__ = 2

    id = db.Column(db.Integer, primary_key=True, info={'verbose_name': 'Идентификатор записи', 'category': 'table_id'})
    account_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор подключенного аккаунта', 'category': 'table_id'})
    customers_id = db.Column(db.Integer, db.ForeignKey('amocrm_customers.id', name='amocrm_customers_notes_amocrm_customers'), nullable=False, info={'verbose_name': 'Идентификатор покупателя'})
    creator_id = db.Column(db.Integer, info={'verbose_name': 'Внутренний идентификатор создавшего'})
    responsible_id = db.Column(db.Integer, info={'verbose_name': 'Внутренний идентификатор ответственного'})
    note_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Внутренний идентификатор примечания'})
    note_type = db.Column(db.Unicode(64), info={'verbose_name': 'Тип примечания'})
    note_type_id = db.Column(db.Integer, nullable=False, info={'verbose_name': 'Идентификатор типа примечания'})
    created_at = db.Column(db.DateTime, nullable=False, info={'verbose_name': 'Дата создания'})
    updated_at = db.Column(db.DateTime, nullable=False, info={'verbose_name': 'Дата изменения'})
    text = db.Column(db.UnicodeText, info={'verbose_name': 'Текст примечания'})
    params = db.Column(db.UnicodeText, info={'verbose_name': 'Дополнительные параметры'})

    amocrm_customers = db.relationship('AmoCrmCustomer', foreign_keys=customers_id)

    __table_args__ = (
        db.Index('amocrm_customers_notes_idx_1', account_id, note_id),
        db.Index('amocrm_customers_notes_idx_2', customers_id),
        db.Index('amocrm_customers_notes_idx_3', created_at),
    )

    def __repr__(self):
        return '<AmoCrmCustomerNote %r>' % self.id
