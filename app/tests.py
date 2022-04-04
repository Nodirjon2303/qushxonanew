from django.test import TestCase
import zoneinfo
# Create your tests here.
a = list(zoneinfo.available_timezones())
print(a)

for i in a:
    if 'sia' in i:
        print(i)