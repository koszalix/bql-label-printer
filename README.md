# Brother Label Printer UI

This is a very simple web interface to create text labels on a Brother QL series label printers supported by [pklaus/brother_ql](https://github.com/pklaus/brother_ql).

This repository is a fork/ derivative of https://github.com/splitbrain/bql-label-printer  

## Installation

To install this tool run

```
git clone https://github.com/koszalix/bql-label-printer.git
cd bql-label-printer
./install.sh
```

This script need root privileges to run.

The bql-label-printer is installed as as service named `bql`.

## Configuration file

The software configuration is stored in `/etc/bql-label-printer/bql.yml`, configuration file
is yaml based.

**Backend**

To configure printer backend edit the `backend` section, see [brother-ql](https://pypi.org/project/brother-ql/) documentation
for detailed backend configuration.

```
backend:
  printer: #specify printer addres
  model: #specify printer models
```

**Server**

To configure server itself (ip address port etc) edit the `server` section

```
server:
  host: # server ip addr, use "0.0.0.0" for  all ips
  port: # service port
  debug: # enable debug
```

## Label Templates

Labels are based on HTML templates located in the `/opt/bql-labels/static/labels/` directory. 
Templates need to start with a supported label size followed by an underscore.
See [pklaus/brother_ql](https://github.com/pklaus/brother_ql) for a list of supported sizes.

Templates need to placed in category, to create category for labels, just create a directory, 
directory name is also a category name. Example file structure of labels is presented bellow.

```
static/labels
  box
    bigbox.html
    smallbox.html
  jar
    whiskey.html
    in.html
```

The templates need to contain exactly one root element, 
specifying the exact size of the label in pixels (again, check the above site for proper values).
Elements containing an `input` class can be edited through the form.

Divs with the `qrcode` class will be converted to a QR Code. They also need the `input` class and a `data-value` attribute instead of an inner text.
  
To enable auto cut for label set `cut` to `True` in  main `<div>` of label definition. 

To enable rotation set `rotation` to specific angle (range from 0 to 360) in main `<div>` of label definition.

## Labels Libraries

Originally the labels were located in the `bql-label-printer` repository, but to make code clean I've decided
to split labels libraries and source code. 

See [source repository labels](https://github.com/splitbrain/bql-label-printer/tree/master/static/labels)
installation of labels is described in chapter above.

## Feedback

Please feel free to submit feedback in the form of pull requests.

## Credits

Many thanks to the following projects:

* [pklaus/brother_ql](https://github.com/pklaus/brother_ql)
* [1904labs/dom-to-image-more](https://github.com/1904labs/dom-to-image-more)
* [oxalorg/sakura](https://github.com/oxalorg/sakura)
* [KeeeX/qrcodejs](https://github.com/KeeeX/qrcodejs)
* [splitbrain](https://github.com/splitbrain/bql-label-printer)
