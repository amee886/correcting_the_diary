import random
from datacenter.models import Schoolkid
from datacenter.models import Subject
from datacenter.models import Lesson
from datacenter.models import Mark
from datacenter.models import Chastisement
from datacenter.models import Commendation
from datacenter.models import Teacher


def get_schoolkid(name):
    children = Schoolkid.objects.filter(full_name__contains=name)
    if not children.exists():
        return "Ученик не найден"
    if children.count() > 1:
        return "Найдено несколько учеников"
    return children.first()


def fix_marks(name):
    schoolkid = get_schoolkid(name)
    Mark.objects.filter(
        schoolkid=schoolkid,
        points__in=[2, 3]
    ).update(points=5)


def remove_chastisements(name):
    schoolkid = get_schoolkid(name)
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(name, subject):
    schoolkid = get_schoolkid(name)
    text = [
        "Молодец!", "Отлично!", "Хорошо!",
        "Сказано здорово – просто и ясно!",
        "Ты меня очень обрадовал!",
        "Ты меня приятно удивил!",
        "Я поражен!"
    ]
    praise = random.choice(text)
    lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject
    ).order_by("?").first()
    if not lesson:
        return "Урок не найден"
    Commendation.objects.create(
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher,
        text=praise,
        created=lesson.date
    )
