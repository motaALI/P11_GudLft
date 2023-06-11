from datetime import date, datetime


maxAuthorathedToReserve = 12

class bookingError(Exception):
    pass

def check_club_possibility_to_reserve_places(club, placesRequired):
    point_available = club['points']
    if placesRequired > int(point_available):
        raise bookingError(f"You don't have enough points. Points remaining ({point_available})!")
    elif placesRequired > maxAuthorathedToReserve:
        raise bookingError(f"You cannot reserve more than ({maxAuthorathedToReserve}) places!")
    else:
        return True 
    

def is_competition_in_present(competition_date: datetime):
    today = datetime.now().date()
    datetime_obj = datetime.strptime(competition_date, '%Y-%m-%d %H:%M:%S')
    date_object = datetime_obj.date()
    today = date.today()
    if date_object < today:
        return False
    else:
        return True
     

def check_reservation_not_in_past(competition_date: datetime):
    today = datetime.now().date()
    try:
        if not is_competition_in_present(competition_date):
            raise bookingError("You are not able to book a place on a post-dated competition.")
    except ValueError as error:
        raise ValueError(f"An error has occurred {error}.!")

    return True

