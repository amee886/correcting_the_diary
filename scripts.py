import random


def fix_marks(schoolkid):
    bad_marks = Mark.objects.filter(
        schoolkid=schoolkid,
        points__in=[2, 3]
    )
    
    for mark in bad_marks:
        mark.points = 5
        mark.save()


def remove_chastisements(schoolkid):
    bad_chastisements=Chastisement.objects.filter(schoolkid=schoolkid).delete()

    
def create_commendation(name,subject):
    children = Schoolkid.objects.filter(full_name__contains=name)
    if not children.exists():
        return "Ученик не найден"
    if children.count() > 1:
        return "Найдено несколько учеников"
    child = children.first()
    text=["Молодец!","Отлично!","Хорошо!","Сказано здорово – просто и ясно!","Ты меня очень обрадовал!","Ты меня приятно удивил!","Я поражен!"]
    praise = random.choice(text)
    lesson=Lesson.objects.filter(year_of_study=child.year_of_study,group_letter=child.group_letter,subject__title=subject).first()
    if not lesson:
        return "Урок не найден"
    Commendation.objects.create(schoolkid=child,subject=lesson.subject,teacher=lesson.teacher,text=praise,created=lesson.date)
