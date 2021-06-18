import datetime
import locale

now = datetime.datetime.now()
print(now)

formatStr = '%B %d, %Y %I:%M:%S %p'

locale.setlocale(locale.LC_ALL, '')
print(locale.getlocale(locale.LC_ALL))
print('default :', now.strftime(formatStr))

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
print(locale.getlocale(locale.LC_ALL))
print('specific:', now.strftime(formatStr))

print('\nconversion')
date_str = 'July 1, 2021   1:23:45 pm'
print('string  :', date_str)
date_dt = datetime.datetime.strptime(date_str, formatStr)
print('convert :', date_dt)
