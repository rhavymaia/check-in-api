from common.database import db
from sqlalchemy.dialects.mysql import DECIMAL, TINYINT


class ConferenceModel(db.Model):
    __bind_key__ = 'ocs'
    __tablename__ = 'conferences'
    conference_id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(32))
    enabled = db.Column(db.Integer)
    settings = db.relationship('ConferenceSettingsModel', lazy='dynamic')
    scheds = db.relationship('SchedConfsModel', lazy='dynamic')


class ConferenceSettingsModel(db.Model):
    __bind_key__ = 'ocs'
    __tablename__ = 'conference_settings'

    conference_id = db.Column(db.Integer,
                              db.ForeignKey(ConferenceModel.conference_id))
    setting_name = db.Column(db.String(255), primary_key=True)
    setting_value = db.Column(db.Text, primary_key=True)
    setting_type = db.Column(db.String(6))
    locale = db.Column(db.String(5))


class SchedConfsModel(db.Model):
    __bind_key__ = 'ocs'
    __tablename__ = 'sched_confs'

    sched_conf_id = db.Column(db.Integer, primary_key=True)
    conference_id = db.Column(db.Integer,
                              db.ForeignKey(ConferenceModel.conference_id))
    path = db.Column(db.String(32))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    settings = db.relationship('SchedConfSettingsModel', lazy='dynamic')
    registrations = db.relationship('RegistrationsModel', lazy='dynamic')

    def __str__(self):
        return '<SchedConfs-OCS sched_conf_id=%d, conference_id=%d>' % (self.sched_conf_id, self.conference_id)

class SchedConfSettingsModel(db.Model):
    __bind_key__ = 'ocs'
    __tablename__ = 'sched_conf_settings'

    sched_conf_id = db.Column(db.Integer,
                              db.ForeignKey(SchedConfsModel.sched_conf_id))
    locale = db.Column(db.String(5))
    setting_name = db.Column(db.String(255), primary_key=True)
    setting_value = db.Column(db.Text)
    setting_type = db.Column(db.String(6))


class UserModel(db.Model):
    __bind_key__ = 'ocs'
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40))
    middle_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    email = db.Column(db.String(90))
    cpf = db.Column(db.String(11))

    def __str__(self):
        return '<UserModel-OCS %s %s %s, %s, %s>' % (self.first_name, self.middle_name,
                                             self.last_name, self.email, self.cpf)


class RegistrationsModel(db.Model):
    __bind_key__ = 'ocs'
    __tablename__ = 'registrations'

    registration_id = db.Column(db.Integer, primary_key=True)
    sched_conf_id = db.Column(db.Integer,
                              db.ForeignKey(SchedConfsModel.sched_conf_id))
    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.user_id))
    type_id = db.Column(db.Integer)
    user = db.relationship('UserModel')


class RegistrationTypesModel(db.Model):
    __bind_key__ = 'ocs'
    __tablename__ = 'registration_types'

    type_id = db.Column(db.Integer, primary_key=True)
    sched_conf_id = db.Column(db.Integer,
                              db.ForeignKey(SchedConfsModel.sched_conf_id))
    settings = db.relationship('RegistrationTypeSettingsModel',
                               backref='registration_types',
                               lazy='dynamic')

    def __str__(self):
        return '<RegistrationTypesModel-OCS %d>' % self.type_id


class RegistrationTypeSettingsModel(db.Model):
    __bind_key__ = 'ocs'
    __tablename__ = 'registration_type_settings'

    type_id = db.Column(db.Integer,
                        db.ForeignKey('registration_types.type_id'),
                        primary_key=True)
    setting_name = db.Column(db.String(255), primary_key=True)
    setting_value = db.Column(db.Text)


class BuildingsModel(db.Model):
    __bind_key__ = 'ocs'
    __tablename__ = 'buildings'

    building_id = db.Column(db.Integer, primary_key=True)
    sched_conf_id = db.Column(db.Integer,
                              db.ForeignKey(SchedConfsModel.sched_conf_id))
    settings = db.relationship('BuildingSettingsModel',
                               backref='buildings_settings',
                               lazy='dynamic')

    def __str__(self):
        return '<BuildingsModel-OCS %d>' % (self.building_id)


class BuildingSettingsModel(db.Model):
    __bind_key__ = 'ocs'
    __tablename__ = 'building_settings'

    building_id = db.Column(db.Integer,
                            db.ForeignKey('buildings.building_id'),
                            primary_key=True)
    setting_name = db.Column(db.String(255), primary_key=True)
    setting_value = db.Column(db.Text)


class RoomsModel(db.Model):
    __bind_key__ = 'ocs'
    __tablename__ = 'rooms'

    room_id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer,
                            db.ForeignKey('buildings.building_id'),
                            primary_key=True)
    settings = db.relationship('RoomSettingsModel',
                               backref='room_settings',
                               lazy='dynamic')

    def __str__(self):
        return '<RoomsModel-OCS %d>' % self.room_id


class RoomSettingsModel(db.Model):
    __bind_key__ = 'ocs'
    __tablename__ = 'room_settings'

    room_id = db.Column(db.Integer,
                        db.ForeignKey('rooms.room_id'),
                        primary_key=True)
    setting_name = db.Column(db.String(255), primary_key=True)
    setting_value = db.Column(db.Text)

class PapersModel(db.Model):
    __bind_key__ = 'ocs'
    __tablename__ = 'papers'

    paper_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                              db.ForeignKey(UserModel.user_id))
    sched_conf_id = db.Column(db.Integer,
                              db.ForeignKey(SchedConfsModel.conference_id))
    status = db.Column(db.Integer)
    submission_progress = db.Column(db.Integer)
    current_stage = db.Column(db.Integer)
    date_to_presentations = db.Column(db.DateTime)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    # Relacionamentos
    user = db.relationship('UserModel')
    settings = db.relationship('PaperSettingsModel',
                               backref='paper_settings',
                               lazy='dynamic')
    sched_conf = db.relationship('SchedConfsModel',
                                 backref='sched_confs')

    def __str__(self):
        return '<Paper-OCS %d>' % self.paper_id

class PaperSettingsModel(db.Model):
    __bind_key__ = 'ocs'
    __tablename__ = 'paper_settings'

    paper_id = db.Column(db.Integer,
                              db.ForeignKey(PapersModel.paper_id))
    locale = db.Column(db.String(5))
    setting_name = db.Column(db.String(255), primary_key=True)
    setting_value = db.Column(db.Text)
    setting_type = db.Column(db.String(6))

class PaperAuthorsModel(db.Model):
    __bind_key__ = 'ocs'
    __tablename__ = 'paper_authors'

    author_id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.Integer,
                        db.ForeignKey(PapersModel.paper_id))
    first_name = db.Column(db.String(40))
    middle_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    email = db.Column(db.String(90))

    # Relacionamentos
    paper = db.relationship('PapersModel', backref='papers')

    def __str__(self):
        return '<PaperAuthorsModel-OCS %s, %s, %s>' % (self.first_name,
                                                       self.middle_name,
                                                       self.last_name)
    def __repr__(self):
        return self.__str__()

class PublishedPapersModel(db.Model):
    __bind_key__ = 'ocs'
    __tablename__ = 'published_papers'

    pub_id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.Integer,
                         db.ForeignKey(PapersModel.paper_id))
    sched_conf_id = db.Column(db.Integer,
                              db.ForeignKey(SchedConfsModel.conference_id))
    room_id = db.Column(db.Integer,
                              db.ForeignKey(RoomsModel.room_id))
    date_published = db.Column(db.DateTime)
    # Relacionamentos
    paper = db.relationship('PapersModel')
    sched_conf = db.relationship('SchedConfsModel')
    room = db.relationship('RoomsModel', backref='rooms')

    def __init__(self, paper, sched_conf, room):
        self.paper = paper
        self.sched_conf = sched_conf
        self.room = room

    def __str__(self):
        return '<PublishedPapersModel-OCS %d, %s>' % (self.pub_id, self.room_id)


class TracksModel(db.Model):
    __bind_key__ = 'ocs'
    __tablename__ = 'tracks'

    track_id = db.Column(db.Integer, primary_key=True)
    # FK
    sched_conf_id = db.Column(db.Integer,
                              db.ForeignKey(SchedConfsModel.conference_id))

    settings = db.relationship('TrackSettingsModel',
                               backref='track_settings',
                               lazy='dynamic')

    # Relacionamentos
    sched_conf = db.relationship('SchedConfsModel')

    def __str__(self):
        return '<TracksModel-OCS %d, %d>' % (self.track_id, self.sched_conf_id)

class TrackSettingsModel(db.Model):
    __bind_key__ = 'ocs'
    __tablename__ = 'track_settings'

    track_id = db.Column(db.Integer,
                              db.ForeignKey(TracksModel.track_id))
    locale = db.Column(db.String(5))
    setting_name = db.Column(db.String(255), primary_key=True)
    setting_value = db.Column(db.Text)
    setting_type = db.Column(db.String(6))
