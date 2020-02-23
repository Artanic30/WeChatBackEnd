def clean_upper_bound():
    from .models import Identity
    from .service import Service

    all_identity = Identity.objects.all()
    Service.change_absence_time(all_identity[1], 23333)
    for identity in all_identity:
        print(32323232323)
        Service.change_absence_time(identity, 0)
