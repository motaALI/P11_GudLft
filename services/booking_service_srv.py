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
    
    