from Account.models import User


def update_user_credit(obj, amount_id):
    amount_obj = obj.amount_set.filter(id=amount_id)
    obj.credits = obj.credits + amount_obj.amount
    obj.save()
    return obj

def add_credits(payment_uid):
    # The payment uid contains the joined format of the user id, the payment he/she wants and the amount
    # We are spliting it to get each value
    ids = payment_uid.split('-')
    user_uid = ids[0]
    payment_uid = ids[1]
    amount_uid = ids[2]

    # Get the user obj
    user=User.objects.get(id=user_uid)

    # Get the user payment object
    if payment_uid == 101:
        # Means mothlypayment
        return update_user_credit(user.monthlypayment, amount_uid)
    elif payment_uid == 202:
        # Means yearly payment
        return update_user_credit(user.yearlypayment, amount_uid)
    elif payment_uid == 303:
        # Means one off payment
        return update_user_credit(user.oneoffpayment, amount_uid)
    elif payment_uid == 404:
        # Means special payment
        return update_user_credit(user.specialpayment, amount_uid)

