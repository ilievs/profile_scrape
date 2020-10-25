import enum

from sqlalchemy import Column, Integer, Text, Enum

from model.entity_base import Base


class Gender(str, enum.Enum):
    male = 'male'
    female = 'female'
    undefined = 'undefined'


class LookingFor(str, enum.Enum):
    friend = 'friend'
    activityPartner = 'activityPartner'
    worshipPartner = 'worshipPartner'
    date = 'date'
    talkEmailBuddy = 'talkEmailBuddy'
    longTermRelationship = 'longTermRelationship'
    marriagePartner = 'marriagePartner'
    Anything = 'anything'
    undefined = 'undefined'


class ChurchAttendance(str, enum.Enum):
    onSpecialOccasion = 'onSpecialOccasion'
    severalTimesAYear = 'severalTimesAYear'
    onceOrTwiceAMonth = 'onceOrTwiceAMonth'
    everyWeek = 'everyWeek'
    noAnswer = 'noAnswer'
    undefined = 'undefined'


class Drink(str, enum.Enum):
    no = 'no'
    oneOrTwoOnOccasion = 'oneOrTwoOnOccasion'
    socially = 'socially'
    oftenIeMoreThanThreeTimesAWeek = 'oftenIeMoreThanThreeTimesAWeek'
    undefined = 'undefined'


class Smoke(str, enum.Enum):
    no = 'no'
    occasionally = 'occasionally'
    often = 'often'
    undefined = 'undefined'


class BodyType(str, enum.Enum):
    slender = 'slender'
    athletic = 'athletic'
    average = 'average'
    aFewExtraPounds = 'aFewExtraPounds'
    bigAndTallBBW = 'bigAndTallBBW'
    muscular = 'muscular'
    voluptuous = 'voluptuous'
    petite = 'petite'
    wellProportioned = 'wellProportioned'
    thick = 'thick'
    bigGuy = 'bigGuy'
    curvyCurvaceous = 'curvyCurvaceous'
    fullFigured = 'fullFigured'
    undefined = 'undefined'


class Denomination(str, enum.Enum):
    seventhDayAdventist = 'seventhDayAdventist'
    anglican = 'anglican'
    apostolicAssemblyOfGod = 'apostolicAssemblyOfGod'
    baptist = 'baptist'
    catholic = 'catholic'
    charismatic = 'charismatic'
    christianReformed = 'christianReformed'
    churchOfChrist = 'churchOfChrist'
    churchOfGod = 'churchOfGod'
    episcopalian = 'episcopalian'
    evangelical = 'evangelical'
    interdenominational = 'interdenominational'
    lutheran = 'lutheran'
    mennonite = 'mennonite'
    messianic = 'messianic'
    methodist = 'methodist'
    missionaryAlliance = 'missionaryAlliance'
    nazarene = 'nazarene'
    nonDenominational = 'nonDenominational'
    notSureYet = 'notSureYet'
    orthodox = 'orthodox'
    pentecostal = 'pentecostal'
    presbyterian = 'presbyterian'
    protestant = 'protestant'
    reformed = 'reformed'
    southernBaptist = 'southernBaptist'
    united = 'united'
    unitedPentecostalChurch = 'unitedPentecostalChurch'
    other = 'other'
    undefined = 'undefined'


class EducationLevel(str, enum.Enum):
    someSchool = 'someSchool'
    GED = 'GED'
    highSchoolGraduate = 'highSchoolGraduate'
    specialtyTradeSchool = 'specialtyTradeSchool'
    someCollege = 'someCollege'
    twoYearCollegeDegree = 'twoYearCollegeDegree'
    fourYearCollegeDegree = 'fourYearCollegeDegree'
    mastersPostGrad = 'mastersPostGrad'
    phDDoctorate = 'phDDoctorate'
    undefined = 'undefined'


class MaritalStatus(str, enum.Enum):
    single = 'single'
    divorced = 'divorced'
    separated = 'separated'
    widowed = 'widowed'
    undefined = 'undefined'


class Ethnicity(str, enum.Enum):
    africanAmerican = 'africanAmerican'
    caucasian = 'caucasian'
    european = 'european'
    hispanic = 'hispanic'
    indian = 'indian'
    middleEastern = 'middleEastern'
    african = 'african'
    nativeAmericanIndian = 'nativeAmericanIndian'
    asian = 'asian'
    pacificIslander = 'pacificIslander'
    caribbean = 'caribbean'
    mixedRace = 'mixedRace'
    black = 'black'
    other = 'other'
    undefined = 'undefined'


class HairColor(str, enum.Enum):
    black = 'black'
    blonde = 'blonde'
    brown = 'brown'
    red = 'red'
    grey = 'grey'
    white = 'white'
    silver = 'silver'
    saltAndPepper = 'saltAndPepper'
    bald = 'bald'
    mixed = 'mixed'
    undefined = 'undefined'


class EyeColor(str, enum.Enum):
    brown = 'brown'
    blue = 'blue'
    green = 'green'
    hazel = 'hazel'
    black = 'black'
    grey = 'grey'
    undefined = 'undefined'


class UserWantsChildren(str, enum.Enum):
    wantChildren = 'wantChildren'
    doesNotWantChildren = 'doesNotWantChildren'
    undecidedOpen = 'undecidedOpen'
    undefined = 'undefined'


class UserWithChildren(str, enum.Enum):
    yes = 'yes'
    no = 'no'
    yesButTheyAreGrown = 'yesButTheyAreGrown'
    yesButNotLivingAtHome = 'yesButNotLivingAtHome'
    undefined = 'undefined'


class WillingToRelocate(str, enum.Enum):
    noWay = 'noWay'
    sureWhyNot = 'sureWhyNot'
    possiblyWhoKnows = 'possiblyWhoKnows'
    undefined = 'undefined'


class Profile(Base):

    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    description = Column(Text)
    url = Column(Text)
    gender = Column(Enum(Gender))
    country = Column(Text)
    city = Column(Text)
    state = Column(Text)
    height = Column(Integer)
    age = Column(Integer)
    eye_color = Column(Enum(EyeColor))
    body_type = Column(Enum(BodyType))
    hair_color = Column(Enum(HairColor))
    ethnicity = Column(Enum(Ethnicity))
    denomination = Column(Enum(Denomination))
    image_urls = Column(Text)
    image_paths = Column(Text)
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
