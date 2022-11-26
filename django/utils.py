from ippanel import Client, HTTPError, Error, ResponseCode


def send_otp_code(phone_number, code):

    api_key = "4XFCCNqo5enerHlmaKIdJPpooYP4u6JQM5MPLHCBCMw="
    pattern_code = "pz13d1efn9pp93k"
    originator = "+983000505"
    sms = Client(api_key)

    try:
        pattern_values = {
            "code": code,
        }
        sms.send_pattern(
            pattern_code,  # pattern code
            originator,  # originator
            str(phone_number),  # recipient
            pattern_values,  # pattern values
        )

    except Error as e:  # ippanel sms error
        print(f"Error handled => code: {e.code}, message: {e.message}")
        if e.code == ResponseCode.ErrUnprocessableEntity.value:
            for field in e.message:
                print(f"Field: {field} , Errors: {e.message[field]}")

    except HTTPError as e:  # http error like network error, not found
        print(f"Error handled => code: {e}")


def phone_number_validator(phone_number: str) -> (bool, str):
    if phone_number[:3] != "+98":
        return False, "Phone number should start with '+98'"
    elif len(phone_number) != 13:
        if len(phone_number) < 1:
            return False, "(short) Phone number is shorter than 13 character"
        else:
            return False, "(long) Phone number is longer than 13 character"
    else:
        return True, ""




