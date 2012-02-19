graphtecprint v1.0.1

(c) 2008 Vidar Madsen <vidarino@gmail.com>

http://vidar.gimp.org/graphtecprint/


1. About

graphtecprint is a driver / cutting application for the desktop plotter /
cutter Graphtec CC200-20 or any of the OEM models based on it, such as
the QuicKutz Silhouettei or the Xyron Wishblade. It may work on other
Graphtec devices as well, but it's so far only tested on the CC200-20.
It was developed on Linux, but in theory it should work on other Unix-
like operating systems, too, and perhaps even Windows (not tested!). The
rest of this document will assume that you're using a Linux distribution.


2. Requirements

First of all, and unsurprisingly, you need a compatible Graphtec cutter.
To see if you have a compatible device, run "lsusb". You should see a line looking something like this, the important bit in bold:

    $ lsusb
    . . .
    Bus 001 Device 003: ID 0b4d:110a
    . . .

If the numbers differ you likely have another model, but it might still work.
You can also use the "usb_printerid" utility that comes with "foo2zjs" package you may or may not already have installed:

    $ sudo usb_printerid /dev/usb/lp1
    GET_DEVICE_ID string:
    MANUFACTURER:Graphtec;MODEL:CC200-20;CLASS:PRINTER;DESCRIPTION:Graphtec CC200-20;


graphtecprint requires the following packages to be installed:

  - python (tested with 2.5, other versions may work)
  - python-gtk2
  - python-glade2
  - python-cairo
  - pstoedit (tested with version 3.44, others may work)
  - ghostscript

If you are using Debian or a Debian based distribution, such as Ubuntu,
running  "sudo apt-get install <package names>" should do the trick. For
other distributions, follow the normal procedure of finding and installing
software.


3. Installing

There are two ways of "installing" graphtecprint. The first way is to
install it alongside other installed programs:

    tar xvzf graphtecprint-1.0.tar.gz
    cd graphtecprint-1.0
    sudo cp graphtecprint /usr/local/bin/
    sudo mkdir /usr/local/share/graphtecprint
    sudo cp *.png *.glade /usr/local/share/graphtecprint

Alternatively, the program and data files can be installed in their own
separate directory, e.g. /opt/graphtecprint:

    tar xvzf graphtecprint-1.0.tar.gz
    cp -a graphtecprint-1.0 /opt/graphtecprint


4. Usage

The program was primarily tested to work with Inkscape, but in theory,
all applications capable of printing PostScript to a file or a pipe should
work. If you come across a program whose output does not work, feel free
to inform the author. (Note! Raster graphics from programs such as the
GIMP can't possibly work. Only vector graphics elements will be parsed by
this program.)

To cut using Inkscape, open or edit your file of choice, then go to the
File menu and select Print. In the Print dialog, select "Print using
PostScript operators". Under "Print destination", type "| graphtecprint"
(the first symbol is a pipe symbol). If you have installed graphtecprint
under a directory that's not in your path you must enter the full path
instead, e.g. "| /opt/graphtecprint/graphtecprint"

If you're using another application, see if it can print to a pipe
directly. If so, the procedure should be very similar to the one above.

If the application can not print to a pipe, chose "Print to file" (most
applications should offer this) and select an appropriate file name. Then,
in a terminal window, run "graphtecprint < somefile.ps", substituting
"somefile.ps" for the name of the file you just printed to.

If everything goes according to plan, you should now get the main dialog
window. If not, check your program's terminal for error messages that
may explain what went wrong.


5. Notes

Everything should be more or less self-explanatory, but there are some
things to note:

- You need write access to the USB device file! (The "Device" pulldown menu
should list the detected cutter and its character device. To give yourself
(everyone, actually, so beware) write permissions, open a terminal window
and run the command "sudo chmod a+rw /dev/usb/lpX", where X is the number
of the device shown in the pulldown menu.)

- Paper size should match the page size from your application. This
information doesn't make it through the format conversions, unfortunately.

- Orientation is hardcoded to portrait so far, as the overlying application
would normally do the work of rotating it if it is a landscape drawing.

- The fine tuning buttons will not work with the usblp driver. For these to
work you will need a separate driver for the cutter, or possibly a patched
usblp driver. None of these options are implemented yet, but they might be
in the future.


