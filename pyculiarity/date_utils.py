# -*- coding: utf-8 -*-
from datetime import datetime
from heapq import nlargest
from re import match
import pytz
import numpy as np
import itertools

def datetimes_from_ts(column):
    return column.map(
        lambda datestring: datetime.fromtimestamp(int(datestring), tz=pytz.utc))

def date_format(column, format):
    return column.map(lambda datestring: datetime.strptime(datestring, format))

def format_timestamp(indf, index=0):
    if indf.dtypes[0].type is np.datetime64:
        return indf

    column = indf.iloc[:,index]

    if match("^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2} \\+\\d{4}$",
             column[0]):
        column = date_format(column, "%Y-%m-%d %H:%M:%S")
    elif match("^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}$", column[0]):
        column = date_format(column, "%Y-%m-%d %H:%M:%S")
    elif match("^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}$", column[0]):
        column = date_format(column, "%Y-%m-%d %H:%M")
    elif match("^\\d{2}/\\d{2}/\\d{2}$", column[0]):
        column = date_format(column, "%m/%d/%y")
    elif match("^\\d{2}/\\d{2}/\\d{4}$", column[0]):
        column = date_format(column, "%Y%m%d")
    elif match("^\\d{4}\\d{2}\\d{2}$", column[0]):
        column = date_format(column, "%Y/%m/%d/%H")
    elif match("^\\d{10}$", column[0]):
        column = datetimes_from_ts(column)

    indf.iloc[:,index] = column

    return indf


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)


def get_gran(tsdf, index=0):
    col = tsdf.iloc[:, index]
    n = len(col)

    granularities = []
    largest_10 = nlargest(10, col)
    for current, previous in pairwise(largest_10):
        seconds_between = int(round(np.timedelta64(current - previous) / np.timedelta64(1, 's')))
        granularities.append(seconds_between)

    gran = np.mean(granularities)

    if gran >= 0.97 * 86400:
        return "day"
    elif gran >= 0.97 * 3600:
        return "hr"
    elif gran >= 0.97 * 60:
        return "min"
    elif gran >= 0.97 * 1:
        return "sec"
    else:
        return "ms"


