import enum

from sqlalchemy import Column, Integer, Text, Enum

from model.entity_base import Base


class Gender(enum.Enum):
    male = 1
    female = 2
    undefined = 3


class LookingFor(enum.Enum):
    friend = 1
    activityPartner = 2
    worshipPartner = 3
    date = 4
    talkEmailBuddy = 5
    longTermRelationship = 6
    marriagePartner = 7
    Anything = 8
    undefined = 9


class ChurchAttendance(enum.Enum):
    onSpecialOccasion = 1
    severalTimesAYear = 2
    onceOrTwiceAMonth = 3
    everyWeek = 4
    noAnswer = 5
    undefined = 6


class Drink(enum.Enum):
    no = 1
    oneOrTwoOnOccasion = 2
    socially = 3
    oftenIeMoreThanThreeTimesAWeek = 4
    undefined = 5


class Smoke(enum.Enum):
    no = 1
    occasionally = 2
    often = 3
    undefined = 4


class BodyType(enum.Enum):
    slender = 1
    athletic = 2
    average = 3
    aFewExtraPounds = 4
    bigAndTallBBW = 5
    muscular = 6
    voluptuous = 7
    petite = 8
    wellProportioned = 9
    thick = 10
    bigGuy = 11
    curvyCurvaceous = 12
    fullFigured = 13
    undefined = 14


class Denomination(enum.Enum):
    seventhDayAdventist = 1
    anglican = 2
    apostolicAssemblyOfGod = 3
    baptist = 4
    catholic = 5
    charismatic = 6
    christianReformed = 7
    churchOfChrist = 8
    churchOfGod = 9
    episcopalian = 10
    evangelical = 11
    interdenominational = 12
    lutheran = 13
    mennonite = 14
    messianic = 15
    methodist = 16
    missionaryAlliance = 17
    nazarene = 18
    nonDenominational = 19
    notSureYet = 20
    orthodox = 21
    pentecostal = 22
    presbyterian = 23
    protestant = 24
    reformed = 25
    southernBaptist = 26
    united = 27
    unitedPentecostalChurch = 28
    other = 29
    undefined = 30


class EducationLevel(enum.Enum):
    someSchool = 1
    GED = 2
    highSchoolGraduate = 3
    specialtyTradeSchool = 4
    someCollege = 5
    twoYearCollegeDegree = 6
    fourYearCollegeDegree = 7
    mastersPostGrad = 8
    phDDoctorate = 9
    undefined = 10


class MaritalStatus(enum.Enum):
    single = 1
    divorced = 2
    separated = 3
    widowed = 4
    undefined = 5


class Ethnicity(enum.Enum):
    africanAmerican = 1
    caucasian = 2
    european = 3
    hispanic = 4
    indian = 5
    middleEastern = 6
    african = 7
    nativeAmericanIndian = 8
    asian = 9
    pacificIslander = 10
    caribbean = 11
    mixedRace = 12
    black = 13
    other = 14
    undefined = 15


class HairColor(enum.Enum):
    black = 1
    blonde = 2
    brown = 3
    red = 4
    grey = 5
    white = 6
    silver = 7
    saltAndPepper = 8
    bald = 9
    mixed = 10
    undefined = 11


class EyeColor(enum.Enum):
    brown = 1
    blue = 2
    green = 3
    hazel = 4
    black = 5
    grey = 6
    undefined = 7


class UserWantsChildren(enum.Enum):
    wantChildren = 1
    doesNotWantChildren = 2
    undecidedOpen = 3
    undefined = 4


class UserWithChildren(enum.Enum):
    yes = 1
    no = 2
    yesButTheyAreGrown = 3
    yesButNotLivingAtHome = 4
    undefined = 5


class WillingToRelocate(enum.Enum):
    noWay = 1
    sureWhyNot = 2
    possiblyWhoKnows = 3
    undefined = 4


class Profile(Base):

    __tablename__ = 'profiles_v3'

    id = Column(Integer, primary_key=True)
    url = Column(Text)
    gender = Column(Enum(Gender))
    country = Column(Text)
    city = Column(Text)
    state = Column(Text)
    height_cm = Column(Integer)
    age = Column(Integer)
    eye_color = Column(Enum(EyeColor))
    body_type = Column(Enum(BodyType))
    hair_color = Column(Enum(HairColor))
    ethnicity = Column(Enum(Ethnicity))
    denomination = Column(Enum(Denomination))
    photo_urls = Column(Text)
    photoLocations = Column(Text)
    looking_for = Column(Enum(LookingFor))
    church_name = Column(Text)
    church_attendance = Column(Enum(ChurchAttendance))
    church_raised_in = Column(Text)
    drink = Column(Enum(Drink))
    smoke = Column(Enum(Smoke))
    willing_to_relocate = Column(Enum(WillingToRelocate))
    marital_status = Column(Enum(MaritalStatus))
    have_children = Column(Enum(UserWithChildren))
    want_children = Column(Enum(UserWantsChildren))
    education_level = Column(Enum(EducationLevel))
    profession = Column(Text)
    interests = Column(Text)
    about_me = Column(Text)
    first_date = Column(Text)
    account_settings_criteria = Column(Text)
