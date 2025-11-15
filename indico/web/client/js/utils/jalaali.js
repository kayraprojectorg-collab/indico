// This file is part of Indico.
// Copyright (C) 2002 - 2025 CERN
//
// Indico is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see the
// LICENSE file for more details.

import moment from 'moment';
import jMoment from 'moment-jalaali';

// Configure moment-jalaali to load Jalaali calendar
jMoment.loadPersian({
  usePersianDigits: true,
  dialect: 'persian-modern',
});

/**
 * Get the current locale to determine if Jalali calendar should be used
 */
export function shouldUseJalali() {
  const locale = moment.locale();
  return locale === 'fa' || locale === 'fa-IR' || locale.startsWith('fa');
}

/**
 * Convert Gregorian moment to Jalaali
 */
export function toJalaali(dt) {
  if (!dt) {
    return null;
  }
  return jMoment(dt);
}

/**
 * Convert Jalaali date to Gregorian moment
 */
export function fromJalaali(jDate) {
  if (!jDate) {
    return null;
  }
  return moment(jDate.format('YYYY-MM-DD'));
}

/**
 * Format date considering locale (Jalali for Persian, Gregorian for others)
 */
export function formatDate(dt, format = 'YYYY/MM/DD') {
  if (!dt) {
    return null;
  }

  if (shouldUseJalali()) {
    return jMoment(dt).format(format);
  }

  return moment(dt).format(format);
}

/**
 * Format datetime considering locale
 */
export function formatDateTime(dt, format = 'YYYY/MM/DD HH:mm') {
  if (!dt) {
    return null;
  }

  if (shouldUseJalali()) {
    return jMoment(dt).format(format);
  }

  return moment(dt).format(format);
}

/**
 * Parse date string (handles both Jalali and Gregorian)
 */
export function parseDate(dateStr, format = 'YYYY/MM/DD') {
  if (!dateStr) {
    return null;
  }

  if (shouldUseJalali()) {
    return jMoment(dateStr, format);
  }

  return moment(dateStr, format);
}

/**
 * Get current date in appropriate calendar
 */
export function now() {
  if (shouldUseJalali()) {
    return jMoment();
  }
  return moment();
}

/**
 * Convert moment to display string based on locale
 */
export function toDisplayString(dt, includeTime = false) {
  if (!dt) {
    return '';
  }

  if (shouldUseJalali()) {
    const m = jMoment(dt);
    if (includeTime) {
      return m.format('jYYYY/jMM/jDD HH:mm');
    }
    return m.format('jYYYY/jMM/jDD');
  }

  const m = moment(dt);
  if (includeTime) {
    return m.format('YYYY/MM/DD HH:mm');
  }
  return m.format('YYYY/MM/DD');
}

/**
 * Get localized month names
 */
export function getMonthNames() {
  if (shouldUseJalali()) {
    return [
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
    ];
  }

  return moment.months();
}

/**
 * Get localized weekday names
 */
export function getWeekdayNames(short = false) {
  if (shouldUseJalali()) {
    if (short) {
      return ['ش', 'ی', 'د', 'س', 'چ', 'پ', 'ج'];
    }
    return ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه', 'جمعه'];
  }

  return short ? moment.weekdaysShort() : moment.weekdays();
}

/**
 * Create a date range in the appropriate calendar
 */
export function dateRange(start, end, step = 1, unit = 'day') {
  const result = [];
  let current;

  if (shouldUseJalali()) {
    current = jMoment(start);
    const endMoment = jMoment(end);

    while (current.isSameOrBefore(endMoment)) {
      result.push(current.clone());
      current.add(step, unit);
    }
  } else {
    current = moment(start);
    const endMoment = moment(end);

    while (current.isSameOrBefore(endMoment)) {
      result.push(current.clone());
      current.add(step, unit);
    }
  }

  return result;
}

/**
 * Get the start of a period (day, week, month, year) in appropriate calendar
 */
export function startOf(dt, unit = 'day') {
  if (!dt) {
    return null;
  }

  if (shouldUseJalali()) {
    return jMoment(dt).startOf(unit);
  }

  return moment(dt).startOf(unit);
}

/**
 * Get the end of a period (day, week, month, year) in appropriate calendar
 */
export function endOf(dt, unit = 'day') {
  if (!dt) {
    return null;
  }

  if (shouldUseJalali()) {
    return jMoment(dt).endOf(unit);
  }

  return moment(dt).endOf(unit);
}

/**
 * Get days in month for appropriate calendar
 */
export function daysInMonth(dt) {
  if (!dt) {
    return 0;
  }

  if (shouldUseJalali()) {
    return jMoment(dt).jDaysInMonth();
  }

  return moment(dt).daysInMonth();
}

/**
 * Format relative time (e.g., "2 days ago")
 */
export function fromNow(dt) {
  if (!dt) {
    return '';
  }

  if (shouldUseJalali()) {
    return jMoment(dt).fromNow();
  }

  return moment(dt).fromNow();
}

/**
 * Check if date is valid
 */
export function isValid(dt) {
  if (!dt) {
    return false;
  }

  if (shouldUseJalali()) {
    return jMoment(dt).isValid();
  }

  return moment(dt).isValid();
}

/**
 * Get year for appropriate calendar
 */
export function getYear(dt) {
  if (!dt) {
    return null;
  }

  if (shouldUseJalali()) {
    return jMoment(dt).jYear();
  }

  return moment(dt).year();
}

/**
 * Get month for appropriate calendar (0-indexed)
 */
export function getMonth(dt) {
  if (!dt) {
    return null;
  }

  if (shouldUseJalali()) {
    return jMoment(dt).jMonth();
  }

  return moment(dt).month();
}

/**
 * Get day of month for appropriate calendar
 */
export function getDate(dt) {
  if (!dt) {
    return null;
  }

  if (shouldUseJalali()) {
    return jMoment(dt).jDate();
  }

  return moment(dt).date();
}

/**
 * Create date from year, month, day in appropriate calendar
 */
export function createDate(year, month, day) {
  if (shouldUseJalali()) {
    return jMoment().jYear(year).jMonth(month).jDate(day);
  }

  return moment().year(year).month(month).date(day);
}

/**
 * Convert Persian/Arabic numerals to English
 */
export function normalizeDigits(str) {
  if (!str) {
    return str;
  }

  const persianDigits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
  const arabicDigits = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];

  let result = str;
  for (let i = 0; i < 10; i++) {
    result = result.replace(new RegExp(persianDigits[i], 'g'), i.toString());
    result = result.replace(new RegExp(arabicDigits[i], 'g'), i.toString());
  }

  return result;
}

/**
 * Convert English numerals to Persian
 */
export function toPersianDigits(str) {
  if (!str) {
    return str;
  }

  const persianDigits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
  let result = str.toString();

  for (let i = 0; i < 10; i++) {
    result = result.replace(new RegExp(i.toString(), 'g'), persianDigits[i]);
  }

  return result;
}

export default {
  shouldUseJalali,
  toJalaali,
  fromJalaali,
  formatDate,
  formatDateTime,
  parseDate,
  now,
  toDisplayString,
  getMonthNames,
  getWeekdayNames,
  dateRange,
  startOf,
  endOf,
  daysInMonth,
  fromNow,
  isValid,
  getYear,
  getMonth,
  getDate,
  createDate,
  normalizeDigits,
  toPersianDigits,
};
