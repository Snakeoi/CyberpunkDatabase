from dataclasses import dataclass


@dataclass
class _Cfg:
    prompt: str


@dataclass
class _RegexCfg:
    pattern: str
    prompt: str


@dataclass
class _LengthCfg:
    min: int
    max: int
    prompt: str


class Email:
    required = _Cfg("Hasło jest wymagane.")
    email = _Cfg("Musi być poprawnym adresem e-mail.")
    length = _LengthCfg(1, 64, "Adres e-mail jest za długi")


class Username:
    required = _Cfg("Nazwa użytkownika jest wymagana.")
    length = _LengthCfg(3, 32, "Nazwa użytkownika musi mieć od 3 do 32 znaków.")
    regex = _RegexCfg(
        r"^[^\d!@#$%^&*()_+=\[\]{}|\\:;\"<>,.?/`~]+$",
        "Nazwa użytkownika może zawierać tylko litery, spacje, myślniki i apostrofy.",
    )


class Password:
    required = _Cfg("Hasło jest wymagane.")
    length = _LengthCfg(8, 64, "Hasło musi mieć od 8 do 64 znaków.")
    regex = _RegexCfg(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).+$",
        "Hasło musi zawierać co najmniej jedną wielką literę, jedną małą literę, jedną cyfrę i znak specjalny.",
    )


class PasswordRepeat:
    required = _Cfg("Powtórzone hasło jest wymagane.")
    equal_to = _Cfg("Hasła muszą być identyczne.")


class Pin:
    regex = _RegexCfg(r"^\d\d\d\d\d\d$", "Nieprawidłowy PIN")
