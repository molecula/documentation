# Regenerating SQL SVGs

The scripts in this folder are used to regenerate the images found in the /img/sql/ folder.

## makebnf.sh

Start by running the makebnf.sh script. This will generate the sql3.html file that is required for the next step. First install any dependencies (likely ebnf2railroad)

`npm install -g ebnf2railroad`

Next, run the script:

`./makebnf.sh`

You should see some `Missing reference...` output followed by:

`📜 Document created at ./sql3.html`

## extract.py

Next, run the extract.py script, which extract all of the images in the sql3.html file and places them in /img/sql. This is intended to be run in python3 and will likely have a couple of dependencies:

Conda:
`conda install bs4`
`conda install lxml`

Pip:
`pip install bs4`
`pip install lxml`

Run the script:

`python extract.py`

All done! Go validate the images have been properly updated in the /img/sql folder.