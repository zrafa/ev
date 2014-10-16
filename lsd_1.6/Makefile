# -----------------------------------------------------------------------------
#
# LSD - Line Segment Detector on digital images
#
# Copyright (c) 2007-2011 rafael grompone von gioi <grompone@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# -----------------------------------------------------------------------------

mipsel:
	PATH=/usr/local/jlime-2010.1/mipsel/bin/:/usr/bin/:/bin/ mipsel-linux-gcc -O3 -o lsd-mipsel lsd_cmd.c lsd.c -lm
mips:
	mips-linux-gnu-gcc -O3 -o lsd-mips lsd_cmd.c lsd.c -lm

openwrt:
	PATH=/home/rafa/embebidos/mr3020/OpenWrt-Toolchain-ar71xx-for-mips_r2-gcc-4.6-linaro_uClibc-0.9.33.2/toolchain-mips_r2_gcc-4.6-linaro_uClibc-0.9.33.2/bin/:/usr/bin:/bin/ mips-openwrt-linux-gcc -O3 -o lsd-openwrt lsd_cmd.c lsd.c -lm


all: lsd lsd_call_example

lsd: lsd.c lsd.h lsd_cmd.c
	cc -O3 -pg -o lsd lsd_cmd.c lsd.c -lm

lsd_call_example: lsd.c lsd.h lsd_call_example.c
	cc -o lsd_call_example lsd_call_example.c lsd.c -lm

doc: lsd.c lsd.h doxygen.config
	doxygen doxygen.config

clean:
	rm -f lsd lsd_call_example lsd-mipsel lsd-mips lsd-openwrt

cleandoc:
	rm -rf doc

# -----------------------------------------------------------------------------
