# -*- coding: utf-8 -*-
# Copyright (C) 2009 Lado Kumsiashvili <herrlado@arcor.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.




#Nokia E63  RM-437, RM-449, RM-450
KBD_E63_V = [u'RM-437', u'RM-449', u'RM-450', u'RM-530', u'RM-529']

#Nokia E61  RM-89, RM-227, RM-294
KBD_E61_V = [u'RM-89', u'RM-227', u'RM-294']

#Nokia E71  RM-346, RM-357, RM-407, RM-493, RM-462
#Nokia E72  RM-530, RM-529
KBD_E71_V = [u'RM-346', u'RM-357', u'RM-407', u'RM-493', u'RM-462',u'RM-530', u'RM-529']

#Nokia E70      RM-10, RM-24
#Nokia E90      RA-6,  RA-7
DBL_KBD_V = [u'RM-10',u'RM-24',u'RA-6',u'RA-7']


#Nokia N97
#Nokia E75      RM-412, RM-413
#Nokia 5730 XpressMusic RM-465,RM-468
N97_V = [u'RM-505',u'RM-507',u'RM-555', u'N97-5', u'RM-412',u'RM-413',u'RM-465',u'RM-468']

def getFW():
    import sysinfo
    sw = sysinfo.sw_version()
    sw_list = sw.split(' ')
    if sw[0].isalpha():
        firmware_code = sw_list[3]
    else:
        firmware_code = sw_list[2]
    return firmware_code
