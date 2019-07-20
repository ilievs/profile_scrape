from model.profile import *

gender_to_enum_mapping = {
    'Male': Gender.male,
    'Female': Gender.female,
}

looking_for_to_enum_mapping = {
    'A Friend': LookingFor.friend,
    'An Activity Partner': LookingFor.activityPartner,
    'A Worship Partner': LookingFor.worshipPartner,
    'A Date': LookingFor.date,
    'A Talk/Email Buddy': LookingFor.talkEmailBuddy,
    'A Long Term Relationship': LookingFor.longTermRelationship,
    'A Marriage Partner': LookingFor.marriagePartner,
    'Anything': LookingFor.Anything,
}

church_attendance_to_enum_mapping = {
    'On special occasion': ChurchAttendance.onSpecialOccasion,
    'Several times a year': ChurchAttendance.severalTimesAYear,
    'Once or Twice a month': ChurchAttendance.onceOrTwiceAMonth,
    'Every week': ChurchAttendance.everyWeek,
    'No answer': ChurchAttendance.noAnswer,
}

drink_to_enum_mapping = {
    'No': Drink.no,
    '1 or 2 on occasion': Drink.oneOrTwoOnOccasion,
    'Socially': Drink.socially,
    'Often(>3 Times/Week)': Drink.oftenIeMoreThanThreeTimesAWeek,
}

smoke_to_enum_mapping = {
    'No': Smoke.no,
    'Occasionally': Smoke.occasionally,
    'Often': Smoke.often,
}

body_type_to_enum_mapping = {
    'Slender': BodyType.slender,
    'Athletic': BodyType.athletic,
    'Average': BodyType.average,
    'A Few Extra Pounds': BodyType.aFewExtraPounds,
    'Big & Tall/BBW': BodyType.bigAndTallBBW,
    'Muscular': BodyType.muscular,
    'Voluptuous': BodyType.voluptuous,
    'Petite': BodyType.petite,
    'Well Proportioned': BodyType.wellProportioned,
    'Thick': BodyType.thick,
    'Big Guy': BodyType.bigGuy,
    'Curvy/Curvaceous': BodyType.curvyCurvaceous,
    'Full Figured': BodyType.fullFigured,
}

denomination_to_enum_mapping = {
    '7th Day Adventist': Denomination.seventhDayAdventist,
    'Anglican': Denomination.anglican,
    'Apostolic Assembly of God': Denomination.apostolicAssemblyOfGod,
    'Baptist': Denomination.baptist,
    'Catholic': Denomination.catholic,
    'Charismatic': Denomination.charismatic,
    'Christian Reformed': Denomination.christianReformed,
    'Church of Christ': Denomination.churchOfChrist,
    'Church of God': Denomination.churchOfGod,
    'Episcopalian': Denomination.episcopalian,
    'Evangelical': Denomination.evangelical,
    'Interdenominational': Denomination.interdenominational,
    'Lutheran': Denomination.lutheran,
    'Mennonite': Denomination.mennonite,
    'Messianic': Denomination.messianic,
    'Methodist': Denomination.methodist,
    'Missionary Alliance': Denomination.missionaryAlliance,
    'Nazarene': Denomination.nazarene,
    'Non-Denominational': Denomination.nonDenominational,
    'Not sure yet': Denomination.notSureYet,
    'Orthodox': Denomination.orthodox,
    'Pentecostal': Denomination.pentecostal,
    'Presbyterian': Denomination.presbyterian,
    'Protestant': Denomination.protestant,
    'Reformed': Denomination.reformed,
    'Southern Baptist': Denomination.southernBaptist,
    'United': Denomination.united,
    'United Pentecostal Church': Denomination.unitedPentecostalChurch,
    'Other': Denomination.other,
}

edu_level_to_enum_mapping = {
    'Some School': EducationLevel.someSchool,
    'GED': EducationLevel.GED,
    'HS Graduate': EducationLevel.highSchoolGraduate,
    'Specialty/Trade School': EducationLevel.specialtyTradeSchool,
    'Some College': EducationLevel.someCollege,
    '2 Yr College Degree': EducationLevel.twoYearCollegeDegree,
    '4 Yr College Degree': EducationLevel.fourYearCollegeDegree,
    'Masters/Post Grad': EducationLevel.mastersPostGrad,
    'Ph.D./Doctorate': EducationLevel.phDDoctorate,
}

marital_status_to_enum_mapping = {
    'Single': MaritalStatus.single,
    'Divorced': MaritalStatus.divorced,
    'Separated': MaritalStatus.separated,
    'Widowed': MaritalStatus.widowed,
}

ethnicity_to_enum_mapping = {
    'African American': Ethnicity.africanAmerican,
    'Caucasian': Ethnicity.caucasian,
    'European': Ethnicity.european,
    'Hispanic': Ethnicity.hispanic,
    'Indian': Ethnicity.indian,
    'MiddleEastern': Ethnicity.middleEastern,
    'African': Ethnicity.african,
    'Native American (Indian)': Ethnicity.nativeAmericanIndian,
    'Asian': Ethnicity.asian,
    'Pacific Islander': Ethnicity.pacificIslander,
    'Caribbean': Ethnicity.caribbean,
    'Mixed Race': Ethnicity.mixedRace,
    'Black': Ethnicity.black,
    'Other Ethnicity': Ethnicity.other,
}

hair_color_to_enum_mapping = {
    'Black': HairColor.black,
    'Blonde': HairColor.blonde,
    'Brown': HairColor.brown,
    'Red': HairColor.red,
    'Grey': HairColor.grey,
    'White': HairColor.white,
    'Silver': HairColor.silver,
    'Salt n Pepper': HairColor.saltAndPepper,
    'Bald': HairColor.bald,
    'Mixed Color': HairColor.mixed,
}

ey_color_to_enum_mapping = {
    'Brown': EyeColor.brown,
    'Blue': EyeColor.blue,
    'Green': EyeColor.green,
    'Hazel': EyeColor.hazel,
    'Black': EyeColor.black,
    'Grey': EyeColor.grey,
}

wants_children_to_enum_mapping = {
    'Want Children': UserWantsChildren.wantChildren,
    'Does Not Want Children': UserWantsChildren.doesNotWantChildren,
    'Undecided/Open': UserWantsChildren.undecidedOpen,
}

with_children_to_enum_mapping = {
    'Yes': UserWithChildren.yes,
    'No': UserWithChildren.no,
    "Yes but they're grown": UserWithChildren.yesButTheyAreGrown,
    'Yes but not living at home': UserWithChildren.yesButNotLivingAtHome,
}

relocation_to_enum_mapping = {
    'No way': WillingToRelocate.noWay,
    'Sure, who not': WillingToRelocate.sureWhyNot,
    'Possibly, who knows': WillingToRelocate.possiblyWhoKnows,
}


def get_gender(scraped_value):
    return gender_to_enum_mapping.get(scraped_value, Gender.undefined)


def get_looking_for(scraped_value):
    return looking_for_to_enum_mapping.get(scraped_value, LookingFor.undefined)


def get_church_attendance(scraped_value):
    return church_attendance_to_enum_mapping.get(scraped_value, ChurchAttendance.undefined)


def get_drink(scraped_value):
    return drink_to_enum_mapping.get(scraped_value, Drink.undefined)


def get_smoke(scraped_value):
    return smoke_to_enum_mapping.get(scraped_value, Smoke.undefined)


def get_body_type(scraped_value):
    return body_type_to_enum_mapping.get(scraped_value, BodyType.undefined)


def get_denomination(scraped_value):
    return denomination_to_enum_mapping.get(scraped_value, Denomination.undefined)


def get_education_level(scraped_value):
    return edu_level_to_enum_mapping.get(scraped_value, EducationLevel.undefined)


def get_marital_status(scraped_value):
    return marital_status_to_enum_mapping.get(scraped_value, MaritalStatus.undefined)


def get_ethnicity(scraped_value):
    return ethnicity_to_enum_mapping.get(scraped_value, Ethnicity.undefined)


def get_hair_color(scraped_value):
    return hair_color_to_enum_mapping.get(scraped_value, HairColor.undefined)


def get_eye_color(scraped_value):
    return ey_color_to_enum_mapping.get(scraped_value, EyeColor.undefined)


def get_user_wants_children(scraped_value):
    return wants_children_to_enum_mapping.get(scraped_value, UserWantsChildren.undefined)


def get_user_with_children(scraped_value):
    return with_children_to_enum_mapping.get(scraped_value, UserWithChildren.undefined)


def get_willing_to_relocate(scraped_value):
    return relocation_to_enum_mapping.get(scraped_value, WillingToRelocate.undefined)
