# This file is part of Indico.
# Copyright (C) 2002 - 2025 CERN
#
# Indico is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see the
# LICENSE file for more details.

"""Jalali (Persian) calendar utilities."""

from datetime import date, datetime

import jdatetime
import pytz
from babel.dates import get_timezone

from indico.util.i18n import get_current_locale


PERSIAN_MONTHS = [
    'فروردین',
    'اردیبهشت',
    'خرداد',
    'تیر',
    'مرداد',
    'شهریور',
    'مهر',
    'آبان',
    'آذر',
    'دی',
    'بهمن',
    'اسفند',
]

PERSIAN_WEEKDAYS = [
    'شنبه',      # Saturday
    'یکشنبه',    # Sunday
    'دوشنبه',    # Monday
    'سه‌شنبه',   # Tuesday
    'چهارشنبه',  # Wednesday
    'پنج‌شنبه',  # Thursday
    'جمعه',      # Friday
]

PERSIAN_WEEKDAYS_SHORT = ['ش', 'ی', 'د', 'س', 'چ', 'پ', 'ج']

PERSIAN_DIGITS = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹']


def should_use_jalali():
    """Check if Jalali calendar should be used based on current locale.

    Returns:
        bool: True if current locale is Persian (fa/fa_IR), False otherwise.
    """
    try:
        locale = get_current_locale()
        locale_str = str(locale)
        return locale_str in ('fa', 'fa_IR') or locale_str.startswith('fa_')
    except (AttributeError, RuntimeError):
        return False


def to_jalaali(dt):
    """Convert Gregorian datetime/date to Jalali.

    Args:
        dt: A datetime or date object in Gregorian calendar.

    Returns:
        jdatetime.datetime or jdatetime.date: The equivalent Jalali date/datetime.
    """
    if dt is None:
        return None

    if isinstance(dt, datetime):
        if dt.tzinfo:
            # Convert to UTC first, then to jdatetime
            utc_dt = dt.astimezone(pytz.UTC)
            return jdatetime.datetime.fromgregorian(
                datetime=utc_dt,
                locale='fa_IR'
            )
        return jdatetime.datetime.fromgregorian(
            datetime=dt,
            locale='fa_IR'
        )
    elif isinstance(dt, date):
        return jdatetime.date.fromgregorian(date=dt, locale='fa_IR')

    return None


def from_jalaali(jdt):
    """Convert Jalali datetime/date to Gregorian.

    Args:
        jdt: A jdatetime.datetime or jdatetime.date object.

    Returns:
        datetime or date: The equivalent Gregorian date/datetime.
    """
    if jdt is None:
        return None

    if isinstance(jdt, jdatetime.datetime):
        return jdt.togregorian()
    elif isinstance(jdt, jdatetime.date):
        return jdt.togregorian()

    return None


def format_jalaali_date(dt, format='medium', locale=None):
    """Format a date in Jalali calendar.

    Args:
        dt: A datetime or date object.
        format: Format string ('short', 'medium', 'long', or custom format).
        locale: Locale string (not used, kept for compatibility).

    Returns:
        str: Formatted Jalali date string.
    """
    if dt is None:
        return ''

    jdt = to_jalaali(dt)
    if jdt is None:
        return ''

    # Predefined formats
    if format == 'short':
        return jdt.strftime('%y/%m/%d', locale='fa_IR')
    elif format == 'medium':
        return jdt.strftime('%Y/%m/%d', locale='fa_IR')
    elif format == 'long':
        day = jdt.day
        month = PERSIAN_MONTHS[jdt.month - 1]
        year = jdt.year
        return f'{day} {month} {year}'
    elif format == 'full':
        weekday = PERSIAN_WEEKDAYS[jdt.weekday()]
        day = jdt.day
        month = PERSIAN_MONTHS[jdt.month - 1]
        year = jdt.year
        return f'{weekday}، {day} {month} {year}'
    elif format == 'code':
        return jdt.strftime('%d/%m/%Y', locale='fa_IR')
    else:
        # Custom format
        return jdt.strftime(format, locale='fa_IR')


def format_jalaali_datetime(dt, format='medium', locale=None, timezone=None):
    """Format a datetime in Jalali calendar.

    Args:
        dt: A datetime object.
        format: Format string ('short', 'medium', 'long', or custom format).
        locale: Locale string (not used, kept for compatibility).
        timezone: Timezone to convert to before formatting.

    Returns:
        str: Formatted Jalali datetime string.
    """
    if dt is None:
        return ''

    # Apply timezone conversion if needed
    if timezone and dt.tzinfo:
        if isinstance(timezone, str):
            timezone = get_timezone(timezone)
        dt = dt.astimezone(timezone)

    jdt = to_jalaali(dt)
    if jdt is None:
        return ''

    # Predefined formats
    if format == 'short':
        return jdt.strftime('%y/%m/%d %H:%M', locale='fa_IR')
    elif format == 'medium':
        return jdt.strftime('%Y/%m/%d %H:%M', locale='fa_IR')
    elif format == 'long':
        day = jdt.day
        month = PERSIAN_MONTHS[jdt.month - 1]
        year = jdt.year
        time_str = jdt.strftime('%H:%M', locale='fa_IR')
        return f'{day} {month} {year}، {time_str}'
    elif format == 'full':
        weekday = PERSIAN_WEEKDAYS[jdt.weekday()]
        day = jdt.day
        month = PERSIAN_MONTHS[jdt.month - 1]
        year = jdt.year
        time_str = jdt.strftime('%H:%M:%S', locale='fa_IR')
        return f'{weekday}، {day} {month} {year}، {time_str}'
    elif format == 'code':
        return jdt.strftime('%d/%m/%Y %H:%M', locale='fa_IR')
    else:
        # Custom format
        return jdt.strftime(format, locale='fa_IR')


def parse_jalaali_date(date_str, format='%Y/%m/%d'):
    """Parse a Jalali date string.

    Args:
        date_str: String representation of a Jalali date.
        format: Format string for parsing.

    Returns:
        datetime.date: Gregorian date object.
    """
    if not date_str:
        return None

    # Normalize digits first
    date_str = normalize_persian_digits(date_str)

    try:
        jdt = jdatetime.datetime.strptime(date_str, format, locale='fa_IR')
        return jdt.togregorian().date()
    except (ValueError, AttributeError):
        return None


def parse_jalaali_datetime(datetime_str, format='%Y/%m/%d %H:%M'):
    """Parse a Jalali datetime string.

    Args:
        datetime_str: String representation of a Jalali datetime.
        format: Format string for parsing.

    Returns:
        datetime: Gregorian datetime object.
    """
    if not datetime_str:
        return None

    # Normalize digits first
    datetime_str = normalize_persian_digits(datetime_str)

    try:
        jdt = jdatetime.datetime.strptime(datetime_str, format, locale='fa_IR')
        return jdt.togregorian()
    except (ValueError, AttributeError):
        return None


def normalize_persian_digits(text):
    """Convert Persian/Arabic digits to English digits.

    Args:
        text: String potentially containing Persian/Arabic digits.

    Returns:
        str: String with English digits.
    """
    if not text:
        return text

    # Persian digits
    persian_digits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹']
    # Arabic-Indic digits
    arabic_digits = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩']

    result = text
    for i in range(10):
        result = result.replace(persian_digits[i], str(i))
        result = result.replace(arabic_digits[i], str(i))

    return result


def to_persian_digits(text):
    """Convert English digits to Persian digits.

    Args:
        text: String potentially containing English digits.

    Returns:
        str: String with Persian digits.
    """
    if not text:
        return text

    result = str(text)
    for i in range(10):
        result = result.replace(str(i), PERSIAN_DIGITS[i])

    return result


def get_jalaali_month_names():
    """Get list of Jalali month names in Persian.

    Returns:
        list: List of 12 month names.
    """
    return PERSIAN_MONTHS.copy()


def get_jalaali_weekday_names(short=False):
    """Get list of weekday names in Persian.

    Args:
        short: If True, return abbreviated weekday names.

    Returns:
        list: List of 7 weekday names.
    """
    return PERSIAN_WEEKDAYS_SHORT.copy() if short else PERSIAN_WEEKDAYS.copy()


def jalaali_now():
    """Get current date/time in Jalali calendar.

    Returns:
        jdatetime.datetime: Current Jalali datetime.
    """
    return jdatetime.datetime.now(locale='fa_IR')


def jalaali_today():
    """Get current date in Jalali calendar.

    Returns:
        jdatetime.date: Current Jalali date.
    """
    return jdatetime.date.today(locale='fa_IR')
