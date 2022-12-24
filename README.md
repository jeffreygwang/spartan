# Spartan

Spartan is an application that utilizes **sp**eech to generate **art** in seconds. 

# To Run

```
git clone https://github.com/jeffreyywangg/spartan
conda env create -f ./spartan/environment.yml
conda activate spartan
```

Then, add your OpenAI API key in `methods.py`, and run:

```
python app.py
```

# Extensions (WIP)
- Make language-agnostic

- Make a GUI for this (computer application use).

- Make this into a piece of physical hardware: press button; see art. 
    - Purchase a Raspberry Pi and a square mini-TV/monitor.
    - Install a button that, when pressed, records sound from a mic. 
    - Run this workflow and then display the image. 