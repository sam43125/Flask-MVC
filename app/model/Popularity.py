from app import db

class Popularity(db.Model):
    __tablename__ = 'b_popularity'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    TSMC = db.Column(db.Integer)
    AppliedMaterials = db.Column(db.Integer)
    ASML = db.Column(db.Integer)
    SUMCO = db.Column(db.Integer)
    
    def __init__(self, date, TSMC, AppliedMaterials, ASML, SUMCO):
        self.date = date
        self.TSMC = TSMC
        self.AppliedMaterials = AppliedMaterials
        self.ASML = ASML
        self.SUMCO = SUMCO

    def __repr__(self):
        return '<Popularity %r %r %r %r %r>' % (self.date, self.TSMC, self.AppliedMaterials, self.ASML, self.SUMCO)