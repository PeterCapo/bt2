from app import db


class Bucketlist(db.Model):
    """This class represents the bucketlist table."""

    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    shortcode = db.Column(db.Integer)
    msisdn = db.Column(db.Integer)
    commandid = db.Column(db.String(255))
    billrefnumber = db.Column(db.String(255))
    refno = db.Column(db.String(255))

    def __init__(
                self, name,
                shortcode, msisdn, commandid, billrefnumber,
                refno):
        """initialize with name."""
        self.name = name
        self.shortcode = shortcode
        self.msisdn = msisdn
        self.commandid = commandid
        self.billrefnumber = billrefnumber
        self.refno = refno

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Bucketlist.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Bucketlist: {}>".format(self.name)
